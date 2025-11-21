# Synchronisation Notion PRD - Resume

**Date:** 2025-11-21
**Source:** https://www.notion.so/Automatisation-des-estimations-2fc6cfd339504d1bbf444c0ae078ff5c
**Status:** Synchronisation complete

---

## Fichiers Generes

### 1. Contenu Brut
**Fichier:** `c:\Users\jbcho\Estimation-immo-1\docs\NOTION_PRD_RAW.md`
**Description:** Contenu complet de la page Notion PRD au format Markdown (400 lignes, 289 blocks)

### 2. Contenu Complet
**Fichier:** `c:\Users\jbcho\Estimation-immo-1\docs\NOTION_COMPLETE.md`
**Description:** Page principale + pages enfants (aucune page enfant trouvee)

### 3. Structure EPIC/US (Markdown)
**Fichier:** `c:\Users\jbcho\Estimation-immo-1\docs\EPICS_USER_STORIES.md`
**Description:** Structure detaillee des 5 Epics et 13 User Stories avec criteres d'acceptation

### 4. Structure EPIC/US (JSON)
**Fichier:** `c:\Users\jbcho\Estimation-immo-1\docs\EPICS_USER_STORIES.json`
**Description:** Structure machine-readable pour integration avec outils de gestion de projet

---

## Structure du Projet

### Vue d'ensemble
- **Projet:** Estimateur Immobilier Automatise v1.0
- **Mission:** Reduire le temps de production des estimations immobilieres de 50% en automatisant la collecte, l'analyse et le calcul de 4 methodes d'estimation complementaires
- **Total Epics:** 5
- **Total User Stories:** 13
- **Total Story Points:** 60

---

## Epics et User Stories

### Epic 1: Onglet Comparables Vendues (DVF+)
**Story Points:** 21 | **Phase:** Phase 1 | **Onglet:** Onglet 1

**Description:**
Analyser les transactions passees similaires au bien estime. Calcul automatique score similarite, filtrage manuel, selection checkbox, metriques calculees (mediane, prix/m2, boxplot). Carte interactive avec Street View.

**User Stories (7):**
1. **US-1:** Formulaire de saisie du bien a estimer (Sprint 1, 3 SP, Must Have)
2. **US-2:** Calcul similarite et affichage top 30 comparables DVF+ (Sprint 1, 5 SP, Must Have)
3. **US-3:** Carte interactive avec marqueurs colores selon similarite (Sprint 1, 3 SP, Must Have)
4. **US-4:** Street View au clic sur marqueur (Sprint 2, 2 SP, Must Have)
5. **US-5:** Filtres manuels (rayon, annees, similarite) (Sprint 2, 3 SP, Must Have)
6. **US-6:** Selection checkbox et calcul metriques (Sprint 2, 2 SP, Must Have)
7. **US-7:** Colonne prix ajuste pouvoir d'achat (Sprint 2, 3 SP, Must Have)

---

### Epic 2: Onglet Comparables en Vente (Perplexity)
**Story Points:** 13 | **Phase:** Phase 1 | **Onglet:** Onglet 2

**Description:**
Analyser les annonces actuelles du marche. Scan web via API Perplexity (SeLoger, LeBonCoin, etc.). Filtrage manuel, selection, metriques.

**User Stories (2):**
1. **US-8:** Integration API Perplexity scan annonces web (Sprint 3, 5 SP, Should Have)
2. **US-9:** Carte, filtres et selection onglet comparables en vente (Sprint 3, 8 SP, Should Have)

---

### Epic 3: Onglet Methode Additionnelle (Maisons)
**Story Points:** 8 | **Phase:** Phase 2 | **Onglet:** Onglet 3

**Description:**
Calculer valeur terrain + cout construction + ajustements. Automatisation Perplexity pour recherche prix/m2 terrain et cout construction neuf dans la zone.

**User Stories (1):**
1. **US-10:** Methode additionnelle avec recherche Perplexity prix zone (Sprint 4, 8 SP, Should Have)

---

### Epic 4: Onglet Methode Locative (Appartements)
**Story Points:** 5 | **Phase:** Phase 2 | **Onglet:** Onglet 4

**Description:**
Calculer valeur basee sur rendement locatif. Automatisation Perplexity pour recherche taux de rendement espere.

**User Stories (1):**
1. **US-11:** Methode locative avec recherche Perplexity taux rendement (Sprint 4, 5 SP, Should Have)

---

### Epic 5: Onglet Synthese et Ponderation
**Story Points:** 13 | **Phase:** Phase 2 | **Onglet:** Onglet 5

