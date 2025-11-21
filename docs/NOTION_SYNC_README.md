# Guide d'Utilisation - Synchronisation Notion PRD

Ce guide explique comment utiliser les fichiers generes par la synchronisation Notion et comment maintenir la structure EPIC/US a jour.

---

## Fichiers Generes

### Documentation PRD

| Fichier | Description | Usage |
|---------|-------------|-------|
| `NOTION_PRD_RAW.md` | Contenu brut de la page Notion (400 lignes) | Reference complete du PRD |
| `NOTION_COMPLETE.md` | Page principale + pages enfants | Document consolide |
| `NOTION_SYNC_SUMMARY.md` | Resume de la synchronisation avec vue d'ensemble | Point d'entree principal |

### Structure EPIC/User Stories

| Fichier | Description | Usage |
|---------|-------------|-------|
| `EPICS_USER_STORIES.md` | Structure detaillee des 5 Epics et 13 US avec criteres d'acceptation | Documentation developpement |
| `EPICS_USER_STORIES.json` | Structure machine-readable | Integration outils de gestion |
| `NOTION_PRD_STRUCTURE.json` | Structure extraite du parsing automatique | Debug/analyse |

---

## Scripts de Synchronisation

### Script 1: `scripts/notion_sync.py`
**Fonction:** Recupere le contenu depuis Notion via l'API officielle

**Prerequis:**
```bash
pip install notion-client
```

**Configuration:**
- Token Notion: Configure dans le script (ligne 14)
- Page ID: `2fc6cfd339504d1bbf444c0ae078ff5c`

**Usage:**
```bash
python scripts/notion_sync.py
```

**Output:**
- `docs/NOTION_PRD_RAW.md` - Contenu brut
- `docs/NOTION_COMPLETE.md` - Avec pages enfants
- `docs/NOTION_PRD_STRUCTURE.json` - Structure parsee

---

### Script 2: `scripts/extract_epics_from_prd.py`
**Fonction:** Extrait la structure EPIC/US depuis le PRD avec criteres d'acceptation

**Usage:**
```bash
python scripts/extract_epics_from_prd.py
```

**Output:**
- `docs/EPICS_USER_STORIES.md` - Structure Markdown
- `docs/EPICS_USER_STORIES.json` - Structure JSON

---

## Workflow de Synchronisation

### Synchronisation Complete (Recommandee)
```bash
# 1. Recuperer le contenu depuis Notion
python scripts/notion_sync.py

# 2. Extraire la structure EPIC/US
python scripts/extract_epics_from_prd.py
```

### Frequence Recommandee
- **Quotidienne:** Pendant la phase de specification (avant developpement)
- **Hebdomadaire:** Pendant le developpement actif
- **A la demande:** Lors de changements majeurs dans le Notion

---

## Integration avec Outils de Gestion

### Jira / Linear / Shortcut

**Option 1: Import Manuel**
1. Ouvrir `EPICS_USER_STORIES.md`
2. Copier chaque Epic comme une Epic dans votre outil
3. Copier chaque US comme une Story liee a l'Epic
4. Copier les criteres d'acceptation dans la description

**Option 2: Import Automatise (JSON)**
```python
import json

# Charger la structure
with open('docs/EPICS_USER_STORIES.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Exemple: Creer des tickets Jira
for epic in data['epics']:
    epic_key = create_jira_epic(
        name=epic['name'],
        description=epic['description'],
        story_points=epic['story_points']
    )

    for us in epic['user_stories']:
        create_jira_story(
            epic_link=epic_key,
            title=us['title'],
            description=us['title'],
            acceptance_criteria=us['acceptance_criteria'],
            story_points=int(us['effort'].split()[0]),
            sprint=us['sprint'],
            priority=us['priority']
        )
```

---

## Structure des Donnees

### Format JSON - Epic
```json
{
  "id": 1,
  "name": "Onglet Comparables Vendues (DVF+)",
  "story_points": 21,
  "phase": "Phase 1",
  "description": "Analyser les transactions passees...",
  "onglet": "Onglet 1",
  "user_stories": [...]
}
```

