# Index Complet - EPICs & User Stories

## Vue d'ensemble

Ce document indexe la structure complète des spécifications fonctionnelles de l'Estimateur Immobilier MVP pour la zone Chablais/Annemasse (74). L'application est structurée en 5 EPICs couvrant l'ensemble du parcours utilisateur, de la saisie du bien à l'export du rapport d'estimation.

**Total :** 5 EPICs | 13 User Stories | 60 Story Points | 4 Sprints

---

## EPIC-001 : Comparables Vendues (DVF+)

**📁 Path:** `docs/Spec/EPIC_001_Comparables_DVF/`
**Story Points:** 21 SP | **Sprint:** 1-2 | **Priorité:** Must Have

### Description
Analyser les transactions passées similaires au bien estimé via les données DVF+ (56,216 mutations). Calcul automatique score similarité, filtrage manuel, sélection checkbox, métriques calculées (médiane, prix/m², boxplot). Carte interactive avec Street View.

### Fichiers
- [README.md](./EPIC_001_Comparables_DVF/README.md)
- [USER_STORIES.md](./EPIC_001_Comparables_DVF/USER_STORIES.md)

### User Stories (7)

| ID | Fichier | Titre | SP | Sprint | Priorité |
|----|---------|-------|----|----|----------|
| US-1 | [US_001_Formulaire_Saisie.md](./EPIC_001_Comparables_DVF/US_001_Formulaire_Saisie.md) | Formulaire de saisie | 3 | 1 | Must Have |
| US-2 | [US_002_Calcul_Similarite.md](./EPIC_001_Comparables_DVF/US_002_Calcul_Similarite.md) | Calcul similarité | 5 | 1 | Must Have |
| US-3 | [US_003_Carte_Interactive.md](./EPIC_001_Comparables_DVF/US_003_Carte_Interactive.md) | Carte interactive | 3 | 1 | Must Have |
| US-4 | [US_004_Street_View.md](./EPIC_001_Comparables_DVF/US_004_Street_View.md) | Street View | 2 | 1-2 | Should Have |
| US-5 | [US_005_Filtres_Manuels.md](./EPIC_001_Comparables_DVF/US_005_Filtres_Manuels.md) | Filtres manuels | 3 | 2 | Must Have |
| US-6 | [US_006_Selection_Metriques.md](./EPIC_001_Comparables_DVF/US_006_Selection_Metriques.md) | Sélection & métriques | 2 | 2 | Must Have |
| US-7 | [US_007_Prix_Ajuste.md](./EPIC_001_Comparables_DVF/US_007_Prix_Ajuste.md) | Prix ajusté | 3 | 2 | Should Have |

**Dépendances:** Supabase (DVF+), API Adresse Etalab, Google Maps API, Folium, Plotly

---

## EPIC-002 : Comparables en Vente (Perplexity)

**📁 Path:** `docs/Spec/EPIC_002_Comparables_Vente/`
**Story Points:** 13 SP | **Sprint:** 2-3 | **Priorité:** Must Have

### Description
Récupérer et afficher les biens actuellement en vente via l'API Perplexity. Filtrage par localité, code postal et prix. Affichage sur carte + tableau avec sources URL. Export CSV disponible.

### Fichiers
- [README.md](./EPIC_002_Comparables_Vente/README.md)
- [USER_STORIES.md](./EPIC_002_Comparables_Vente/USER_STORIES.md)

### User Stories (2)

| ID | Fichier | Titre | SP | Sprint | Priorité |
|----|---------|-------|----|----|----------|
| US-8 | [US_008_Perplexity_Integration.md](./EPIC_002_Comparables_Vente/US_008_Perplexity_Integration.md) | Perplexity Integration | 8 | 2-3 | Must Have |
| US-9 | [US_009_Affichage_Comparables_Vente.md](./EPIC_002_Comparables_Vente/US_009_Affichage_Comparables_Vente.md) | Affichage comparables vente | 5 | 3 | Must Have |

**Dépendances:** API Perplexity, Folium, pandas, Streamlit

---

## EPIC-003 : Méthode Additionnelle (Maisons)

**📁 Path:** `docs/Spec/EPIC_003_Methode_Additionnelle/`
**Story Points:** 8 SP | **Sprint:** 3 | **Priorité:** Should Have

### Description
Appliquer la méthode additionnelle d'estimation pour les maisons (Terrain + Construction). Calcul basé sur prix/m² terrain et construction récupérés via Perplexity, ajustés selon année de construction et finition.

### Fichiers
- [README.md](./EPIC_003_Methode_Additionnelle/README.md)
- [USER_STORIES.md](./EPIC_003_Methode_Additionnelle/USER_STORIES.md)

