# US-9 : Affichage comparables vente

**EPIC:** EPIC-002 - Onglet Comparables en Vente (Perplexity)
**Sprint:** 3
**Priorité:** Must Have
**Story Points:** 5 SP

## User Story

En tant qu'agent immobilier, je veux visualiser les comparables en vente sur une carte interactive avec filtres dynamiques, pour comparer les prix affichés avec mon estimation et détecter les opportunités de marché.

## Critères d'acceptation

- [ ] Les comparables en vente s'affichent sur une carte Folium
- [ ] Les filtres disponibles :
  - Prix (slider min-max)
  - Localité (multiselect)
  - Type de bien (multiselect)
  - Date de publication (slider jours)
- [ ] Au clic sur un marqueur, affichage :
  - Adresse
  - Prix affiché
  - Surface et prix/m²
  - Description courte
  - Lien vers annonce source (cliquable)
- [ ] Un tableau récapitulatif liste toutes les annonces
- [ ] Export CSV disponible (bouton "Télécharger CSV")
- [ ] Les marqueurs sont colorés selon fourchette de prix
- [ ] Le chargement est <2 secondes

## Notes techniques

### Dépendances
- Données Perplexity (US-8)
- Folium pour la carte
- pandas pour filtrage
- Streamlit pour interface

### Stack technique
- **Cartographie:** Folium
- **Filtrage:** pandas + Streamlit widgets
- **Export:** pandas.to_csv()
- **Affichage:** st.dataframe, st.download_button

### Estimation détaillée
- Intégration carte Folium : 2h
- Filtres dynamiques : 3h
- Popups avec détails : 2h
- Tableau récapitulatif : 2h
- Export CSV : 1h
- Tests et optimisation : 2h
- **Total : 12h (5 SP)**

### Implémentation carte

```python
import folium
from streamlit_folium import st_folium

# Filtres
col1, col2 = st.columns(2)
with col1:
    prix_range = st.slider("Fourchette de prix (€)", 0, 1000000, (100000, 500000), step=10000)
with col2:
    jours_max = st.slider("Publiées depuis (jours)", 1, 365, 30)

# Filtrage dataframe
df_filtered = df_vente[
    (df_vente['prix'] >= prix_range[0]) &
    (df_vente['prix'] <= prix_range[1]) &
    (df_vente['jours_publication'] <= jours_max)
]

# Carte
m = folium.Map(location=[46.2, 6.2], zoom_start=11)

for idx, row in df_filtered.iterrows():
    color = 'green' if row['prix'] < 300000 else 'orange' if row['prix'] < 500000 else 'red'

    popup_html = f"""
    <div style="font-family: Arial; min-width: 250px;">
        <h4>{row['adresse']}</h4>
        <p><b>Prix :</b> {row['prix']:,} €</p>
        <p><b>Surface :</b> {row['surface']} m²</p>
        <p><b>Prix/m² :</b> {row['prix']/row['surface']:.0f} €/m²</p>
        <p><b>Pièces :</b> {row['pieces']}</p>
        <p>{row['description'][:100]}...</p>
        <a href="{row['url_source']}" target="_blank">Voir l'annonce</a>
    </div>
    """

    folium.Marker(
        location=[row['lat'], row['lng']],
        popup=folium.Popup(popup_html, max_width=300),
        icon=folium.Icon(color=color, icon='home')
    ).add_to(m)

st_folium(m, width=800, height=600)
```

### Tableau récapitulatif

```python
st.subheader("Liste des annonces")
st.dataframe(
    df_filtered[['adresse', 'prix', 'surface', 'pieces', 'url_source']],
    column_config={
        "prix": st.column_config.NumberColumn("Prix", format="%.0f €"),
        "surface": st.column_config.NumberColumn("Surface", format="%.0f m²"),
        "url_source": st.column_config.LinkColumn("Annonce")
    }
)
```

### Export CSV

```python
csv = df_filtered.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Télécharger CSV",
    data=csv,
    file_name=f"comparables_vente_{ville}_{date.today()}.csv",
    mime="text/csv"
)
```

### Gradient de couleurs prix

- **Vert :** Prix < 300k€ (bon rapport qualité/prix)
- **Orange :** 300k€ ≤ Prix < 500k€ (moyenne marché)
- **Rouge :** Prix ≥ 500k€ (haut de gamme)

### Risques
- Coordonnées GPS manquantes → Géocodage via API Adresse Etalab
- Annonces obsolètes → Filtrer par date publication
- Trop d'annonces sur carte → Clustering Folium

---

**Lien EPIC parent:** [README.md](./README.md)
