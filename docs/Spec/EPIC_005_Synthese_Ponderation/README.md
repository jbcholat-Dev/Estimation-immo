# EPIC-005 : Onglet Synthèse et Pondération

**Story Points:** 13 SP
**Sprint:** 4
**Priorité:** Must Have
**User Stories:** 2

## Description

Consolider toutes les méthodes d'estimation (DVF+, Comparables vente, Additionnelle, Locative) en un onglet de synthèse final. L'utilisateur peut pondérer manuellement chaque méthode via des sliders pour obtenir une estimation finale personnalisée. Des visualisations avancées (radar chart, histogram, box plot) permettent d'analyser la cohérence des résultats. Export PDF du rapport d'estimation complet.

## Objectifs

- Afficher toutes les estimations des 4 méthodes
- Permettre la pondération manuelle via sliders (total = 100%)
- Calculer l'estimation finale pondérée en temps réel
- Visualiser les résultats avec graphiques interactifs :
  - Radar chart (4 méthodes)
  - Histogram de distribution des prix
  - Box plot de cohérence
- Afficher une fourchette de prix (min-max) et un score de confiance
- Générer un rapport PDF professionnel avec ReportLab
- Exporter les données au format CSV

## User Stories incluses

| ID | Titre | Story Points | Sprint | Priorité |
|----|-------|--------------|--------|----------|
| US-12 | Pondération | 7 SP | 4 | Must Have |
| US-13 | Synthèse graphique | 6 SP | 4 | Must Have |

## Dépendances

- Toutes les méthodes d'estimation (EPIC-001 à EPIC-004)
- Session state avec résultats des 4 méthodes
- Plotly pour visualisations
- ReportLab pour génération PDF
- Streamlit pour interface

## Liens

- [Voir les User Stories détaillées](./USER_STORIES.md)
- [CONTEXT_PROJET.md](../../CONTEXT_PROJET.md)