### User Stories (1)

| ID | Fichier | Titre | SP | Sprint | Priorité |
|----|---------|-------|----|----|----------|
| US-10 | [US_010_Methode_Additionnelle.md](./EPIC_003_Methode_Additionnelle/US_010_Methode_Additionnelle.md) | Méthode Additionnelle | 8 | 3 | Should Have |

**Dépendances:** API Perplexity (prix/m²), Plotly, Streamlit

---

## EPIC-004 : Méthode Locative (Appartements)

**📁 Path:** `docs/Spec/EPIC_004_Methode_Locative/`
**Story Points:** 5 SP | **Sprint:** 3 | **Priorité:** Should Have

### Description
Appliquer la méthode locative d'estimation pour les appartements (capitalisation du loyer). Calcul rendement brut/net, comparaison avec taux zone, estimation par capitalisation.

### Fichiers
- [README.md](./EPIC_004_Methode_Locative/README.md)
- [USER_STORIES.md](./EPIC_004_Methode_Locative/USER_STORIES.md)

### User Stories (1)

| ID | Fichier | Titre | SP | Sprint | Priorité |
|----|---------|-------|----|----|----------|
| US-11 | [US_011_Methode_Locative.md](./EPIC_004_Methode_Locative/US_011_Methode_Locative.md) | Méthode Locative | 5 | 3 | Should Have |

**Dépendances:** API Perplexity (taux zone), Plotly, Streamlit

---

## EPIC-005 : Synthèse et Pondération

**📁 Path:** `docs/Spec/EPIC_005_Synthese_Ponderation/`
**Story Points:** 13 SP | **Sprint:** 4 | **Priorité:** Must Have

### Description
Consolider toutes les méthodes d'estimation avec pondération manuelle. Visualisations avancées (radar chart, histogram, box plot). Score de confiance. Export PDF professionnel avec ReportLab.

### Fichiers
- [README.md](./EPIC_005_Synthese_Ponderation/README.md)
- [USER_STORIES.md](./EPIC_005_Synthese_Ponderation/USER_STORIES.md)

### User Stories (2)

| ID | Fichier | Titre | SP | Sprint | Priorité |
|----|---------|-------|----|----|----------|
| US-12 | [US_012_Ponderation.md](./EPIC_005_Synthese_Ponderation/US_012_Ponderation.md) | Pondération | 7 | 4 | Must Have |
| US-13 | [US_013_Synthese_Graphique.md](./EPIC_005_Synthese_Ponderation/US_013_Synthese_Graphique.md) | Synthèse graphique | 6 | 4 | Must Have |

**Dépendances:** Plotly, ReportLab, pandas, Streamlit, tous les EPICs précédents

---

## Planification Sprint Détaillée

### Sprint 1 (11 SP) - Fondations DVF+
**Objectif :** Mise en place du cœur de l'estimation via DVF+

- US-1 : Formulaire de saisie (3 SP)
  - Champs obligatoires + géocodage Etalab
- US-2 : Calcul similarité (5 SP)
  - Algorithme scoring multi-critères (6 dimensions)
- US-3 : Carte interactive (3 SP)
  - Folium + marqueurs colorés + popups

**Livrable :** Interface de saisie fonctionnelle + top 30 comparables sur carte

---

### Sprint 2 (10 SP) - Enrichissement DVF+
**Objectif :** Finaliser l'onglet DVF+ avec filtres et métriques

- US-4 : Street View (2 SP)
  - Intégration Google Maps API
- US-5 : Filtres manuels (3 SP)
  - Sliders rayon/années/score
- US-6 : Sélection & métriques (2 SP)
  - Checkbox + calculs statistiques + boxplot
- US-7 : Prix ajusté (3 SP)
  - Correction taux emprunt Banque de France

**Livrable :** Onglet DVF+ complet avec sélection manuelle et métriques

---

### Sprint 3 (18 SP) - Méthodes Complémentaires
**Objectif :** Ajouter 3 méthodes d'estimation alternatives

- US-8 : Perplexity Integration (8 SP)
  - API Perplexity pour annonces vente
- US-9 : Affichage comparables vente (5 SP)
  - Carte + filtres + export CSV
- US-10 : Méthode Additionnelle (8 SP) [Parallèle]
  - Maisons uniquement (Terrain + Construction)
- US-11 : Méthode Locative (5 SP) [Parallèle]
  - Appartements uniquement (capitalisation loyer)

**Livrable :** 4 méthodes d'estimation fonctionnelles

---

### Sprint 4 (13 SP) - Synthèse et Export
**Objectif :** Consolider toutes les méthodes et produire le rapport final

