# US-13 : Synthèse graphique

**EPIC:** EPIC-005 - Onglet Synthèse et Pondération
**Sprint:** 4
**Priorité:** Must Have
**Story Points:** 6 SP

## User Story

En tant qu'agent immobilier, je veux visualiser graphiquement la cohérence des différentes méthodes d'estimation et exporter un rapport PDF professionnel, pour présenter l'estimation à mes clients avec confiance.

## Critères d'acceptation

- [ ] Un radar chart affiche les 4 méthodes d'estimation
- [ ] Un histogram montre la distribution des prix des comparables
- [ ] Un box plot visualise la cohérence et les outliers
- [ ] Une fourchette de prix finale est affichée (min-max)
- [ ] Un score de confiance (0-100%) est calculé basé sur :
  - Écart-type des méthodes (<15% = bon)
  - Nombre de comparables (>5 = bon)
  - Cohérence DVF+ vs Vente (<10% écart = bon)
- [ ] Un bouton "Générer PDF" crée un rapport professionnel avec :
  - En-tête avec logo et infos bien
  - Résumé estimation finale
  - Graphiques (radar, histogram, box plot)
  - Tableau comparables sélectionnés
  - Méthodologie et sources
  - Footer avec date et signature agent
- [ ] Le PDF se télécharge automatiquement
- [ ] Un export CSV des données brutes est disponible

## Notes techniques

### Dépendances
- Résultats des 4 méthodes (US-1 à US-11)
- Plotly pour graphiques interactifs
- ReportLab pour génération PDF
- pandas pour export CSV

### Stack technique
- **Visualisation:** Plotly Express
- **PDF:** ReportLab
- **Export:** pandas.to_csv()
- **Interface:** Streamlit

### Estimation détaillée
- Radar chart : 2h
- Histogram et box plot : 2h
- Calcul score de confiance : 2h
- Génération PDF ReportLab : 6h
- Export CSV : 1h
- Tests et optimisation : 3h
- **Total : 16h (6 SP)**

### Radar chart

```python
import plotly.graph_objects as go

def create_radar_chart(estimations: dict) -> go.Figure:
    """
    Crée un radar chart des 4 méthodes d'estimation.
    """
    categories = ['DVF+', 'Comparables Vente', 'Additionnelle', 'Expertise']
    values = [
        estimations['dvf'],
        estimations['vente'],
        estimations['additionnelle'],
        estimations['expertise']
    ]

    # Normalisation 0-100 (par rapport au max)
    max_val = max(values)
    values_norm = [v / max_val * 100 for v in values]

    fig = go.Figure(data=go.Scatterpolar(
        r=values_norm,
        theta=categories,
        fill='toself',
        name='Estimation'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        title="Comparaison des méthodes d'estimation"
    )

    return fig

# Affichage
st.plotly_chart(create_radar_chart(estimations), use_container_width=True)
```

### Histogram et Box plot

```python
import plotly.express as px

# Histogram distribution prix comparables DVF+
fig_hist = px.histogram(
    df_comparables,
    x='prix',
    nbins=20,
    title="Distribution des prix des comparables DVF+",
    labels={'prix': 'Prix (€)', 'count': 'Nombre de biens'}
)
fig_hist.add_vline(
    x=estimation_finale,
    line_dash="dash",
    line_color="red",
    annotation_text="Estimation finale"
)
st.plotly_chart(fig_hist, use_container_width=True)

# Box plot cohérence
all_estimations = [
    {'methode': 'DVF+', 'prix': estimation_dvf},
    {'methode': 'Vente', 'prix': estimation_vente},
    {'methode': 'Additionnelle', 'prix': estimation_additionnelle},
    {'methode': 'Finale', 'prix': estimation_finale}
]
df_box = pd.DataFrame(all_estimations)

fig_box = px.box(
    df_box,
    x='methode',
    y='prix',
    title="Cohérence des estimations",
    labels={'prix': 'Prix (€)', 'methode': 'Méthode'}
)
st.plotly_chart(fig_box, use_container_width=True)
```

### Calcul score de confiance

```python
def calculer_score_confiance(
    estimations: list,
    nb_comparables: int,
    ecart_dvf_vente: float
) -> dict:
    """
    Calcule un score de confiance 0-100%.

    Critères :
    - Écart-type des estimations (<15% = bon)
    - Nombre de comparables (>5 = bon)
    - Cohérence DVF+ vs Vente (<10% écart = bon)
    """
    # Écart-type des estimations
    mean_estimation = np.mean(estimations)
    std_estimation = np.std(estimations)
    coef_variation = (std_estimation / mean_estimation) * 100

    score_coherence = max(0, 100 - (coef_variation * 5))  # Max 100, -5 pts par % d'écart

    # Nombre de comparables
    score_comparables = min(100, (nb_comparables / 7) * 100)  # 7 comparables = 100%

    # Cohérence DVF+ vs Vente
    score_dvf_vente = max(0, 100 - (abs(ecart_dvf_vente) * 5))  # -5 pts par % d'écart

    # Score final pondéré
    score_final = (
        score_coherence * 0.5 +
        score_comparables * 0.25 +
        score_dvf_vente * 0.25
    )

    niveau = "Élevé" if score_final >= 80 else "Moyen" if score_final >= 60 else "Faible"

    return {
        "score": round(score_final, 0),
        "niveau": niveau,
        "details": {
            "coherence": round(score_coherence, 0),
            "comparables": round(score_comparables, 0),
            "dvf_vente": round(score_dvf_vente, 0)
        }
    }
```

