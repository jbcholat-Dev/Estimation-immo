# Index des EPIC

**Synchronisé depuis Notion PRD** 
**Date** : 2025-11-21

---

## 📋 Vue d'Ensemble

| EPIC | Story Points | Sprint(s) | US Count | Priorité | Dossier |
|------|--------------|-----------|----------|----------|---------|
| EPIC 1 : Comparables DVF+ | 21 SP | 1-2 | 7 | Must Have | [EPIC_001](./EPIC_001_Comparables_DVF/) |
| EPIC 2 : Comparables Vente | 13 SP | 3 | 2 | Should Have | [EPIC_002](./EPIC_002_Comparables_Vente/) |
| EPIC 3 : Méthode Additionnelle | 8 SP | 4 | 1 | Should Have | [EPIC_003](./EPIC_003_Methode_Additionnelle/) |
| EPIC 4 : Méthode Locative | 5 SP | 4 | 1 | Should Have | [EPIC_004](./EPIC_004_Methode_Locative/) |
| EPIC 5 : Synthèse & Pondération | 13 SP | 5 | 2 | Should Have | [EPIC_005](./EPIC_005_Synthese_Ponderation/) |
| **TOTAL** | **60 SP** | 1-5 | **13** | - | - |

---

## Phase 1 : MVP (Sprints 1-3) - 45 SP

### EPIC 1 : Onglet Comparables Vendues (DVF+)

**📁 [Lire le dossier EPIC_001](./EPIC_001_Comparables_DVF/README.md)**

- **Story Points** : 21 SP
- **Sprint** : 1-2
- **User Stories** : 7
- **Priorité** : All Must Have
- **Description** : Analyser les transactions passées similaires au bien estimé via données DVF+. Calcul automatique score similarité, filtrage manuel, sélection checkbox, métriques calculées (médiane, prix/m², boxplot). Carte interactive avec Street View.

**User Stories :**
1. US-1 : Formulaire de saisie du bien à estimer (3 SP)
2. US-2 : Calcul similarité et affichage top 30 comparables DVF+ (5 SP)
3. US-3 : Carte interactive avec marqueurs colorés (3 SP)
4. US-4 : Street View au clic sur marqueur (2 SP)
5. US-5 : Filtres manuels (rayon, années, similarité) (3 SP)
6. US-6 : Sélection checkbox et calcul métriques (2 SP)
7. US-7 : Colonne prix ajusté pouvoir d'achat (3 SP)

---

### EPIC 2 : Onglet Comparables en Vente (Perplexity)

**📁 [Lire le dossier EPIC_002](./EPIC_002_Comparables_Vente/README.md)**

- **Story Points** : 13 SP
- **Sprint** : 3
- **User Stories** : 2
- **Priorité** : Should Have
- **Description** : Intégration API Perplexity pour récupérer annonces immobilières en vente. Affichage sur carte, filtrage, export.

**User Stories :**
1. US-8 : Intégration API Perplexity avec recherche par localité (8 SP)
2. US-9 : Affichage comparables vente sur carte + filtres (5 SP)

---

## Phase 2 : Complémentaires (Sprints 4-5) - 15 SP

### EPIC 3 : Onglet Méthode Additionnelle (Maisons)

**📁 [Lire le dossier EPIC_003](./EPIC_003_Methode_Additionnelle/README.md)**

- **Story Points** : 8 SP
- **Sprint** : 4
- **User Stories** : 1
- **Priorité** : Should Have
- **Description** : Calcul terrain + construction avec Perplexity pour maisons.

**User Stories :**
1. US-10 : Calcul Terrain + Construction (Perplexity) pour Maisons (8 SP)

---

### EPIC 4 : Onglet Méthode Locative (Appartements)

**📁 [Lire le dossier EPIC_004](./EPIC_004_Methode_Locative/README.md)**

- **Story Points** : 5 SP
- **Sprint** : 4
- **User Stories** : 1
- **Priorité** : Should Have
- **Description** : Calcul rendement locatif avec Perplexity pour appartements.

**User Stories :**
1. US-11 : Calcul Rendement Locatif (Perplexity) pour Appartements (5 SP)

---

### EPIC 5 : Onglet Synthèse et Pondération

**📁 [Lire le dossier EPIC_005](./EPIC_005_Synthese_Ponderation/README.md)**

- **Story Points** : 13 SP
- **Sprint** : 5
- **User Stories** : 2
- **Priorité** : Should Have
- **Description** : Pondération ajustable des 4 méthodes d'estimation, graphique comparatif, synthèse finale.

**User Stories :**
1. US-12 : Pondération ajustable des 4 méthodes d'estimation (7 SP)
2. US-13 : Synthèse graphique + comparaison (6 SP)

---

## 📊 Distribution par Priorité

### Must Have (Phase 1 MVP) - 21 SP
- EPIC 1 entier (7 US) : **21 SP**

### Should Have (Phase 2 + Perplexity) - 39 SP
- EPIC 2 : 13 SP (2 US)
- EPIC 3 : 8 SP (1 US)
- EPIC 4 : 5 SP (1 US)
- EPIC 5 : 13 SP (2 US)

---

## 📅 Timeline par Sprint

```
Sprint 1 (11 SP) ┐
                 ├─ Phase 1 MVP (45 SP)
Sprint 2 (10 SP) ┤ Comparables DVF+ + Perplexity annonces
Sprint 3 (13 SP) ┘

Sprint 4 (13 SP) ┐
                 └─ Phase 2 Extensions (15 SP)
Sprint 5 (13 SP)   Méthodes additionnelle/locative/synthèse
```

---

**Pour consulter une User Story en détail :**
1. Choisissez l'EPIC dans le tableau ci-dessus
2. Cliquez sur le lien dossier EPIC_XXX
3. Consultez le fichier US_XXX correspondant

**Exemple :**
- Dossier EPIC_001 → USER_STORIES.md → US_001_Formulaire.md