- US-12 : Pondération (7 SP)
  - Sliders pondération + estimation finale
- US-13 : Synthèse graphique (6 SP)
  - Radar chart + histogram + box plot + PDF ReportLab

**Livrable :** Application complète avec export PDF professionnel

---

## Statistiques Globales

### Répartition Story Points

| EPIC | SP | % Total | Sprint |
|------|----|---------|----|
| EPIC-001 | 21 | 35% | 1-2 |
| EPIC-002 | 13 | 22% | 2-3 |
| EPIC-003 | 8 | 13% | 3 |
| EPIC-004 | 5 | 8% | 3 |
| EPIC-005 | 13 | 22% | 4 |
| **TOTAL** | **60** | **100%** | **4** |

### Répartition Priorités

- **Must Have :** 9 US (47 SP) - 78%
- **Should Have :** 4 US (13 SP) - 22%

### Charge par Sprint

| Sprint | SP | US | Velocity |
|--------|----|----|----------|
| Sprint 1 | 11 | 3 | ~11 SP/sprint |
| Sprint 2 | 10 | 4 | |
| Sprint 3 | 18 | 4 | |
| Sprint 4 | 13 | 2 | |
| **Moyenne** | **13** | **3.25** | **13 SP/sprint** |

---

## Dépendances Techniques Globales

### Infrastructure
- **Base de données :** Supabase (PostgreSQL + PostGIS)
- **Backend :** Python 3.11+, pandas, NumPy
- **Frontend :** Streamlit
- **Déploiement :** Vercel

### APIs Externes
- **Google Maps API :** Street View Static
- **API Adresse Etalab :** Géocodage (gratuite)
- **Perplexity API :** Recherche annonces + prix/m²
- **Banque de France :** Taux d'emprunt historiques

### Bibliothèques Python
- **Cartographie :** Folium, streamlit-folium
- **Visualisation :** Plotly Express
- **PDF :** ReportLab
- **HTTP :** httpx (async)
- **Tests :** pytest, pytest-cov

### Modules Internes
- `src/supabase_data_retriever.py` : Requêtes PostGIS DVF+
- `src/estimation_algorithm.py` : Scoring multi-critères
- `src/utils/geocoding.py` : Wrapper Google Maps
- `src/streamlit_components/` : 5 composants modulaires

---

## Critères de Qualité

### Tests
- Coverage ≥ 80%
- 1 fichier test par module (39 tests, 22 passing actuellement)
- Tests unitaires + intégration

### Performance
- Calcul similarité : <3s
- Chargement carte : <2s
- Filtrage : <1s
- Génération PDF : <10s

### UX
- Interface responsive (mobile/desktop)
- Messages d'erreur clairs
- Tooltips explicatifs
- Temps de chargement visibles (spinners)

### Documentation
- Docstrings style Google (3 lignes min)
- Type hints Python obligatoires
- README par EPIC
- USER_STORIES.md détaillé

---

## Navigation Rapide

### Documents Projet
- [README.md](./README.md) - Vue d'ensemble PRD
- [EPICS.md](./EPICS.md) - Index EPICs
- [../CONTEXT_PROJET.md](../CONTEXT_PROJET.md) - Contexte business
- [../PLAN_MVP_IMPLEMENTATION.md](../PLAN_MVP_IMPLEMENTATION.md) - Plan technique
- [../../CLAUDE.md](../../CLAUDE.md) - Instructions Claude

### Par EPIC
1. [EPIC-001 : Comparables DVF+](./EPIC_001_Comparables_DVF/README.md)
2. [EPIC-002 : Comparables Vente](./EPIC_002_Comparables_Vente/README.md)
3. [EPIC-003 : Méthode Additionnelle](./EPIC_003_Methode_Additionnelle/README.md)
4. [EPIC-004 : Méthode Locative](./EPIC_004_Methode_Locative/README.md)
5. [EPIC-005 : Synthèse Pondération](./EPIC_005_Synthese_Ponderation/README.md)

### Liens Externes
- [PRD Notion](https://www.notion.so/Automatisation-des-estimations-2fc6cfd339504d1bbf444c0ae078ff5c)
- [Repo GitHub](https://github.com/jbcholat-Dev/Estimation-immo-1)

---

## Changelog

**Version 1.0** (2025-11-21)
- Création structure complète 5 EPICs
- Documentation 13 User Stories détaillées
- Total 60 SP planifiés sur 4 sprints
- 23 fichiers markdown créés

---

**Maintenu par :** Agent Claude Code
**Dernière mise à jour :** 2025-11-21
**Format :** Markdown
**Encodage :** UTF-8