**Description:**
Agreger les 4 methodes avec ponderation ajustable. Logique conditionnelle Maisons vs Appartements. Graphique comparatif horizontal.

**User Stories (2):**
1. **US-12:** Ponderation ajustable avec contrainte 100% (Sprint 5, 5 SP, Should Have)
2. **US-13:** Graphique comparatif horizontal vendus vs en vente (Sprint 5, 8 SP, Should Have)

---

## Distribution par Sprint

### Sprint 1 (3 US, 11 SP)
- US-1: Formulaire de saisie du bien a estimer (3 SP)
- US-2: Calcul similarite et affichage top 30 comparables DVF+ (5 SP)
- US-3: Carte interactive avec marqueurs colores selon similarite (3 SP)

### Sprint 2 (4 US, 10 SP)
- US-4: Street View au clic sur marqueur (2 SP)
- US-5: Filtres manuels (rayon, annees, similarite) (3 SP)
- US-6: Selection checkbox et calcul metriques (2 SP)
- US-7: Colonne prix ajuste pouvoir d'achat (3 SP)

### Sprint 3 (2 US, 13 SP)
- US-8: Integration API Perplexity scan annonces web (5 SP)
- US-9: Carte, filtres et selection onglet comparables en vente (8 SP)

### Sprint 4 (2 US, 13 SP)
- US-10: Methode additionnelle avec recherche Perplexity prix zone (8 SP)
- US-11: Methode locative avec recherche Perplexity taux rendement (5 SP)

### Sprint 5 (2 US, 13 SP)
- US-12: Ponderation ajustable avec contrainte 100% (5 SP)
- US-13: Graphique comparatif horizontal vendus vs en vente (8 SP)

---

## Distribution par Priorite

### Must Have (7 US, 21 SP)
- US-1 a US-7 (Epic 1 complet)

### Should Have (6 US, 39 SP)
- US-8 a US-13 (Epics 2, 3, 4, 5)

---

## Distribution par Phase

### Phase 1 (9 US, 34 SP)
- Epic 1: Onglet Comparables Vendues (DVF+) - 7 US, 21 SP
- Epic 2: Onglet Comparables en Vente (Perplexity) - 2 US, 13 SP

### Phase 2 (4 US, 26 SP)
- Epic 3: Onglet Methode Additionnelle (Maisons) - 1 US, 8 SP
- Epic 4: Onglet Methode Locative (Appartements) - 1 US, 5 SP
- Epic 5: Onglet Synthese et Ponderation - 2 US, 13 SP

---

## Scripts Utilises

### Script 1: Synchronisation Notion
**Fichier:** `c:\Users\jbcho\Estimation-immo-1\scripts\notion_sync.py`
**Description:** Recupere le contenu de la page Notion via API officielle, convertit en Markdown, explore les pages enfants

**Usage:**
```bash
python scripts/notion_sync.py
```

### Script 2: Extraction Structure EPIC/US
**Fichier:** `c:\Users\jbcho\Estimation-immo-1\scripts\extract_epics_from_prd.py`
**Description:** Parse le PRD pour extraire la structure des Epics et User Stories avec criteres d'acceptation detailles

**Usage:**
```bash
python scripts/extract_epics_from_prd.py
```

---

## Prochaines Etapes

1. **Validation:** Verifier que les criteres d'acceptation correspondent aux attentes metier
2. **Integration:** Importer la structure JSON dans votre outil de gestion de projet (Jira, Linear, etc.)
3. **Planification:** Confirmer la distribution par sprint et ajuster si necessaire
4. **Suivi:** Utiliser `EPICS_USER_STORIES.md` comme reference pour le developpement

---

## Notes Techniques

### API Notion
- **Token:** Configure dans `notion_sync.py`
- **Page ID:** `2fc6cfd339504d1bbf444c0ae078ff5c`
- **Methode:** Utilisation de l'API officielle Notion (`notion-client` Python)

### Limitations
- Pas de pages enfants trouvees dans le Notion (structure plate)
- Les criteres d'acceptation ont ete deduits du contenu du PRD et des meilleures pratiques
- Les estimations de Story Points sont basees sur la complexite estimee de chaque US

### Recommandations
- Mettre a jour regulierement depuis Notion avec `notion_sync.py`
- Synchroniser les criteres d'acceptation dans Notion pour avoir une source unique de verite
- Utiliser le JSON pour automatiser la creation de tickets dans votre outil de gestion
