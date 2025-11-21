# EPIC 2 : Guide Technique Détaillé

## 📐 Architecture Globale

```
┌─────────────────────────────────────────────────────────────┐
│                     main.py (Streamlit)                     │
│                                                              │
│  Tab 1: EPIC 1 (DVF+)  | Tab 2: EPIC 2 (Perplexity) |       │
└─────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
        ┌───────────▼──────────┐   ┌──▼────────────────┐
        │  epic_2_perplexity.py│   │ Sidebar Filters  │
        │  (UI Component)      │   │ & Search Button  │
        └──────────┬───────────┘   └──────────────────┘
                   │
        ┌──────────▼──────────────┐
        │ perplexity_retriever.py │
        │  (Backend Service)      │
        └──────────┬──────────────┘
                   │
        ┌──────────▼──────────────┐
        │   Perplexity API        │
        │  (httpx Async Client)   │
        └──────────┬──────────────┘
                   │
        ┌──────────▼──────────────┐
        │ Google Maps Geocoding   │
        │ (Enrichissement lat/lon)│
        └────────────────────────┘
```

---

## 🏗️ Module Backend : `src/perplexity_retriever.py`

### Classes Pydantic (Validation)

#### 1. `PropertyType` (Enum)
```python
class PropertyType(str, Enum):
    APARTMENT = "apartment"
    HOUSE = "house"
    STUDIO = "studio"
    TOWNHOUSE = "townhouse"
    ALL = "all"
```

**Utilité** : Énumération des types de bien supportés

#### 2. `PerplexityProperty` (BaseModel)
```python
class PerplexityProperty(BaseModel):
    address: str                              # Obligatoire
    price: Optional[float] = None             # Validé: >= 0
    surface: Optional[float] = None           # Validé: >= 0
    rooms: Optional[int] = None
    property_type: Optional[str] = None
    listing_url: Optional[str] = None
    publication_date: Optional[str] = None
    description: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    @field_validator("price")
    @classmethod
    def validate_price(cls, v):
        if v is not None and v < 0:
            raise ValueError("Le prix doit être positif")
        return v

    @field_validator("surface")
    @classmethod
    def validate_surface(cls, v):
        if v is not None and v < 0:
            raise ValueError("La surface doit être positive")
        return v
```

**Validations** :
- Prix et surface doivent être positifs (Pydantic rejette automatiquement)
- Autres champs optionnels peuvent être None
- `.model_dump()` convertit en dict (Pydantic V2)

#### 3. `PerplexityResponse` (BaseModel)
```python
class PerplexityResponse(BaseModel):
    properties: List[PerplexityProperty] = Field(default_factory=list)
    total_count: int = Field(default=0)
    search_query: str = Field(default="")
```

**Usage** : Format attendu de la réponse API (non utilisé actuellement, réservé pour futures évolutions)

---

### Classe Service : `PerplexityRetriever`

#### Constantes
```python
BASE_URL = "https://api.perplexity.ai/chat/completions"
MODEL = "sonar"                    # Modèle Perplexity utilisé
MAX_RETRIES = 3                    # Retries exponentiels
RETRY_DELAY = 1                    # 1 seconde (base)
REQUEST_TIMEOUT = 30               # 30 secondes
```

#### `__init__`
```python
def __init__(self):
    self.api_key = Config.PERPLEXITY_API_KEY
    if not self.api_key:
        logger.error("[ERROR] PERPLEXITY_API_KEY non configurée")
        self.client = None
    else:
        self.client = httpx.AsyncClient(
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
```

**Points clés** :
- Charge clé depuis `Config` (`.env.local`)
- Crée un client async (non-bloquant)
- Header Authorization pour Perplexity

#### `_make_request_with_retry` (Async)
```python
async def _make_request_with_retry(
    self,
    prompt: str,
    max_retries: int = MAX_RETRIES
) -> Optional[Dict]:
```

**Logique** :
1. Loop `for attempt in range(max_retries):`
2. POST vers Perplexity API avec payload JSON
3. Capture d'erreurs spécifiques :
   - `TimeoutException` → Retry avec backoff
   - `HTTPStatusError` 429 (rate limit) → Retry
   - `HTTPStatusError` autres → Erreur finale
4. Backoff exponentiel : `RETRY_DELAY * (2 ** attempt)` = 1s, 2s, 4s

**Exemple timeline** :
```
Tentative 1 : POST → Timeout → Attendre 1s
Tentative 2 : POST → Timeout → Attendre 2s
Tentative 3 : POST → Timeout → Attendre 4s → Retour None
```

#### `_build_search_prompt`
```python
def _build_search_prompt(
    self,
    city: str,
    postal_code: str,
    property_type: str = "all",
    price_min: Optional[float] = None,
    price_max: Optional[float] = None,
    radius_km: int = 5,
) -> str:
```

