# US-10 : Méthode Additionnelle

**EPIC:** EPIC-003 - Onglet Méthode Additionnelle (Maisons)
**Sprint:** 3
**Priorité:** Should Have
**Story Points:** 8 SP

## User Story

En tant qu'agent immobilier, je veux estimer une maison par la méthode additionnelle (Terrain + Construction), pour obtenir une estimation complémentaire basée sur les composantes physiques du bien.

## Critères d'acceptation

- [ ] L'onglet n'est actif que pour les maisons
- [ ] Les champs de saisie incluent :
  - Surface terrain (m²)
  - Année de construction
  - Niveau de finition (Basique, Standard, Haut de gamme)
- [ ] Les prix/m² sont récupérés via Perplexity :
  - Prix/m² terrain local
  - Prix/m² construction selon finition
- [ ] Le calcul applique les formules :
  - Valeur terrain = Surface terrain × Prix/m² terrain
  - Valeur construction = Surface habitable × Prix/m² construction × Coefficient vétusté × Coefficient finition
  - Estimation totale = Valeur terrain + Valeur construction
- [ ] Un tableau récapitulatif affiche :
  - Valeur terrain
  - Valeur construction
  - Coefficients appliqués
  - Estimation totale
- [ ] Les coefficients sont ajustables manuellement
- [ ] Un graphique en barres empilées visualise les composantes

## Notes techniques

### Dépendances
- API Perplexity (récupération prix/m² locaux)
- Formulaire de saisie avec champs maisons
- Streamlit pour interface
- Plotly pour graphique

### Stack technique
- **API:** Perplexity
- **Calculs:** pandas, numpy
- **Visualisation:** Plotly (stacked bar chart)
- **Interface:** Streamlit

### Estimation détaillée
- Intégration Perplexity prix/m² : 4h
- Calcul méthode additionnelle : 3h
- Coefficients vétusté/finition : 2h
- Interface Streamlit : 3h
- Graphique Plotly : 2h
- Tests et validation : 3h
- **Total : 17h (8 SP)**

### Formule détaillée

```python
def calculer_methode_additionnelle(
    surface_terrain: float,
    surface_habitable: float,
    annee_construction: int,
    niveau_finition: str,
    prix_m2_terrain: float,
    prix_m2_construction_base: float
) -> dict:
    """
    Calcule l'estimation par méthode additionnelle.

    Returns:
        dict avec valeur_terrain, valeur_construction, estimation_totale
    """
    # Valeur terrain
    valeur_terrain = surface_terrain * prix_m2_terrain

    # Coefficient vétusté
    age_bien = 2024 - annee_construction
    if age_bien < 5:
        coef_vetuste = 1.0
    elif age_bien < 10:
        coef_vetuste = 0.95
    elif age_bien < 20:
        coef_vetuste = 0.85
    elif age_bien < 30:
        coef_vetuste = 0.75
    else:
        coef_vetuste = 0.65

    # Coefficient finition
    coef_finition = {
        "Basique": 0.85,
        "Standard": 1.0,
        "Haut de gamme": 1.20
    }[niveau_finition]

    # Valeur construction
    prix_m2_construction = prix_m2_construction_base * coef_vetuste * coef_finition
    valeur_construction = surface_habitable * prix_m2_construction

    # Estimation totale
    estimation_totale = valeur_terrain + valeur_construction

    return {
        "valeur_terrain": round(valeur_terrain, 0),
        "valeur_construction": round(valeur_construction, 0),
        "estimation_totale": round(estimation_totale, 0),
        "coef_vetuste": coef_vetuste,
        "coef_finition": coef_finition,
        "prix_m2_construction_final": round(prix_m2_construction, 0)
    }
```

### Récupération prix/m² via Perplexity

```python
async def get_prix_m2_locaux(ville: str, code_postal: str) -> dict:
    """
    Récupère les prix/m² locaux via Perplexity.
    """
    prompt = f"""
    Donne les prix moyens au m² pour {ville} ({code_postal}) en 2024 :
    1. Prix/m² terrain constructible
    2. Prix/m² construction maison neuve (standard)

    Retourne au format JSON :
    {{
        "prix_m2_terrain": 250,
        "prix_m2_construction": 1800
    }}
    """

    response = await call_perplexity_api(prompt)
    return parse_json_response(response)
```

### Coefficients de vétusté

| Âge du bien | Coefficient |
|-------------|-------------|
| < 5 ans | 1.00 |
| 5-10 ans | 0.95 |
| 10-20 ans | 0.85 |
| 20-30 ans | 0.75 |
| > 30 ans | 0.65 |

### Coefficients de finition

| Niveau | Coefficient |
|--------|-------------|
| Basique | 0.85 |
| Standard | 1.00 |
| Haut de gamme | 1.20 |

### Interface Streamlit

```python
st.header("Méthode Additionnelle (Maisons)")

col1, col2 = st.columns(2)
with col1:
    surface_terrain = st.number_input("Surface terrain (m²)", min_value=0, value=500)
    annee_construction = st.number_input("Année construction", min_value=1900, max_value=2024, value=2000)

with col2:
    niveau_finition = st.selectbox("Niveau de finition", ["Basique", "Standard", "Haut de gamme"])
    surface_habitable = st.session_state.get('surface_habitable', 100)

# Récupération prix/m² locaux
if st.button("Calculer estimation"):
    with st.spinner("Récupération prix/m² locaux..."):
        prix_locaux = asyncio.run(get_prix_m2_locaux(ville, code_postal))

    result = calculer_methode_additionnelle(
        surface_terrain,
        surface_habitable,
        annee_construction,
        niveau_finition,
        prix_locaux['prix_m2_terrain'],
        prix_locaux['prix_m2_construction']
    )

    # Affichage résultats
    col1, col2, col3 = st.columns(3)
    col1.metric("Valeur terrain", f"{result['valeur_terrain']:,.0f} €")
    col2.metric("Valeur construction", f"{result['valeur_construction']:,.0f} €")
    col3.metric("Estimation totale", f"{result['estimation_totale']:,.0f} €")

    # Graphique
    fig = go.Figure(data=[
        go.Bar(name='Terrain', x=['Estimation'], y=[result['valeur_terrain']]),
        go.Bar(name='Construction', x=['Estimation'], y=[result['valeur_construction']])
    ])
    fig.update_layout(barmode='stack', title="Décomposition de l'estimation")
    st.plotly_chart(fig)
```

### Risques
- Prix/m² Perplexity imprécis → Validation avec données locales
- Coefficients trop simplistes → Ajustement avec expert
- Méthode non adaptée appartements → Désactiver pour appartements

---

**Lien EPIC parent:** [README.md](./README.md)
