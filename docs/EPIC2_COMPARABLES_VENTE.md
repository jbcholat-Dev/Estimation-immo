# EPIC 2 : Comparables en Vente (Perplexity API)

## 🎯 Vue d'ensemble

L'EPIC 2 permet de rechercher les **biens immobiliers actuellement en vente** dans une zone géographique donnée, en utilisant l'**API Perplexity** pour accéder aux annonces web en temps réel.

Contrairement à l'EPIC 1 (comparables passés - DVF+), l'EPIC 2 fournit des données **actuelles** et **vivantes** du marché immobilier.

---

## 📋 Fonctionnalités

### 1. Recherche Web via Perplexity
- Interroge l'API Perplexity avec critères de recherche
- Récupère les biens en vente avec prix, surface, type, URL
- Enrichit automatiquement les données avec **géocodage** (lat/lon via Google Maps)
- Gestion robuste des erreurs et retries exponentiels

### 2. Filtres de Recherche
- **Rayon géographique** : 1-50 km autour du bien cible
- **Type de bien** : Tous, Appartement, Maison, Studio, Duplex
- **Fourchette de prix** : Min/Max configurable
- **Date de publication** : Afficher seulement les annonces récentes

### 3. Visualisations Interactives

#### Tab 1 : Tableau des Résultats
- Affichage structuré de tous les biens trouvés
- Colonnage formaté (prix en €, surface en m², URLs cliquables)
- **Export CSV** avec timestamp

#### Tab 2 : Carte Folium
- Marqueur bleu = **bien cible** (bien à estimer)
- Marqueurs colorés = biens en vente
  - 🟢 Vert : prix bas (< 33e percentile)
  - 🟠 Orange : prix moyen (33-66e percentile)
  - 🔴 Rouge : prix haut (> 66e percentile)
- Popups enrichies : adresse, prix, surface, type, pièces, URL
- Zoom intelligent

#### Tab 3 : Statistiques
- **Metrics** : Prix moyen, surface moyenne, pièces moyennes, prix/m²
- **Charts** : Distribution par type de bien, distribution des prix (histogramme)

---

## 🔧 Architecture Technique

### Backend : `src/perplexity_retriever.py`

**Classe principale** : `PerplexityRetriever`

#### Méthodes publiques

```python
async def search_properties_for_sale(
    city: str,                          # Ville (ex: "Thonon-les-Bains")
    postal_code: str,                   # Code postal (ex: "74200")
    property_type: str = "all",         # Type bien (apartment, house, studio, townhouse, all)
    price_min: Optional[float] = None,  # Prix minimum en €
    price_max: Optional[float] = None,  # Prix maximum en €
    radius_km: int = 5,                 # Rayon recherche en km
) -> List[Dict]:
    """
    Recherche biens en vente via Perplexity API et enrichit avec géocodage.

    Returns: Liste de dicts avec clés:
        - address: adresse complète
        - price: prix en €
        - surface: surface en m²
        - rooms: nombre de pièces
        - property_type: type de bien
        - listing_url: URL annonce
        - publication_date: date publication
        - latitude: latitude WGS84
        - longitude: longitude WGS84
    """
```

#### Gestion des Erreurs & Retries
- **Timeout** : Retry 3x avec délai exponentiel (1s, 2s, 4s)
- **Rate limit (429)** : Retry automatique avec backoff
- **Parsing JSON** : Validation Pydantic, skip items invalides
- **Géocodage** : Fallback gracieux si échec

### Frontend : `src/ui/epic_2_perplexity.py`

**Fonction principale** : `render()`

#### Dépendances session_state
- `bien_params` : Paramètres du bien saisi dans EPIC 1 (obligatoire)
- `perplexity_results` : Cache des résultats recherche

#### Layout

```
Sidebar (gauche)
├── Rayon de recherche (slider)
├── Type de bien (selectbox)
├── Fourchette prix (2 colonnes)
├── Date minimale (date_input)
└── 🔍 Bouton recherche

Main (3 tabs si résultats)
├── Tab 1: Tableau + Export CSV
├── Tab 2: Carte Folium interactive
└── Tab 3: Statistiques + Charts
```

---

## 🚀 Utilisation

### Prérequis

1. **Configuration** : Clé Perplexity dans `.env.local`
   ```env
   PERPLEXITY_API_KEY=pplx-xxxxx...
   ```

2. **Dépendances installées**
   ```bash
   pip install -r requirements.txt
   ```

### Workflow Utilisateur

1. **Lancez l'application**
   ```bash
   streamlit run main.py
   ```

2. **EPIC 1 : Comparables Vendus (DVF+)**
   - Remplissez le formulaire (adresse, type, surface)
   - Cliquez "🚀 Estimer"
   - Les paramètres sont stockés dans `st.session_state['bien_params']`

3. **EPIC 2 : Comparables en Vente**
   - Allez à l'onglet "2. Comparables en Vente"
   - Les paramètres du bien sont **automatiquement chargés**
   - Réglez les filtres (rayon, prix, type, date)
   - Cliquez "🔍 Rechercher comparables en vente"
   - Explorez les 3 onglets : Tableau, Carte, Statistiques

