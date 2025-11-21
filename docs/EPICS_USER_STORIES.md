# Estimateur Immobilier Automatise v1.0

**Mission:** Reduire le temps de production des estimations immobilieres de 50% en automatisant la collecte, l'analyse et le calcul de 4 methodes d'estimation complementaires

**Total Epics:** 5
**Total Story Points:** 60
**Total User Stories:** 13

---

## Epic 1: Onglet Comparables Vendues (DVF+)

**Story Points:** 21 | **Phase:** Phase 1 | **Onglet:** Onglet 1

**Description:**
Analyser les transactions passees similaires au bien estime. Calcul automatique score similarite, filtrage manuel, selection checkbox, metriques calculees (mediane, prix/m2, boxplot). Carte interactive avec Street View.

**User Stories (7):**

### US-1: Formulaire de saisie du bien à estimer

**Sprint:** 1 | **Priorite:** Must Have | **Effort:** 3 SP

**Criteres d'acceptation:**
1. Formulaire contient tous les champs obligatoires (adresse, type bien, surface, pieces, DPE)
2. Geocodage automatique via API Adresse Etalab fonctionnel
3. Champs conditionnels apparaissent selon type bien (terrain pour Maison)
4. Validation des champs obligatoires avant calcul
5. Donnees stockees dans session_state pour utilisation dans autres onglets


### US-2: Calcul similarité et affichage top 30 comparables DVF+

**Sprint:** 1 | **Priorite:** Must Have | **Effort:** 5 SP

**Criteres d'acceptation:**
1. Algorithme calcule score similarite base sur ponderation definie (surface 25%, pieces 15%, DPE 15%, distance 20%, anciennete 10%, type bien 15%)
2. Top 30 comparables affiches dans tableau avec toutes colonnes requises
3. Scores de similarite affiches en pourcentage (0-100%)
4. Calcul < 3 secondes pour recherche dans rayon 10km
5. Donnees DVF+ correctement recuperees depuis Supabase


### US-3: Carte interactive avec marqueurs colorés selon similarité

**Sprint:** 1 | **Priorite:** Must Have | **Effort:** 3 SP

**Criteres d'acceptation:**
1. Carte interactive Folium affichee au-dessus du tableau
2. Marqueur rouge pour bien a estimer + points colores pour comparables (gradient selon similarite)
3. Clic sur marqueur ouvre panneau avec Street View + details bien
4. Carte centre automatiquement sur bien a estimer
5. Performance: chargement carte < 2 secondes


### US-4: Street View au clic sur marqueur

**Sprint:** 2 | **Priorite:** Must Have | **Effort:** 2 SP

**Criteres d'acceptation:**
1. Integration Google Street View API fonctionnelle
2. Photo Street View affichee au clic sur marqueur
3. Fallback si Street View indisponible (message + photo generique)
4. Panneau affiche adresse, prix, surface, date, score
5. Budget API Google Maps respecte (200 euros/mois max)


### US-5: Filtres manuels (rayon, années, similarité)

**Sprint:** 2 | **Priorite:** Must Have | **Effort:** 3 SP

**Criteres d'acceptation:**
1. Sliders pour rayon km (1-20km), annees (1-10 ans), similarite min (0-100%)
2. Filtrage temps reel du tableau selon criteres
3. Nombre de resultats mis a jour dynamiquement
4. Performance: filtrage < 1 seconde
5. Valeurs par defaut pertinentes (rayon 5km, 5 ans, 50% similarite)


### US-6: Sélection checkbox et calcul métriques

**Sprint:** 2 | **Priorite:** Must Have | **Effort:** 2 SP

**Criteres d'acceptation:**
1. Checkbox pour chaque ligne du tableau
2. Selection multiple possible (5-7 biens recommandes)
3. Calcul automatique metriques: mediane, prix/m2, boxplot Plotly
4. Metriques mis a jour en temps reel lors selection/deselection
5. Validation: minimum 3 biens selectionnes pour calcul valide


### US-7: Colonne prix ajusté pouvoir d'achat

**Sprint:** 2 | **Priorite:** Must Have | **Effort:** 3 SP

**Criteres d'acceptation:**
1. Colonne prix ajuste affichee dans tableau avec formule basee sur taux emprunt historique
2. Source donnees taux emprunt Banque de France identifiee et integree
3. Calcul ajustement pouvoir achat correct (variation selon annee transaction)
4. Explication formule disponible (tooltip ou note)
5. Valeurs ajustees utilisees dans calculs metriques