**Génère** :
```
Recherche les biens immobiliers actuellement à vendre dans {city} ({postal_code}),
dans un rayon de {radius_km}km.

Critères:
- Type: {property_type}
- Prix: {price_min} - {price_max} euros
- Rayon: {radius_km}km

Retourne JSON structuré avec: address, price, surface, rooms, property_type,
listing_url, publication_date, description

[Instruction finale: Retourne SEULEMENT le JSON valide]
```

#### `_parse_perplexity_response`
```python
def _parse_perplexity_response(
    self,
    response_data: Dict
) -> List[PerplexityProperty]:
```

**Étapes** :
1. Extrait `response_data["choices"][0]["message"]["content"]`
2. Parse JSON depuis le contenu
3. Valide chaque property avec Pydantic
4. Skip les properties invalides (log warning)
5. Retourne liste `PerplexityProperty`

**Gestion erreurs** :
- Format inattendu → [] vide
- JSON invalide → [] vide
- Property invalide → Skip + continue

#### `_enrich_with_geocoding` (Async)
```python
async def _enrich_with_geocoding(
    self,
    properties: List[PerplexityProperty]
) -> List[Dict]:
```

**Logique** :
1. Boucle chaque property
2. Convertir `PerplexityProperty` → dict avec `.model_dump()`
3. Si `latitude` ou `longitude` manquants :
   - Appeler `get_coordinates(address)` (Google Maps)
   - Si succès → Ajouter lat/lon au dict
   - Si échoue → Log warning, garder None
4. Retourne liste de dicts enrichis

#### `search_properties_for_sale` (Async - Main Public Method)
```python
async def search_properties_for_sale(
    self,
    city: str,
    postal_code: str,
    property_type: str = "all",
    price_min: Optional[float] = None,
    price_max: Optional[float] = None,
    radius_km: int = 5,
) -> List[Dict]:
```

**Workflow complet** :
1. Vérifier `self.client` initialisé
2. Construire prompt avec `_build_search_prompt`
3. Appeler API avec retries : `_make_request_with_retry(prompt)`
4. Parser réponse : `_parse_perplexity_response(response_data)`
5. Enrichir coords : `_enrich_with_geocoding(properties)`
6. Retourner liste dicts (ou [] si erreur)

---

## 🎨 Module Frontend : `src/ui/epic_2_perplexity.py`

### Fonctions Utilitaires

#### `get_perplexity_service()`
```python
@st.cache_resource(show_spinner=False)
def get_perplexity_service():
    """Retourne instance singleton (cache Streamlit)"""
```

**Pattern** : Singleton en cache Streamlit → Une seule instance par session

#### `_build_property_map(properties, center_lat, center_lon)`
```python
def _build_property_map(
    properties: pd.DataFrame,
    center_lat: float,
    center_lon: float
) -> folium.Map:
```

**Crée** :
1. Base map centrée sur `(center_lat, center_lon)` avec zoom 13
2. Marqueur bleu pour bien cible (🏠 info-sign)
3. Marqueurs colorés pour chaque bien :
   - Calcul ratio prix : `(price - min) / range`
   - Vert (ratio < 0.33), Orange (0.33-0.66), Rouge (> 0.66)
   - Popup enrichi avec adresse, prix, surface, URL cliquable
4. Retourne objet Folium Map

#### `_apply_filters(properties, price_min, price_max, publication_after)`
```python
def _apply_filters(
    properties: pd.DataFrame,
    price_min: Optional[float],
    price_max: Optional[float],
    publication_after: Optional[str]
) -> pd.DataFrame:
```

**Filtre** :
- `price >= price_min` (si défini)
- `price <= price_max` (si défini)
- `publication_date >= publication_after` (si défini)

#### `_get_csv_download_link(df)`
```python
def _get_csv_download_link(df: pd.DataFrame) -> bytes:
```

**Convertit** : DataFrame → CSV → Bytes (UTF-8-sig pour Excel compatibility)

---

### Fonction Principale : `render()`

#### Phase 1 : Vérification Prérequis
```python
if 'bien_params' not in st.session_state or st.session_state['bien_params'] is None:
    st.info("Aucun bien saisie - Remplissez le formulaire en EPIC 1 d'abord")
    return
```

#### Phase 2 : Sidebar Filters
```python
with st.sidebar:
    rayon_km = st.slider(...)
    property_type = st.selectbox(...)
    price_min = st.number_input(...)
    price_max = st.number_input(...)
    publication_after = st.date_input(...)
    search_button = st.button("🔍 Rechercher")
```

#### Phase 3 : Logique de Recherche
```python
if search_button or st.session_state.get('perplexity_results_cached'):
    st.session_state['perplexity_results_cached'] = True

    with st.spinner("⏳ Recherche Perplexity..."):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        results = loop.run_until_complete(
            perplexity_service.search_properties_for_sale(...)
        )

        loop.close()
        st.session_state['perplexity_results'] = pd.DataFrame(results)
```