### Exemple d'Utilisation Programmatique

```python
import asyncio
from src.perplexity_retriever import get_perplexity_retriever

async def main():
    service = get_perplexity_retriever()

    results = await service.search_properties_for_sale(
        city="Thonon-les-Bains",
        postal_code="74200",
        property_type="house",
        price_min=250000,
        price_max=500000,
        radius_km=10
    )

    for prop in results:
        print(f"{prop['address']} - {prop['price']}€")

    await service.close()

asyncio.run(main())
```

---

## 🧪 Tests

### Exécuter les tests

```bash
# Tous les tests EPIC 2
pytest tests/unit/test_perplexity_retriever.py -v

# Test spécifique
pytest tests/unit/test_perplexity_retriever.py::TestPerplexityProperty::test_valid_property -v

# Avec coverage
pytest tests/unit/test_perplexity_retriever.py --cov=src.perplexity_retriever
```

### Coverage

- **20 tests unitaires** : 100% passing ✅
- **Validation Pydantic** : 4 tests
- **Retry logic** : 4 tests
- **Parsing & enrichissement** : 8 tests
- **Workflow complet** : 4 tests

### Mocks Utilisés

- `httpx.AsyncClient.post()` : Simulation appels API
- `get_coordinates()` : Simulation géocodage

---

## 🔍 Dépannage

### ❌ Aucun bien trouvé

**Causes possibles** :
1. **Clé Perplexity invalide ou manquante** → Vérifier `.env.local`
2. **Critères trop restrictifs** → Augmenter rayon, relâcher filtres prix
3. **Ville/code postal invalide** → Vérifier orthographe exacte
4. **Timeout API** → Réessayer (retry automatique après 3 tentatives)

**Solutions** :
- Vérifier logs : `python -c "from src.perplexity_retriever import get_perplexity_retriever; print(get_perplexity_retriever().api_key)"`
- Tester avec rayon plus grand (ex: 20 km)
- Vérifier que `bien_params` est bien chargé en EPIC 1

### ❌ Erreur "Client Perplexity non initialisé"

**Cause** : `PERPLEXITY_API_KEY` manquante ou invalide

**Solution** :
```bash
# Vérifier config
python -c "from src.utils.config import Config; Config.validate()"

# Doit afficher [OK] Configuration valide
```

### ❌ Géocodage échoué pour une adresse

**Cause** : Google Maps API ne reconnaît pas l'adresse

**Solution** :
- Les biens sans lat/lon sont quand même affichés (tableau), mais manquent sur la carte
- Vérifier GOOGLE_MAPS_API_KEY dans `.env.local`

---

## 📊 Structure des Données

### PerplexityProperty (Pydantic Model)

```python
address: str                          # Adresse complète
price: Optional[float]                # Prix en €
surface: Optional[float]              # Surface en m²
rooms: Optional[int]                  # Nombre de pièces
property_type: Optional[str]          # Type (apartment, house, etc.)
listing_url: Optional[str]            # URL annonce
publication_date: Optional[str]       # Date (YYYY-MM-DD)
description: Optional[str]            # Description courte
latitude: Optional[float]             # Latitude WGS84
longitude: Optional[float]            # Longitude WGS84
```

### Validations
- ✅ `price >= 0` (ou None)
- ✅ `surface >= 0` (ou None)
- ✅ Champs optionnels acceptent None

---

## 🔐 Sécurité

### Clés API
- ✅ `PERPLEXITY_API_KEY` = `.env.local` uniquement (**.gitignore**)
- ✅ `.env.example` = template sans secrets
- ✅ Validation stricte en `Config.validate()`

### Validation des Données
- ✅ Pydantic V2 models avec validators
- ✅ Rejet automatique des propriétés invalides
- ✅ Pas d'injection SQL (data binding)

---

## 📈 Performance

### Optimisations
- **Async/await** : Requests non-bloquants
- **Singleton pattern** : `PerplexityRetriever` en cache
- **Session_state cache** : Résultats persistants pendant la session
- **Retry exponential** : Évite les appels inutiles

### Limits à Connaître
- **Timeout API** : 30 secondes par request
- **Retries** : 3 max (9 à 30 secondes max)
- **Coûts Perplexity** : Dépend du plan API (consulter dashboard Perplexity)

---

## 🚧 Améliorations Futures

- [ ] **Phase 3** : Cache Redis pour persistance multi-sessions
- [ ] **Phase 4** : Tests d'intégration avec vraie API Perplexity
- [ ] **Phase 5** : Persister résultats en Supabase table `comparables_vente`
- [ ] **Analytics** : Tracker quels critères sont les plus utilisés
- [ ] **Notifications** : Alerter si nouveaux biens matching critères
- [ ] **ML** : Prédire tendances prix basé sur listings actuels

---

## 📞 Support

Pour des questions ou issues :
1. Vérifier logs Streamlit (CLI)
2. Consulter `CLAUDE.md` pour contexte projet
3. Vérifier `.env.local` (clés API présentes)
4. Relancer `streamlit run main.py`

---

**Dernière mise à jour** : 2025-11-21
**Version** : 1.0
**Phase** : 5 (EPIC 2 Phase 1+2 Complete)
