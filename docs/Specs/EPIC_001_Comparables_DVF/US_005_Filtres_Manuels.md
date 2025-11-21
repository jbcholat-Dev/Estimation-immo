# US-5 : Filtres manuels

**EPIC:** EPIC-001 - Onglet Comparables Vendues (DVF+)
**Sprint:** 2
**Priorité:** Must Have
**Story Points:** 3 SP

## User Story

En tant qu'agent immobilier, je veux affiner manuellement la sélection des comparables via des sliders (rayon, années, similarité), pour adapter l'estimation à mon expertise locale.

## Critères d'acceptation

- [ ] Slider rayon de recherche : 1 à 20 km (défaut : 5 km)
- [ ] Slider ancienneté : 1 à 10 ans (défaut : 5 ans)
- [ ] Slider score de similarité minimum : 0 à 100% (défaut : 40%)
- [ ] Le filtrage s'applique en temps réel sur les comparables
- [ ] La carte et le tableau se mettent à jour automatiquement
- [ ] Le nombre de comparables restants s'affiche
- [ ] Le filtrage prend moins de 1 seconde
- [ ] Les valeurs par défaut sont optimisées pour la zone Chablais/Annemasse
- [ ] Les filtres se réinitialisent individuellement ou globalement

## Notes techniques

### Dépendances
- Streamlit sliders (st.slider)
- Session state pour persistance des valeurs
- Dataframe pandas des comparables
- Fonction de filtrage réactive

### Stack technique
- **Frontend:** Streamlit (st.slider, st.sidebar)
- **Backend:** pandas (filtrage dataframe)
- **Réactivité:** Callbacks Streamlit + session state

### Estimation détaillée
- Création des 3 sliders : 2h
- Logique de filtrage réactif : 2h
- Intégration avec carte et tableau : 2h
- Optimisation performance : 1h
- Tests et validation : 2h
- **Total : 9h (3 SP)**

### Implémentation

```python
# Sidebar filters
with st.sidebar:
    st.header("Filtres de sélection")

    rayon_km = st.slider(
        "Rayon de recherche (km)",
        min_value=1,
        max_value=20,
        value=5,
        step=1
    )

    anciennete_ans = st.slider(
        "Ancienneté max (années)",
        min_value=1,
        max_value=10,
        value=5,
        step=1
    )

    score_min = st.slider(
        "Score minimum (%)",
        min_value=0,
        max_value=100,
        value=40,
        step=5
    )

# Filtrage dataframe
df_filtered = df_comparables[
    (df_comparables['distance_km'] <= rayon_km) &
    (df_comparables['anciennete_ans'] <= anciennete_ans) &
    (df_comparables['score_similarite'] >= score_min)
]

st.metric("Comparables trouvés", len(df_filtered))
```

### Valeurs par défaut optimisées

- **Rayon 5 km :** Zone Chablais/Annemasse suffisamment dense
- **Ancienneté 5 ans :** Équilibre entre données récentes et volume
- **Score 40% :** Exclut les comparables peu pertinents

### Performance

- Filtrage pandas en mémoire : <100ms pour 30 comparables
- Réaffichage carte Folium : <500ms
- Mise à jour tableau : <100ms
- **Total : <1s (respecte critère d'acceptation)**

### Risques
- Filtres trop restrictifs → Aucun comparable → Message d'alerte
- Performance dégradée si >1000 comparables → Pagination ou lazy loading
- Valeurs par défaut inadaptées → A/B testing avec utilisateurs

---

**Lien EPIC parent:** [README.md](./README.md)
