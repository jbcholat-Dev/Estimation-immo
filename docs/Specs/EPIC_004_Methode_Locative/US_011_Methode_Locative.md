# US-11 : Méthode Locative

**EPIC:** EPIC-004 - Onglet Méthode Locative (Appartements)
**Sprint:** 3
**Priorité:** Should Have
**Story Points:** 5 SP

## User Story

En tant qu'agent immobilier, je veux estimer un appartement par la méthode locative (capitalisation du loyer), pour obtenir une estimation basée sur le rendement locatif et comparer avec les normes du marché local.

## Critères d'acceptation

- [ ] L'onglet n'est actif que pour les appartements
- [ ] Les champs de saisie incluent :
  - Loyer mensuel potentiel (€)
  - Charges annuelles copropriété (€)
  - Taxe foncière annuelle (€)
  - Autres frais annuels (€)
- [ ] Le calcul affiche :
  - Rendement brut (loyer annuel / estimation × 100)
  - Rendement net (loyer - charges / estimation × 100)
  - Estimation par capitalisation (loyer annuel / taux rendement zone)
- [ ] Le taux de rendement moyen de la zone est récupéré automatiquement
- [ ] Un indicateur visuel compare le rendement du bien avec la zone :
  - Vert : Supérieur à la moyenne (+0.5%)
  - Orange : Égal à la moyenne (±0.5%)
  - Rouge : Inférieur à la moyenne (-0.5%)
- [ ] Un graphique compare rendement brut vs net vs zone
- [ ] Un tooltip explique les formules de calcul

## Notes techniques

### Dépendances
- Formulaire de saisie avec champs appartements
- Données rendement moyen zone (API ou base locale)
- Streamlit pour interface
- Plotly pour graphique

### Stack technique
- **Interface:** Streamlit
- **Calculs:** Python, pandas
- **Visualisation:** Plotly (bar chart)
- **Données zone:** Perplexity ou Supabase

### Estimation détaillée
- Formules de calcul rendement : 2h
- Interface Streamlit : 2h
- Récupération taux zone : 2h
- Graphique comparatif : 2h
- Tests et validation : 2h
- **Total : 10h (5 SP)**

### Formules de calcul

```python
def calculer_methode_locative(
    loyer_mensuel: float,
    charges_annuelles: float,
    taxe_fonciere: float,
    autres_frais: float,
    taux_rendement_zone: float
) -> dict:
    """
    Calcule l'estimation par méthode locative.

    Returns:
        dict avec rendements, estimation, comparaison zone
    """
    # Loyer annuel
    loyer_annuel = loyer_mensuel * 12

    # Frais totaux annuels
    frais_totaux = charges_annuelles + taxe_fonciere + autres_frais

    # Loyer net annuel
    loyer_net_annuel = loyer_annuel - frais_totaux

    # Estimation par capitalisation (loyer / taux rendement)
    estimation_par_capitalisation = loyer_annuel / (taux_rendement_zone / 100)

    # Rendement brut
    rendement_brut = (loyer_annuel / estimation_par_capitalisation) * 100

    # Rendement net
    rendement_net = (loyer_net_annuel / estimation_par_capitalisation) * 100

    # Comparaison zone
    delta_zone = rendement_net - taux_rendement_zone
    if delta_zone > 0.5:
        indicateur = "Bon"
        couleur = "green"
    elif delta_zone < -0.5:
        indicateur = "Faible"
        couleur = "red"
    else:
        indicateur = "Moyen"
        couleur = "orange"

    return {
        "loyer_annuel": round(loyer_annuel, 0),
        "loyer_net_annuel": round(loyer_net_annuel, 0),
        "estimation_capitalisation": round(estimation_par_capitalisation, 0),
        "rendement_brut": round(rendement_brut, 2),
        "rendement_net": round(rendement_net, 2),
        "taux_zone": taux_rendement_zone,
        "indicateur": indicateur,
        "couleur": couleur,
        "delta_zone": round(delta_zone, 2)
    }
```

