# US-6 : Sélection & métriques

**EPIC:** EPIC-001 - Onglet Comparables Vendues (DVF+)
**Sprint:** 2
**Priorité:** Must Have
**Story Points:** 2 SP

## User Story

En tant qu'agent immobilier, je veux sélectionner manuellement 5 à 7 comparables pertinents via checkbox, pour calculer automatiquement les métriques statistiques (médiane, prix/m², boxplot) et affiner mon estimation.

## Critères d'acceptation

- [ ] Chaque ligne du tableau possède une checkbox
- [ ] La sélection multiple est possible (5-7 biens recommandés)
- [ ] Le calcul des métriques se fait en temps réel :
  - Prix médian
  - Prix/m² médian
  - Prix minimum et maximum
  - Écart-type
- [ ] Un boxplot Plotly s'affiche avec la distribution des prix
- [ ] Un message d'erreur s'affiche si moins de 3 biens sélectionnés
- [ ] Les métriques sont stockées dans le session state
- [ ] Un bouton "Tout sélectionner" / "Tout désélectionner" est disponible

## Notes techniques

### Dépendances
- Streamlit (st.checkbox, st.dataframe)
- pandas (calculs statistiques)
- Plotly (graphique boxplot)
- Session state pour persistance

### Stack technique
- **Frontend:** Streamlit (dataframe avec checkboxes)
- **Calculs:** pandas (median, std, min, max)
- **Visualisation:** Plotly Express (box plot)

### Estimation détaillée
- Intégration checkboxes dans tableau : 1h
- Calculs métriques temps réel : 2h
- Graphique boxplot Plotly : 2h
- Validation sélection (min 3 biens) : 1h
- Tests et optimisation : 1h
- **Total : 7h (2 SP)**

### Implémentation

```python
# Dataframe avec checkboxes
selected_comparables = []
for idx, row in df_filtered.iterrows():
    if st.checkbox(f"", key=f"select_{idx}"):
        selected_comparables.append(row)

df_selected = pd.DataFrame(selected_comparables)

# Validation
if len(df_selected) < 3:
    st.warning("Sélectionnez au moins 3 comparables pour un calcul fiable")
elif len(df_selected) > 10:
    st.info("Plus de 10 comparables sélectionnés. Recommandation : 5-7 pour équilibre précision/pertinence")

# Calcul métriques
if len(df_selected) >= 3:
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Prix médian", f"{df_selected['prix'].median():,.0f} €")
    col2.metric("Prix/m² médian", f"{(df_selected['prix'] / df_selected['surface']).median():.0f} €/m²")
    col3.metric("Prix min", f"{df_selected['prix'].min():,.0f} €")
    col4.metric("Prix max", f"{df_selected['prix'].max():,.0f} €")

    # Boxplot
    fig = px.box(df_selected, y='prix', title="Distribution des prix des comparables sélectionnés")
    st.plotly_chart(fig, use_container_width=True)
```

### Métriques calculées

- **Prix médian :** Valeur centrale (robuste aux outliers)
- **Prix/m² médian :** Normalisation par surface
- **Prix min/max :** Fourchette de prix
- **Écart-type :** Mesure de dispersion
- **Boxplot :** Visualisation quartiles + outliers

### Risques
- Sélection biaisée par l'utilisateur → Recommandation 5-7 biens + warning
- Outliers faussent la moyenne → Utiliser médiane (plus robuste)
- Performance dégradée si >50 checkboxes → Pagination du tableau

---

**Lien EPIC parent:** [README.md](./README.md)