### Format JSON - User Story
```json
{
  "id": 1,
  "title": "Formulaire de saisie du bien a estimer",
  "sprint": 1,
  "acceptance_criteria": [
    "Formulaire contient tous les champs obligatoires...",
    "Geocodage automatique via API Adresse Etalab..."
  ],
  "priority": "Must Have",
  "effort": "3 SP"
}
```

---

## Vue d'Ensemble du Projet

### Statistiques Globales
- **5 Epics** repartis sur 2 phases
- **13 User Stories** reparties sur 5 sprints
- **60 Story Points** au total
- **7 Must Have** (21 SP) + **6 Should Have** (39 SP)

### Distribution par Phase
- **Phase 1:** 9 US, 34 SP (Epics 1-2)
- **Phase 2:** 4 US, 26 SP (Epics 3-5)

### Distribution par Sprint
- **Sprint 1:** 3 US, 11 SP (Formulaire + Comparables DVF+)
- **Sprint 2:** 4 US, 10 SP (Filtres + Selection + Prix ajuste)
- **Sprint 3:** 2 US, 13 SP (Integration Perplexity vente)
- **Sprint 4:** 2 US, 13 SP (Methodes additionnelle + locative)
- **Sprint 5:** 2 US, 13 SP (Synthese + Ponderation)

---

## Maintenance et Mise a Jour

### Mettre a Jour depuis Notion
```bash
# Synchroniser avec Notion
python scripts/notion_sync.py

# Re-extraire la structure
python scripts/extract_epics_from_prd.py

# Verifier les changements
git diff docs/EPICS_USER_STORIES.md
```

### Modifier les Criteres d'Acceptation
Les criteres d'acceptation sont definis dans `scripts/extract_epics_from_prd.py` dans la fonction `get_acceptance_criteria_for_us()`.

Pour modifier:
1. Editer `scripts/extract_epics_from_prd.py`
2. Modifier le dictionnaire `criteria_map`
3. Re-executer le script

### Ajouter de Nouveaux Epics/US
1. Mettre a jour le Notion
2. Re-executer `notion_sync.py`
3. Modifier `extract_epics_from_prd.py` si necessaire:
   - Fonction `determine_epic_for_us()` pour mapping US -> Epic
   - Fonction `estimate_effort()` pour estimation SP
   - Fonction `get_acceptance_criteria_for_us()` pour criteres

---

## Troubleshooting

### Erreur: "notion-client non installe"
```bash
pip install notion-client
```

### Erreur: "UnicodeEncodeError" (Windows)
Les scripts ont ete modifies pour eviter les emojis. Si l'erreur persiste:
- Verifier que les fichiers sont enregistres en UTF-8
- Utiliser Python 3.11+

### Erreur: "Impossible de recuperer la page"
- Verifier le token Notion (ligne 14 de `notion_sync.py`)
- Verifier l'ID de page (ligne 16)
- Verifier les permissions d'acces a la page

### Pas d'Epics trouves
Le parser automatique ne detecte pas la structure. Utiliser `extract_epics_from_prd.py` qui parse manuellement la section navigation.

---

## Commandes Rapides

```bash
# Synchronisation complete
python scripts/notion_sync.py && python scripts/extract_epics_from_prd.py

# Voir le resume
cat docs/NOTION_SYNC_SUMMARY.md

# Ouvrir la structure EPIC/US
cat docs/EPICS_USER_STORIES.md

# Export JSON pour integration
cat docs/EPICS_USER_STORIES.json | jq '.epics[] | {name, story_points}'
```

---

## Contact et Support

Pour toute question sur la synchronisation ou les scripts:
1. Consulter `NOTION_SYNC_SUMMARY.md` pour la vue d'ensemble
2. Verifier les logs d'execution des scripts
3. Examiner les fichiers generes dans `docs/`

---

**Date derniere mise a jour:** 2025-11-21
**Version:** 1.0
**Scripts:** `notion_sync.py` + `extract_epics_from_prd.py`