### Récupération taux rendement zone

```python
async def get_taux_rendement_zone(ville: str, code_postal: str) -> float:
    """
    Récupère le taux de rendement locatif moyen de la zone.
    """
    # Option 1 : Perplexity
    prompt = f"""
    Quel est le taux de rendement locatif moyen pour un appartement à {ville} ({code_postal}) en 2024 ?
    Retourne uniquement le taux en pourcentage (exemple: 4.5)
    """
    response = await call_perplexity_api(prompt)
    taux = float(extract_number(response))

    # Option 2 : Base locale (fallback)
    if not taux or taux < 2 or taux > 10:
        # Valeurs par défaut zone Chablais/Annemasse
        taux = 4.5

    return taux
```

### Interface Streamlit

```python
st.header("Méthode Locative (Appartements)")

col1, col2 = st.columns(2)
with col1:
    loyer_mensuel = st.number_input("Loyer mensuel potentiel (€)", min_value=0, value=1000)
    charges_annuelles = st.number_input("Charges copropriété annuelles (€)", min_value=0, value=1200)

with col2:
    taxe_fonciere = st.number_input("Taxe foncière annuelle (€)", min_value=0, value=800)
    autres_frais = st.number_input("Autres frais annuels (€)", min_value=0, value=500)

if st.button("Calculer estimation locative"):
    with st.spinner("Récupération taux zone..."):
        taux_zone = asyncio.run(get_taux_rendement_zone(ville, code_postal))

    result = calculer_methode_locative(
        loyer_mensuel,
        charges_annuelles,
        taxe_fonciere,
        autres_frais,
        taux_zone
    )

    # Affichage résultats
    col1, col2, col3 = st.columns(3)
    col1.metric("Rendement brut", f"{result['rendement_brut']:.2f}%")
    col2.metric("Rendement net", f"{result['rendement_net']:.2f}%")
    col3.metric(
        "Vs Zone",
        f"{result['delta_zone']:+.2f}%",
        delta=result['indicateur'],
        delta_color="normal" if result['couleur'] == 'green' else "inverse"
    )

    st.metric("Estimation par capitalisation", f"{result['estimation_capitalisation']:,.0f} €")

    # Graphique comparatif
    fig = go.Figure(data=[
        go.Bar(name='Rendement brut', x=['Rendement'], y=[result['rendement_brut']]),
        go.Bar(name='Rendement net', x=['Rendement'], y=[result['rendement_net']]),
        go.Bar(name='Taux zone', x=['Rendement'], y=[result['taux_zone']])
    ])
    fig.update_layout(title="Comparaison rendements")
    st.plotly_chart(fig)

    # Tooltip explicatif
    st.info(f"""
    **Formules utilisées :**
    - Rendement brut = (Loyer annuel / Prix) × 100
    - Rendement net = (Loyer - Charges / Prix) × 100
    - Estimation = Loyer annuel / (Taux zone / 100)

    **Taux zone Chablais/Annemasse :** {taux_zone}%
    """)
```

### Graphique comparatif

```python
import plotly.graph_objects as go

fig = go.Figure(data=[
    go.Bar(
        name='Rendements',
        x=['Brut', 'Net', 'Zone'],
        y=[result['rendement_brut'], result['rendement_net'], result['taux_zone']],
        marker_color=['lightblue', 'blue', 'orange']
    )
])
fig.update_layout(
    title="Analyse du rendement locatif",
    yaxis_title="Taux (%)",
    showlegend=False
)
st.plotly_chart(fig, use_container_width=True)
```

### Valeurs de référence Chablais/Annemasse

- **Taux moyen zone :** 4.0-5.0% (net)
- **Bon rendement :** > 5.0%
- **Rendement faible :** < 3.5%

### Risques
- Loyer surestimé → Validation avec annonces locales
- Frais sous-estimés → Checklist complète (travaux, assurance, etc.)
- Taux zone obsolète → Mise à jour trimestrielle

---

**Lien EPIC parent:** [README.md](./README.md)
