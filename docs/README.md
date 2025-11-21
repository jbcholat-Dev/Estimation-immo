# 📚 Documentation - Estimateur Immobilier Automatisé

Bienvenue dans la documentation du projet Estimateur Immobilier. Ce dossier contient tous les guides, spécifications, et références techniques organisés par thématique.

---

## 📁 Structure de la Documentation

### 🎯 [01_Specification](./01_Specification/) - Spécifications et PRD
Tous les documents de spécification, PRD Notion, et User Stories.

| Document | Description |
|----------|-------------|
| **CONTEXT_PROJET.md** | Contexte business complet du projet |
| **MVP_REQUIREMENTS.md** | Requirements du MVP |
| **PLAN_MVP_IMPLEMENTATION.md** | Plan technique détaillé des 5 phases |
| **EPICS_USER_STORIES.md** | Structure EPIC/US extraite de Notion |
| **EPICS_USER_STORIES.json** | Format machine-readable (pour outils agiles) |
| **NOTION_SYNC_README.md** | Guide synchronisation Notion |
| **STREAMLIT_MVP_GUIDE.md** | Guide utilisateur Streamlit |
| **PHASE3_CORRECTION_REPORT.md** | Rapport correction Phase 3 (INSEE) |
| **PHASE5_VALIDATION_REPORT.md** | Rapport validation Phase 5 |
| **RAPPORT_PHASE2_SUPABASE.md** | Rapport Phase 2 (Supabase) |

### 🏗️ [02_Architecture](./02_Architecture/) - Architecture Technique
Documents d'architecture système et patterns.

| Document | Description |
|----------|-------------|
| **ARCHITECTURE_DIAGRAM.md** | Diagramme architecture complète |
| **COMPOUND_ENGINEERING.md** | Framework Compound Engineering |
| **FRONTEND_MIGRATION_STRATEGY.md** | Stratégie migration Streamlit → Next.js |

### ⚙️ [03_Setup](./03_Setup/) - Configuration Initiale
Guides pour configurer les services externes.

| Document | Description |
|----------|-------------|
| **SETUP_SUPABASE.md** | Configuration Supabase + PostGIS |
| **GOOGLE_MAPS_SETUP.md** | Configuration Google Maps API |
| **FIGMA_MCP_SETUP.md** | Configuration Figma MCP |

### 🔧 [04_Infrastructure](./04_Infrastructure/) - Infrastructure et Outils
Guides infrastructure, agents, et gestion.

| Document | Description |
|----------|-------------|
| **AGENTS_GUIDE.md** | Guide des 5 agents spécialisés |
| **CONTEXT_OPTIMIZATION.md** | Optimisation context window Claude |
| **FILE_CATALOG.md** | Catalogue complet des fichiers |
| **FILE_MANAGEMENT.md** | Règles gestion des fichiers |

### 📋 [05_Process](./05_Process/) - Processus et Workflow
Documentation des processus de développement.

| Document | Description |
|----------|-------------|
| **GIT_WORKFLOW.md** | Workflow Git du projet |
| **PRECOMMIT_SETUP.md** | Configuration pre-commit hooks |
| **TERMINAL_SETUP.md** | Setup terminal initial |

### 📊 [Spec](./Spec/) - Spécifications Détaillées (SYNCHRONISÉ NOTION)
Structure complète des 5 EPIC et 13 User Stories, synchronisée depuis Notion.

```
Spec/
├── README.md                    ← Synthèse PRD
├── EPICS.md                     ← Index complet
├── EPIC_001_Comparables_DVF/    (21 SP, 7 US)
├── EPIC_002_Comparables_Vente/  (13 SP, 2 US)
├── EPIC_003_Methode_Additionnelle/ (8 SP, 1 US)
├── EPIC_004_Methode_Locative/   (5 SP, 1 US)
└── EPIC_005_Synthese_Ponderation/ (13 SP, 2 US)
```

**Total : 60 Story Points, 5 Sprints, 13 User Stories, 2 Phases**

### 🖼️ [06_Assets](./06_Assets/) - Ressources Visuelles
Images, schémas, et fichiers multimédias.

---

## 🚀 Points d'Entrée Recommandés