---

## Epic 2: Onglet Comparables en Vente (Perplexity)

**Story Points:** 13 | **Phase:** Phase 1 | **Onglet:** Onglet 2

**Description:**
Analyser les annonces actuelles du marche. Scan web via API Perplexity (SeLoger, LeBonCoin, etc.). Filtrage manuel, selection, metriques.

**User Stories (2):**

### US-8: Intégration API Perplexity scan annonces web

**Sprint:** 3 | **Priorite:** Should Have | **Effort:** 5 SP

**Criteres d'acceptation:**
1. Integration API Perplexity fonctionnelle pour scan annonces web
2. Prompt structure pour recherche annonces similaires au bien
3. Output JSON structure avec adresse, prix, surface, URL annonce
4. Gestion erreurs API (retry, fallback, messages utilisateur)
5. Budget API Perplexity respecte


### US-9: Carte, filtres et sélection onglet comparables en vente

**Sprint:** 3 | **Priorite:** Should Have | **Effort:** 8 SP

**Criteres d'acceptation:**
1. Onglet 2 reprend pattern Onglet 1: carte + tableau + filtres + selection
2. Donnees Perplexity affichees dans tableau avec colonnes identiques
3. Carte avec points verts pour biens en vente
4. Filtres fonctionnels (rayon, prix, surface)
5. Selection checkbox + calcul metriques identique Onglet 1


---

## Epic 3: Onglet Méthode Additionnelle (Maisons)

**Story Points:** 8 | **Phase:** Phase 2 | **Onglet:** Onglet 3

**Description:**
Calculer valeur terrain + cout construction + ajustements. Automatisation Perplexity pour recherche prix/m2 terrain et cout construction neuf dans la zone.

**User Stories (1):**

### US-10: Méthode additionnelle avec recherche Perplexity prix zone

**Sprint:** 4 | **Priorite:** Should Have | **Effort:** 8 SP

**Criteres d'acceptation:**
1. API Perplexity recherche prix/m2 terrain et cout construction neuf dans zone
2. Champs auto-remplies avec valeurs recherchees
3. Sliders ajustement coefficients vetuste et environnement
4. Calcul valeur brute et ajustee affiche en temps reel
5. Formule detaillee visible pour transparence


---

## Epic 4: Onglet Méthode Locative (Appartements)

**Story Points:** 5 | **Phase:** Phase 2 | **Onglet:** Onglet 4

**Description:**
Calculer valeur basee sur rendement locatif. Automatisation Perplexity pour recherche taux de rendement espere.

**User Stories (1):**

### US-11: Méthode locative avec recherche Perplexity taux rendement

**Sprint:** 4 | **Priorite:** Should Have | **Effort:** 5 SP

**Criteres d'acceptation:**
1. Input loyer mensuel fonctionnel
2. API Perplexity recherche taux rendement espere pour type bien + commune
3. Affichage 3 scenarios: prudent, moyen, optimiste
4. Calcul valeur bien pour chaque scenario (Loyer annuel / Taux rendement)
5. Validation: taux rendement coherents (2-8%)


---

## Epic 5: Onglet Synthèse et Pondération

**Story Points:** 13 | **Phase:** Phase 2 | **Onglet:** N/A

**Description:**


**User Stories (2):**

### US-12: Pondération ajustable avec contrainte 100%

**Sprint:** 5 | **Priorite:** Should Have | **Effort:** 5 SP

**Criteres d'acceptation:**
1. Affichage des 3-4 valeurs calculees selon type bien
2. Sliders % pour chaque methode avec contrainte total = 100%
3. Logique conditionnelle Maisons vs Appartements (methodes actives/desactivees)
4. Calcul estimation finale ponderee en temps reel
5. Valeurs par defaut: 50% vendus, 30% vente, 20% additionnelle/locative


### US-13: Graphique comparatif horizontal vendus vs en vente

**Sprint:** 5 | **Priorite:** Should Have | **Effort:** 8 SP

**Criteres d'acceptation:**
1. Graphique Plotly horizontal avec tous biens retenus (onglets 1+2)
2. Code couleur: bleu pour vendus, vert pour en vente
3. Lignes medianes affichees pour detecter surestimation/sous-estimation
4. Graphique interactif (zoom, hover details)
5. Performance: generation graphique < 2 secondes


---
