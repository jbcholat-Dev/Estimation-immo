# EPIC-001 : Onglet Comparables Vendues (DVF+)

**Story Points:** 21 SP
**Sprint:** 1-2
**Priorité:** Must Have
**User Stories:** 7

## Description

Analyser les transactions passées similaires au bien estimé via les données DVF+ (Demandes de Valeurs Foncières). L'utilisateur saisit les caractéristiques du bien, le système calcule automatiquement un score de similarité avec les transactions historiques, permet un filtrage manuel, une sélection par checkbox, et affiche des métriques calculées (médiane, prix/m², boxplot). Une carte interactive avec intégration Street View permet la visualisation géographique des comparables.

## Objectifs

- Permettre la saisie complète des caractéristiques d'un bien immobilier
- Calculer automatiquement la similarité avec les transactions DVF+ (56,216 mutations disponibles)
- Afficher les comparables sur une carte interactive avec Street View
- Permettre le filtrage manuel et la sélection des comparables pertinents
- Calculer les métriques statistiques (médiane, prix/m², boxplot)
- Intégrer les prix ajustés selon les taux d'emprunt historiques

## User Stories incluses

| ID | Titre | Story Points | Sprint | Priorité |
|----|-------|--------------|--------|----------|
| US-1 | Formulaire de saisie | 3 SP | 1 | Must Have |
| US-2 | Calcul similarité | 5 SP | 1 | Must Have |
| US-3 | Carte interactive | 3 SP | 1 | Must Have |
| US-4 | Street View | 2 SP | 1-2 | Should Have |
| US-5 | Filtres manuels | 3 SP | 2 | Must Have |
| US-6 | Sélection & métriques | 2 SP | 2 | Must Have |
| US-7 | Prix ajusté | 3 SP | 2 | Should Have |

## Dépendances

- Base de données Supabase avec données DVF+ (56,216 mutations)
- API Adresse Etalab pour le géocodage
- Google Maps API pour Street View
- Bibliothèques: Streamlit, Folium, Plotly, pandas
- Algorithme de scoring multi-critères (src/estimation_algorithm.py)

## Liens

- [Voir les User Stories détaillées](./USER_STORIES.md)
- [CONTEXT_PROJET.md](../../CONTEXT_PROJET.md)
- [PLAN_MVP_IMPLEMENTATION.md](../../PLAN_MVP_IMPLEMENTATION.md)
