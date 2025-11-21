# EPIC-003 : Onglet Méthode Additionnelle (Maisons)

**Story Points:** 8 SP
**Sprint:** 3
**Priorité:** Should Have
**User Stories:** 1

## Description

Appliquer la méthode additionnelle d'estimation pour les maisons, qui calcule séparément la valeur du terrain et de la construction. Cette méthode utilise les prix au m² du terrain et de la construction récupérés via Perplexity, ajustés selon l'année de construction et le niveau de finition.

## Objectifs

- Calculer la valeur du terrain (surface × prix/m² terrain local)
- Calculer la valeur de la construction (surface × prix/m² construction selon année et finition)
- Récupérer les prix/m² via Perplexity (données locales Chablais/Annemasse)
- Permettre l'ajustement manuel des coefficients de vétusté et finition
- Afficher le résultat de l'estimation additionnelle
- Intégrer le résultat dans la synthèse finale (EPIC-005)

## User Stories incluses

| ID | Titre | Story Points | Sprint | Priorité |
|----|-------|--------------|--------|----------|
| US-10 | Méthode Additionnelle | 8 SP | 3 | Should Have |

## Dépendances

- API Perplexity pour récupération prix/m² locaux
- Formulaire de saisie (US-1) avec champs spécifiques maisons
- Coefficients de vétusté (selon année construction)
- Coefficients de finition (basique, standard, haut de gamme)

## Liens

- [Voir les User Stories détaillées](./USER_STORIES.md)
- [CONTEXT_PROJET.md](../../CONTEXT_PROJET.md)
