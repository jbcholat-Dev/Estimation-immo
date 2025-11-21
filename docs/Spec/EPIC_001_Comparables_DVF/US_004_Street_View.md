# US-4 : Street View

**EPIC:** EPIC-001 - Onglet Comparables Vendues (DVF+)
**Sprint:** 1-2
**Priorité:** Should Have
**Story Points:** 2 SP

## User Story

En tant qu'agent immobilier, je veux visualiser une photo Street View d'un comparable au clic, pour évaluer visuellement l'environnement et la qualité du bien sans me déplacer.

## Critères d'acceptation

- [ ] L'intégration Google Street View API est fonctionnelle
- [ ] Au clic sur un marqueur, la photo Street View s'affiche
- [ ] Un fallback s'affiche si aucune photo n'est disponible
- [ ] Le panneau affiche :
  - Photo Street View
  - Adresse complète
  - Prix de vente
  - Surface et prix/m²
  - Date de transaction
  - Score de similarité
- [ ] Le budget API Google Maps est surveillé
- [ ] Le chargement de l'image prend moins de 2 secondes
- [ ] L'interface reste responsive

## Notes techniques

### Dépendances
- Google Maps API (Street View Static API)
- Clé API Google configurée dans .env
- Coordonnées GPS des comparables
- Module utils/geocoding.py

### Stack technique
- **API:** Google Maps Street View Static API
- **Requête HTTP:** requests ou httpx
- **Affichage:** st.image() dans Streamlit
- **Gestion cache:** st.cache_data pour réduire appels API

### Estimation détaillée
- Configuration Google Maps API : 1h
- Intégration Street View Static : 2h
- Gestion fallback (photo indisponible) : 1h
- Optimisation cache : 1h
- Tests et monitoring budget : 1h
- **Total : 6h (2 SP)**

### URL Street View Static API

```python
BASE_URL = "https://maps.googleapis.com/maps/api/streetview"
params = {
    "size": "600x400",
    "location": f"{lat},{lng}",
    "key": GOOGLE_MAPS_API_KEY,
    "fov": 90,
    "heading": 0,
    "pitch": 0
}
```

### Gestion du budget API

- **Coût :** $7 par 1000 requêtes (Street View Static)
- **Quota gratuit :** $200/mois (≈28,000 requêtes)
- **Cache :** Stocker images en session pour éviter appels multiples
- **Monitoring :** Logs d'utilisation API dans Supabase

### Fallback

```python
if street_view_available:
    st.image(street_view_url)
else:
    st.warning("Photo Street View non disponible pour cette adresse")
    st.image("assets/placeholder.png")
```

### Risques
- Dépassement quota API → Monitoring + alertes + cache agressif
- Latence API élevée → Timeout 5s + message utilisateur
- Photos obsolètes → Afficher date de capture si disponible

---

**Lien EPIC parent:** [README.md](./README.md)