### 👤 Pour un nouveau développeur
1. Lire : [01_Specification/CONTEXT_PROJET.md](./01_Specification/CONTEXT_PROJET.md)
2. Consulter : [02_Architecture/ARCHITECTURE_DIAGRAM.md](./02_Architecture/ARCHITECTURE_DIAGRAM.md)
3. Setup environnement : [03_Setup/](./03_Setup/)
4. Commencer développement : [Spec/EPIC_001/](./Spec/EPIC_001_Comparables_DVF/)

### 👔 Pour le Product Owner
1. Vue d'ensemble : [01_Specification/CONTEXT_PROJET.md](./01_Specification/CONTEXT_PROJET.md)
2. User Stories : [Spec/README.md](./Spec/README.md)
3. Roadmap : [Spec/EPICS.md](./Spec/EPICS.md)

### 🔧 Pour l'Infrastructure
1. Architecture : [02_Architecture/ARCHITECTURE_DIAGRAM.md](./02_Architecture/ARCHITECTURE_DIAGRAM.md)
2. Setup services : [03_Setup/](./03_Setup/)
3. Agents : [04_Infrastructure/AGENTS_GUIDE.md](./04_Infrastructure/AGENTS_GUIDE.md)
4. Infrastructure : [04_Infrastructure/FILE_CATALOG.md](./04_Infrastructure/FILE_CATALOG.md)

### 🎯 Pour démarrer Sprint 1
1. Lire EPIC : [Spec/EPIC_001_Comparables_DVF/README.md](./Spec/EPIC_001_Comparables_DVF/README.md)
2. Consulter User Stories : [Spec/EPIC_001_Comparables_DVF/USER_STORIES.md](./Spec/EPIC_001_Comparables_DVF/USER_STORIES.md)
3. Implémenter : [Spec/EPIC_001_Comparables_DVF/US_001_Formulaire_Saisie.md](./Spec/EPIC_001_Comparables_DVF/US_001_Formulaire_Saisie.md)

---

## 📊 Statistiques Documentation

| Métrique | Valeur |
|----------|--------|
| **Total fichiers markdown** | 40+ |
| **Taille totale** | ~800 KB |
| **Sections** | 6 thématiques |
| **EPIC documentés** | 5 |
| **User Stories** | 13 |
| **Story Points** | 60 |
| **Sprints** | 5 |

---

## 🔄 Synchronisation Notion

La documentation dans [Spec/](./Spec/) est **synchronisée automatiquement** depuis le PRD Notion.

**Pour mettre à jour :**
```bash
# Option 1 : Via agent
@notion-sync-agent

# Option 2 : Via script
python scripts/notion_sync.py
python scripts/extract_epics_from_prd.py
```

**PRD source :** https://www.notion.so/Automatisation-des-estimations-2fc6cfd339504d1bbf444c0ae078ff5c

---

## 🎯 Roadmap Projet

### Phase 1 : MVP (Sprints 1-3) - 45 SP
- ✅ EPIC 1 : Comparables DVF+ (21 SP)
- ✅ EPIC 2 : Comparables en Vente Perplexity (13 SP) [Partial]
- ✅ Fondations + interfaces

### Phase 2 : Extensions (Sprints 4-5) - 15 SP
- 🔜 EPIC 3 : Méthode Additionnelle (8 SP)
- 🔜 EPIC 4 : Méthode Locative (5 SP)
- 🔜 EPIC 5 : Synthèse & Pondération (13 SP)

---

## 📞 Support et Questions

### Agents Spécialisés
- **@docs-agent** - Accès PRD Notion + documentation
- **@notion-sync-agent** - Synchronisation Notion
- **@supabase-data-agent** - PostgreSQL/PostGIS expertise
- **@streamlit-mvp-agent** - Streamlit interface
- **@estimation-algo-agent** - Algorithmes estimation

### Contactez
- **Questions spec** : Consulter [01_Specification/](./01_Specification/)
- **Problèmes setup** : Voir [03_Setup/](./03_Setup/)
- **Architecture** : Lire [02_Architecture/](./02_Architecture/)

---

## 📝 Historique Synchronisation

| Date | Action | Source |
|------|--------|--------|
| 2025-11-21 | Documentation complète synchronisée | Notion PRD |
| 2025-11-21 | Structure docs/ organisée | Manuel |
| 2025-11-14 | Phase 5 validation tests | Tests |

---

**Dernière mise à jour :** 2025-11-21
**Synchronisé depuis Notion PRD :** https://www.notion.so/Automatisation-des-estimations-2fc6cfd339504d1bbf444c0ae078ff5c