### Génération PDF avec ReportLab

```python
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors
from datetime import date

def generer_rapport_pdf(
    estimation_data: dict,
    comparables_df: pd.DataFrame,
    agent_name: str,
    output_path: str
) -> str:
    """
    Génère un rapport PDF professionnel d'estimation immobilière.
    """
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    story = []
    styles = getSampleStyleSheet()

    # En-tête
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1E3A8A'),
        spaceAfter=30
    )
    story.append(Paragraph("RAPPORT D'ESTIMATION IMMOBILIÈRE", title_style))
    story.append(Spacer(1, 0.5*cm))

    # Informations bien
    bien_info = f"""
    <b>Adresse :</b> {estimation_data['adresse']}<br/>
    <b>Type :</b> {estimation_data['type_bien']}<br/>
    <b>Surface :</b> {estimation_data['surface']} m²<br/>
    <b>Pièces :</b> {estimation_data['pieces']}<br/>
    <b>Date :</b> {date.today().strftime('%d/%m/%Y')}
    """
    story.append(Paragraph(bien_info, styles['Normal']))
    story.append(Spacer(1, 1*cm))

    # Estimation finale
    story.append(Paragraph("ESTIMATION FINALE", styles['Heading2']))
    estimation_text = f"""
    <font size=18 color='#1E3A8A'><b>{estimation_data['estimation_finale']:,.0f} €</b></font><br/>
    <b>Fourchette :</b> {estimation_data['fourchette_min']:,.0f} € - {estimation_data['fourchette_max']:,.0f} €<br/>
    <b>Score de confiance :</b> {estimation_data['score_confiance']}% ({estimation_data['niveau_confiance']})
    """
    story.append(Paragraph(estimation_text, styles['Normal']))
    story.append(Spacer(1, 1*cm))

    # Graphiques (sauvegarder en images temporaires)
    # Note : Plotly charts doivent être exportés en images
    # fig.write_image("temp_radar.png")
    # story.append(Image("temp_radar.png", width=15*cm, height=10*cm))

    # Tableau comparables
    story.append(Paragraph("COMPARABLES SÉLECTIONNÉS", styles['Heading2']))
    story.append(Spacer(1, 0.5*cm))

    table_data = [['Adresse', 'Prix', 'Surface', 'Prix/m²', 'Score']]
    for _, row in comparables_df.head(7).iterrows():
        table_data.append([
            row['adresse'][:30],
            f"{row['prix']:,.0f} €",
            f"{row['surface']} m²",
            f"{row['prix']/row['surface']:.0f} €/m²",
            f"{row['score']}%"
        ])

    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A8A')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(table)
    story.append(Spacer(1, 1*cm))

    # Méthodologie
    story.append(Paragraph("MÉTHODOLOGIE", styles['Heading2']))
    methodologie = """
    Cette estimation a été réalisée en combinant 4 méthodes complémentaires :<br/>
    <b>1. DVF+ (40%) :</b> Analyse des transactions passées similaires<br/>
    <b>2. Comparables en vente (25%) :</b> Analyse des biens actuellement en vente<br/>
    <b>3. Méthode additionnelle (20%) :</b> Valeur terrain + construction<br/>
    <b>4. Expertise agent (15%) :</b> Ajustements basés sur la connaissance du marché local
    """
    story.append(Paragraph(methodologie, styles['Normal']))

    # Footer
    story.append(Spacer(1, 2*cm))
    footer_text = f"""
    <i>Rapport généré le {date.today().strftime('%d/%m/%Y')}<br/>
    Agent : {agent_name}<br/>
    Estimateur Immobilier MVP - Chablais/Annemasse</i>
    """
    story.append(Paragraph(footer_text, styles['Normal']))

    # Construction PDF
    doc.build(story)
    return output_path
```

### Interface Streamlit

```python
st.subheader("Visualisations")

# Radar chart
st.plotly_chart(create_radar_chart(estimations), use_container_width=True)

# Histogram et box plot
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig_hist, use_container_width=True)
with col2:
    st.plotly_chart(fig_box, use_container_width=True)

# Score de confiance
confiance = calculer_score_confiance(
    [estimation_dvf, estimation_vente, estimation_additionnelle],
    len(df_comparables_selected),
    abs(estimation_dvf - estimation_vente) / estimation_dvf * 100
)

col1, col2, col3 = st.columns(3)
col1.metric("Score de confiance", f"{confiance['score']:.0f}%")
col2.metric("Niveau", confiance['niveau'])
col3.metric("Comparables", len(df_comparables_selected))

# Export
st.divider()
col1, col2 = st.columns(2)

with col1:
    if st.button("Générer PDF", type="primary"):
        with st.spinner("Génération du rapport PDF..."):
            pdf_path = generer_rapport_pdf(
                estimation_data,
                df_comparables_selected,
                "Agent Immobilier",
                "rapport_estimation.pdf"
            )
        with open(pdf_path, "rb") as f:
            st.download_button(
                label="Télécharger PDF",
                data=f,
                file_name=f"estimation_{adresse}_{date.today()}.pdf",
                mime="application/pdf"
            )

with col2:
    csv = df_comparables_selected.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Télécharger CSV",
        data=csv,
        file_name=f"comparables_{adresse}_{date.today()}.csv",
        mime="text/csv"
    )
```

### Risques
- Génération PDF lente → Optimisation images + cache
- Graphiques non exportables → Conversion Plotly → PNG
- PDF trop volumineux → Compression images

---

**Lien EPIC parent:** [README.md](./README.md)
