# US-3 : Carte interactive

**EPIC:** EPIC-001 - Onglet Comparables Vendues (DVF+)
**Sprint:** 1
**Priorité:** Must Have
**Story Points:** 3 SP

## User Story

En tant qu'agent immobilier, je veux visualiser sur une carte interactive le bien à estimer et ses comparables, pour comprendre la répartition géographique et identifier les tendances locales.

## Critères d'acceptation

- [ ] La carte Folium s'affiche correctement dans Streamlit
- [ ] Le bien à estimer apparaît avec un marqueur rouge distinct
- [ ] Les comparables apparaissent avec des points colorés selon gradient de score
- [ ] Le clic sur un comparable ouvre une popup avec :
  - Adresse complète
  - Prix de vente
  - Surface et prix/m²
  - Date de transaction
  - Score de similarité
  - Lien vers Street View
- [ ] La carte se centre automatiquement sur le bien estimé
- [ ] Le zoom initial affiche tous les comparables
- [ ] Le chargement de la carte prend moins de 2 secondes
- [ ] La carte est responsive (adaptation mobile/desktop)

## Notes techniques

### Dépendances
- Folium (carte interactive)
- streamlit-folium (intégration Streamlit)
- Coordonnées GPS du bien et des comparables
- Scores de similarité calculés (US-2)

### Stack technique
- **Cartographie:** Folium 0.14+
- **Intégration:** streamlit-folium
- **Tuiles:** OpenStreetMap (par défaut)
- **Marqueurs:** folium.Marker, folium.CircleMarker
- **Popups:** HTML personnalisé

### Estimation détaillée
- Intégration Folium + Streamlit : 2h
- Création marqueurs + gradient couleurs : 2h
- Popups HTML avec détails : 2h
- Centrage automatique et zoom : 1h
- Tests et optimisation performance : 2h
- **Total : 9h (3 SP)**

### Gradient de couleurs

```python
def get_color(score):
    if score >= 80: return 'green'
    elif score >= 60: return 'lightgreen'
    elif score >= 40: return 'orange'
    else: return 'red'
```

### Popup HTML template

```html
<div style="font-family: Arial; min-width: 200px;">
    <h4>{adresse}</h4>
    <p><b>Prix :</b> {prix} €</p>
    <p><b>Surface :</b> {surface} m²</p>
    <p><b>Prix/m² :</b> {prix_m2} €/m²</p>
    <p><b>Date :</b> {date_mutation}</p>
    <p><b>Similarité :</b> {score}%</p>
    <a href="{street_view_url}" target="_blank">Voir Street View</a>
</div>
```

### Risques
- Performance dégradée si >100 marqueurs → Limiter affichage top 30
- Coordonnées GPS manquantes → Géocodage automatique ou exclusion
- Tuiles OpenStreetMap indisponibles → Fallback vers autres providers

---

**Lien EPIC parent:** [README.md](./README.md)
