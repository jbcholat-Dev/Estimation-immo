# US-8 : Perplexity Integration

**EPIC:** EPIC-002 - Onglet Comparables en Vente (Perplexity)
**Sprint:** 2-3
**Priorité:** Must Have
**Story Points:** 8 SP

## User Story

En tant qu'agent immobilier, je veux récupérer automatiquement les annonces immobilières en vente via l'API Perplexity, pour compléter mon estimation avec les prix du marché actif.

## Critères d'acceptation

- [ ] L'intégration API Perplexity est fonctionnelle
- [ ] Les paramètres de recherche incluent :
  - Localité (ville)
  - Code postal
  - Type de bien (Maison, Appartement)
  - Fourchette de prix (min-max)
  - Rayon de recherche (km)
- [ ] Les données récupérées contiennent :
  - Adresse
  - Prix affiché
  - Surface
  - Nombre de pièces
  - Description
  - URL source de l'annonce
  - Date de publication
- [ ] Le résultat s'affiche dans un tableau structuré
- [ ] Les sources URL sont cliquables
- [ ] Un message d'erreur s'affiche si l'API est indisponible
- [ ] Le temps de réponse est <10 secondes
- [ ] Les données sont stockées dans le session state

## Notes techniques

### Dépendances
- API Perplexity (clé API dans .env)
- Module requests ou httpx pour appels API
- pandas pour structuration des données
- Streamlit pour affichage

### Stack technique
- **API:** Perplexity API
- **HTTP Client:** httpx (async recommandé)
- **Parsing:** BeautifulSoup ou extraction JSON
- **Stockage temporaire:** st.session_state

### Estimation détaillée
- Configuration API Perplexity : 2h
- Développement requête structurée : 4h
- Parsing et extraction données : 6h
- Gestion erreurs et fallback : 3h
- Tests et validation : 4h
- Documentation : 2h
- **Total : 21h (8 SP)**

### Exemple de requête

```python
import httpx
import os

PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")

async def search_annonces_vente(ville: str, code_postal: str, type_bien: str, prix_min: int, prix_max: int, rayon_km: int):
    """
    Recherche d'annonces immobilières via Perplexity API.
    """
    url = "https://api.perplexity.ai/chat/completions"

    prompt = f"""
    Trouve les annonces immobilières en vente pour :
    - Ville : {ville}
    - Code postal : {code_postal}
    - Type de bien : {type_bien}
    - Prix : {prix_min}€ - {prix_max}€
    - Rayon : {rayon_km} km

    Retourne les résultats au format JSON avec :
    - adresse
    - prix
    - surface
    - pieces
    - description
    - url_source
    - date_publication
    """

    payload = {
        "model": "llama-3.1-sonar-small-128k-online",
        "messages": [
            {"role": "system", "content": "Tu es un assistant spécialisé dans la recherche d'annonces immobilières."},
            {"role": "user", "content": prompt}
        ]
    }

    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers, timeout=30.0)
        response.raise_for_status()
        return response.json()
```

### Gestion du budget API

- **Coût Perplexity :** $1 par 1M tokens
- **Estimation :** ~5,000 tokens par requête
- **Quota mensuel :** $20 = ~400 recherches
- **Cache :** Stocker résultats 24h pour éviter appels redondants

### Parsing des résultats

```python
def parse_perplexity_response(response: dict) -> pd.DataFrame:
    """
    Parse la réponse Perplexity en DataFrame structuré.
    """
    try:
        content = response['choices'][0]['message']['content']
        # Extraire JSON embarqué
        data = json.loads(content)

        df = pd.DataFrame(data['annonces'])
        return df
    except Exception as e:
        st.error(f"Erreur parsing : {e}")
        return pd.DataFrame()
```

### Risques
- API Perplexity rate limit → Cache + throttling
- Qualité extraction variable → Validation post-traitement
- Sources annonces obsolètes → Vérification date publication
- Coût API élevé → Monitoring + alertes budget

---

**Lien EPIC parent:** [README.md](./README.md)