**Points clés** :
- Event loop créé/fermé pour chaque recherche
- Résultats stockés en session_state (cache)
- Flag `perplexity_results_cached` pour éviter recherches répétées

#### Phase 4 : Affichage Résultats (3 Tabs)

**Tab 1 : Tableau**
- Formatage colonnes (prix €, surface m², URLs cliquables)
- `st.dataframe()` interactif
- `st.download_button()` pour CSV

**Tab 2 : Carte**
- Appelle `_build_property_map()`
- `st_folium()` affiche la carte (1200x600)

**Tab 3 : Statistiques**
- 4 metrics : prix moyen, surface, pièces, prix/m²
- 2 charts : distribution type, distribution prix

---

## 🧪 Tests : `tests/unit/test_perplexity_retriever.py`

### Structure

```
TestPerplexityProperty
├── test_valid_property
├── test_negative_price_validation
├── test_negative_surface_validation
└── test_optional_fields

TestPerplexityRetriever
├── test_build_search_prompt_basic
├── test_build_search_prompt_with_filters
├── test_parse_perplexity_response_valid
├── test_parse_perplexity_response_empty
├── test_parse_perplexity_response_invalid_json
├── test_parse_perplexity_response_missing_choices
├── test_parse_perplexity_response_invalid_property
├── test_make_request_with_retry_success [ASYNC]
├── test_make_request_with_retry_timeout [ASYNC]
├── test_make_request_with_retry_rate_limit [ASYNC]
├── test_make_request_with_retry_http_error [ASYNC]
├── test_enrich_with_geocoding_success [ASYNC]
├── test_enrich_with_geocoding_failure [ASYNC]
├── test_enrich_with_geocoding_already_has_coords [ASYNC]
├── test_search_properties_for_sale_full_workflow [ASYNC]
└── test_search_properties_no_client [ASYNC]
```

### Mocks Utilisés

```python
@patch("src.perplexity_retriever.Config.PERPLEXITY_API_KEY", "test-key")
@patch("src.perplexity_retriever.get_coordinates")
```

- Mocking Config pour éviter `.env.local`
- Mocking `get_coordinates` pour tester sans appel Google Maps réel

### Exécution

```bash
pytest tests/unit/test_perplexity_retriever.py -v
pytest tests/unit/test_perplexity_retriever.py::TestPerplexityProperty -v
pytest tests/unit/test_perplexity_retriever.py --cov=src.perplexity_retriever
```

---

## 🔄 Data Flow Complet

```
Utilisateur remplit EPIC 1
    ↓
bien_params = {address, type_bien, surface, latitude, longitude}
    ↓
st.session_state['bien_params'] = well_params
    ↓
Utilisateur accède EPIC 2 (Tab 2)
    ↓
EPIC 2 lit bien_params depuis session_state
    ↓
Utilisateur règle filtres (rayon, prix, type, date)
    ↓
Clique "🔍 Rechercher"
    ↓
PerplexityRetriever.search_properties_for_sale() [ASYNC]
    ├── _build_search_prompt()
    ├── _make_request_with_retry() [loop retry 3x]
    ├── _parse_perplexity_response()
    └── _enrich_with_geocoding()
    ↓
Résultats en DataFrame
    ↓
st.session_state['perplexity_results'] = df
    ↓
Affiche 3 tabs:
    ├── Tab 1: Tableau + Export CSV
    ├── Tab 2: Carte Folium colorée
    └── Tab 3: Metrics + Charts
```

---

## 🔐 Sécurité & Best Practices

### API Key Management
```python
# ❌ Ne pas faire :
PERPLEXITY_API_KEY = "pplx-xxxxx" # Hardcoded

# ✅ Faire :
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
if not PERPLEXITY_API_KEY:
    logger.error("[ERROR] PERPLEXITY_API_KEY manquante")
```

### Validation des Données
```python
# ✅ Pydantic validators
@field_validator("price")
@classmethod
def validate_price(cls, v):
    if v is not None and v < 0:
        raise ValueError("Doit être positif")
    return v
```

### Error Handling
```python
# ✅ Capture spécifique
try:
    ...
except httpx.TimeoutException:
    # Retry logic
except httpx.HTTPStatusError as e:
    if e.response.status_code == 429:
        # Rate limit retry
    else:
        # Error log
except Exception:
    logger.error("Unknown error")
```

---

## 📊 Complexité & Performance

### Time Complexity
- Search: O(1) API call (constant)
- Parsing: O(n) où n = nombre de properties
- Enrichissement: O(n * m) où m = appels géocodage

### Space Complexity
- O(n) pour storage results en session_state

### Optimisations
- ✅ Async/await non-bloquant
- ✅ Session state cache
- ✅ Exponential retry backoff (évite hammering)
- ✅ Singleton retriever

---

**Dernière mise à jour** : 2025-11-21
