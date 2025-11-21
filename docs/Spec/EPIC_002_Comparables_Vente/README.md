# EPIC-002 : Onglet Comparables en Vente (Perplexity)

**Story Points:** 13 SP
**Sprint:** 2-3
**Priorité:** Must Have
**User Stories:** 2

## Description

Récupérer et afficher les biens actuellement en vente via l'API Perplexity pour compléter l'estimation avec les prix du marché actif. L'utilisateur peut filtrer par localité, code postal et fourchette de prix. Les comparables en vente sont affichés dans un tableau avec sources URL et sur une carte interactive. Export CSV disponible.

## Objectifs

- Intégrer l'API Perplexity pour récupérer les annonces immobilières en vente
- Filtrer les annonces par localité, code postal et prix
- Afficher les comparables en vente dans un tableau structuré avec sources
- Visualiser les annonces sur une carte interactive
- Permettre l'export des données au format CSV
- Compléter l'estimation DVF+ avec les prix du marché actif

## User Stories incluses

| ID | Titre | Story Points | Sprint | Priorité |
|----|-------|--------------|--------|----------|
| US-8 | Perplexity Integration | 8 SP | 2-3 | Must Have |
| US-9 | Affichage comparables vente | 5 SP | 3 | Must Have |

## Dépendances

- API Perplexity (clé API requise)
- Module de géocodage (utils/geocoding.py)
- Folium pour la carte interactive
- pandas pour manipulation des données
- Streamlit pour l'interface

## Liens

- [Voir les User Stories détaillées](./USER_STORIES.md)
- [Documentation API Perplexity](https://docs.perplexity.ai/)
- [CONTEXT_PROJET.md](../../CONTEXT_PROJET.md)
