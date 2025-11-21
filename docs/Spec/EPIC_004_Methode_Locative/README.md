# EPIC-004 : Onglet Méthode Locative (Appartements)

**Story Points:** 5 SP
**Sprint:** 3
**Priorité:** Should Have
**User Stories:** 1

## Description

Appliquer la méthode locative d'estimation pour les appartements, qui calcule la valeur du bien en fonction du rendement locatif. Cette méthode capitalise le loyer annuel en utilisant un taux de rendement de référence pour la zone Chablais/Annemasse.

## Objectifs

- Calculer le rendement locatif brut (loyer annuel / prix)
- Calculer le rendement locatif net (loyer - charges / prix)
- Comparer avec le rendement moyen de la zone
- Estimer la valeur du bien par capitalisation du loyer
- Intégrer les frais annuels (charges copropriété, taxe foncière, etc.)
- Afficher un indicateur de rentabilité (bon/moyen/faible)

## User Stories incluses

| ID | Titre | Story Points | Sprint | Priorité |
|----|-------|--------------|--------|----------|
| US-11 | Méthode Locative | 5 SP | 3 | Should Have |

## Dépendances

- Formulaire de saisie (US-1) avec champs spécifiques appartements
- Données de rendement moyen zone (Perplexity ou base locale)
- Module de calcul rendement locatif

## Liens

- [Voir les User Stories détaillées](./USER_STORIES.md)
- [CONTEXT_PROJET.md](../../CONTEXT_PROJET.md)
