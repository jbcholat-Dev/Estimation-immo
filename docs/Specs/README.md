# Spécifications PRD - Estimateur Immobilier Automatisé v1.0

**Synchronisé depuis Notion** : https://www.notion.so/Automatisation-des-estimations-2fc6cfd339504d1bbf444c0ae078ff5c
**Dernière synchronisation** : 2025-11-21

---

## 🎯 Mission

Réduire le temps de production des estimations immobilières de **50%** en automatisant la collecte, l'analyse et le calcul de **4 méthodes d'estimation complémentaires**.

**Objectif chiffré :**
- Temps actuel : 4-6 heures par estimation
- Cible : 2-3 heures par estimation
- Zone : Chablais/Annemasse (Haute-Savoie, 74)

---

## 📊 Vue d'Ensemble

### Métriques Globales

| Métrique | Valeur |
|----------|--------|
| **Total EPIC** | 5 |
| **Total User Stories** | 13 |
| **Total Story Points** | 60 SP |
| **Sprints** | 5 |
| **Phases** | 2 (Phase 1 MVP + Phase 2 Complémentaire) |

### Priorités

| Niveau | Count | Story Points |
|--------|-------|--------------|
| **Must Have** | 7 | 21 SP |
| **Should Have** | 6 | 39 SP |

---

## 🗂️ Structure des EPIC

### Phase 1 : MVP (Sprints 1-3)

#### **EPIC 1 : Onglet Comparables Vendues (DVF+)**
- **Story Points** : 21 SP
- **Sprint** : 1-2
- **User Stories** : 7 (US-1 à US-7)
- 📁 [Dossier EPIC_001](./EPIC_001_Comparables_DVF/README.md)

**Résumé** : Analyser les transactions passées similaires via données DVF+.

#### **EPIC 2 : Onglet Comparables en Vente (Perplexity)**
- **Story Points** : 13 SP
- **Sprint** : 3
- **User Stories** : 2 (US-8 à US-9)
- 📁 [Dossier EPIC_002](./EPIC_002_Comparables_Vente/README.md)

**Résumé** : Intégration API Perplexity pour annonces en vente.

---

### Phase 2 : Complémentaires (Sprints 4-5)

#### **EPIC 3 : Onglet Méthode Additionnelle (Maisons)**
- **Story Points** : 8 SP | **Sprint** : 4
- 📁 [Dossier EPIC_003](./EPIC_003_Methode_Additionnelle/README.md)

#### **EPIC 4 : Onglet Méthode Locative (Appartements)**
- **Story Points** : 5 SP | **Sprint** : 4
- 📁 [Dossier EPIC_004](./EPIC_004_Methode_Locative/README.md)

#### **EPIC 5 : Onglet Synthèse et Pondération**
- **Story Points** : 13 SP | **Sprint** : 5
- 📁 [Dossier EPIC_005](./EPIC_005_Synthese_Ponderation/README.md)

---

## 🚀 Roadmap par Sprint

| Sprint | EPIC | Story Points | Contenu Principal |
|--------|------|--------------|-------------------|
| **Sprint 1** | EPIC 1 | 11 SP | Formulaire + Comparables DVF+ top 30 + Carte |
| **Sprint 2** | EPIC 1 | 10 SP | Street View + Filtres + Sélection + Prix ajusté |
| **Sprint 3** | EPIC 2 | 13 SP | Intégration Perplexity annonces en vente |
| **Sprint 4** | EPIC 3, 4 | 13 SP | Méthodes additionnelle + locative |
| **Sprint 5** | EPIC 5 | 13 SP | Synthèse + Pondération + Graphique |

---

**Voir aussi :**
- [EPICS.md](./EPICS.md) - Index détaillé
- [../EPICS_USER_STORIES.md](../EPICS_USER_STORIES.md) - Extraction brute Notion

**Source PRD Notion** : https://www.notion.so/Automatisation-des-estimations-2fc6cfd339504d1bbf444c0ae078ff5c
