
# PRD – Estimateur Immobilier Automatisé v1.0

> 🎯 Mission: Réduire le temps de production des estimations immobilières de 50% en automatisant la collecte, l'analyse et le calcul de 4 méthodes d'estimation complémentaires, tout en préservant l'expertise métier pour la validation finale.

---

## 🗺️ Navigation & Organisation
  📄 Document actuel : PRD - Spécifications détaillées
  📦 Epics de développement (5) - 60 Story Points :
  1. Epic 1 : Onglet Comparables Vendues (DVF+) - 21 pts - Phase 1
  1. Epic 2 : Onglet Comparables en Vente (Perplexity) - 13 pts - Phase 1
  1. Epic 3 : Onglet Méthode Additionnelle (Maisons) - 8 pts - Phase 2
  1. Epic 4 : Onglet Méthode Locative (Appartements) - 5 pts - Phase 2
  1. Epic 5 : Onglet Synthèse et Pondération - 13 pts - Phase 2
  📋 User Stories (13) :
  - Sprint 1 : US1 : Formulaire de saisie du bien à estimer • US2 : Calcul similarité et affichage top 30 comparables DVF+ • US3 : Carte interactive avec marqueurs colorés selon similarité
  - Sprint 2 : US4 : Street View au clic sur marqueur • US5 : Filtres manuels (rayon, années, similarité) • US6 : Sélection checkbox et calcul métriques • US7 : Colonne prix ajusté pouvoir d'achat
  - Sprint 3 : US8 : Intégration API Perplexity scan annonces web • US9 : Carte, filtres et sélection onglet comparables en vente
  - Sprint 4 : US10 : Méthode additionnelle avec recherche Perplexity prix zone • US11 : Méthode locative avec recherche Perplexity taux rendement
  - Sprint 5 : US12 : Pondération ajustable avec contrainte 100% • US13 : Graphique comparatif horizontal vendus vs en vente
  📊 Tableaux de bord :
  - Kanban Epics • Roadmap Timeline • Sprint Board User Stories

---

## 📑 Sommaire

---

## 1. Contexte & Problème

### Workflow global
Point de départ : Création d'un contact dans Notion CRM → association d'un bien → déclenchement estimation
Outil actuel : Application Streamlit dédiée à la collecte et au traitement des données
Mise en page finale : Gamma (hors scope application)
Source de données principale : Base DVF+ déployée sur Supabase

### Situation actuelle
- Durée estimation: 4 à 6 heures par dossier
- Processus manuel: Recherche DVF, extraction données, analyse comparative, calculs multiples, recherche annonces concurrentes, rédaction
- 4 méthodes d'estimation utilisées: Comparables vendues, comparables en vente, additionnelle, locative
- Contrainte Chablais/Léman: Volume de transactions limité, hétérogénéité du marché

### Problèmes identifiés
1. Répétition des tâches de collecte et calcul pour chaque méthode
1. Absence d'outillage unifié pour exploiter DVF+ et scanner le web
1. Difficulté à visualiser géographiquement les comparables pertinents
1. Pas de méthode standardisée pour pondérer les 4 méthodes d'estimation
1. Validation visuelle fastidieuse (pas de Street View intégré)

### Opportunité
Créer une application unique avec 5 onglets dédiés (4 méthodes + synthèse) pour automatiser la collecte, le calcul et la visualisation, réduisant ainsi le temps d'expertise pure.

---

## 2. Objectifs & Critères de Succès

### Objectifs business
- Gain de temps: Réduire de 50% le temps de production (de 4-6h à 2-3h)
- Standardisation: Processus unifié pour les 4 méthodes d'estimation
- Qualité: Validation visuelle facilitée (carte + Street View)
- Traçabilité: Pondération documentée et ajustable

### Critères de succès (KPIs)

---

## 3. Architecture : 5 Onglets

### Onglet 1 : Comparables Vendues (DVF+)
Objectif: Analyser les transactions passées similaires au bien estimé
Flow:
1. Calcul automatique score similarité (top 30 comparables)
1. Filtrage manuel (sliders : rayon km, années, % similarité min)
1. Sélection checkbox (5-7 biens retenus)
1. Métriques calculées : médiane, prix/m², boxplot
Visualisation:
- Carte interactive au-dessus du tableau
- Marqueur rouge : bien à estimer
- Points colorés (gradient selon similarité) : comparables
- Clic sur marqueur → panneau Street View + détails
Colonnes tableau:
- Adresse, date transaction, prix origine
- Prix ajusté pouvoir d'achat (basé sur taux emprunt historique)
- Surface, pièces, score similarité

---

### Onglet 2 : Comparables en Vente (Concurrentiel)
Objectif: Analyser les annonces actuelles du marché
Source: Scan web via API Perplexity (SeLoger, LeBonCoin, etc.)
Flow:
1. Déclenchement scan Perplexity (calcul similarité intégré)
1. Import/affichage des résultats dans tableau
1. Filtrage manuel identique Onglet 1
1. Sélection checkbox
1. Métriques : médiane, prix/m², boxplot
Visualisation:
- Carte interactive (même pattern qu'Onglet 1)
- Points verts : biens en vente

---

### Onglet 3 : Méthode Additionnelle (Maisons uniquement)
Objectif: Calculer valeur terrain + coût construction + ajustements
Données d'entrée:
- Surface terrain (m²)
- Surface habitable (m²)
- Coefficient vétusté (%)
- Coefficient environnement (%)
Automatisation Perplexity:
- Recherche prix/m² terrain dans la zone
- Recherche coût construction neuf dans la zone
Calcul:

```javascript
Valeur brute = (Terrain × Prix/m² terrain) + (Surface × Coût construction/m²)
Valeur ajustée = Valeur brute × (1 + Coef environnement) × (1 - Coef vétusté)
```
Interface:
- Champs avec valeurs €/m² auto-remplies (API Perplexity)
- Sliders ajustement coefficients
- Affichage calcul détaillé

---

### Onglet 4 : Méthode Locative (Appartements uniquement)
Objectif: Calculer valeur basée sur rendement locatif
Données d'entrée:
- Valeur locative mensuelle (€/mois)
Automatisation Perplexity:
- Recherche taux de rendement espéré pour [type bien] à [commune]
Calcul:

```javascript
Loyer annuel = Loyer mensuel × 12
Valeur bien = Loyer annuel / Taux rendement
```
Interface:
- Input loyer mensuel
- Affichage taux rendement (plusieurs scénarios : prudent/moyen/optimiste)
- Calcul valeur pour chaque scénario

---

### Onglet 5 : Synthèse et Pondération
Objectif: Agréger les 4 méthodes avec pondération ajustable
Logique conditionnelle:
Maisons (3 méthodes actives):
- Comparative vendus : 50%
- Concurrentielle : 30%
- Additionnelle : 20%
- ❌ Locative désactivée
Appartements (3 méthodes actives):
- Comparative vendus : 50%
- Concurrentielle : 30%
- Locative : 20%
- ❌ Additionnelle désactivée
Interface:
- Affichage des 3-4 valeurs calculées
- Sliders % pour chaque méthode (contrainte : total = 100%)
- Calcul estimation finale pondérée
- Graphique comparatif horizontal:
  - Tous les biens retenus (onglets 1 + 2)
  - Code couleur : 🔵 vendus, 🟢 en vente
  - Lignes médianes : détecter surestimation/sous-estimation marché

---

## 4. Formulaire de Saisie Initial

### Champs obligatoires
- Adresse (géocodage automatique)
- Type de bien (Maison / Appartement)
- Surface habitable (m²)
- Nombre de pièces
- DPE (lettre A-G)

### Champs conditionnels
Si Maison:
- Taille terrain (m²)

### Champs ajustements
- Coefficient vétusté (%) : état général du bien
- Coefficient environnement (%) : nuisances, vue, etc.
- Valeur locative mensuelle (€) : pour méthode locative

### Évolution V2
Import automatique depuis Notion (base de données Biens) au lieu de saisie manuelle.

---

## 5. Requirements Fonctionnels Détaillés

### 5.1 Moteur de Similarité

### Score de similarité (pondération 100%)
Critères obligatoires (55%):
1. Type de bien (15%): Maison vs Appartement
  - Identique = 100%
  - Différent = 0%
1. Surface habitable (15%): Écart relatif en %
  - Formule: 100 - min(100, |surface_cible - surface_comparable| / surface_cible × 100)
1. Localisation (15%): Distance géographique
  - Même commune = 100%
  - Rayon 5km = 70%
  - Rayon 10km = 40%
  - Au-delà = 0%
1. Période construction (10%):
  - Même période = 100%
  - Période adjacente = 60%
  - Autre = 30%
Critères détaillés (30%):
1. Nombre de pièces (10%): Écart absolu
  - Identique = 100%
  - ±1 pièce = 70%
  - ±2 pièces = 40%
1. DPE (10%): Écart lettres
  - Identique = 100%
  - ±1 lettre = 70%
  - ±2 lettres = 40%
1. Surface terrain (10%): Pour maisons uniquement
  - Formule identique à surface habitable
Critère temporel (15%):
1. Ancienneté transaction (15%):
  - < 1 an = 100%
  - 1-2 ans = 95%
  - 2-3 ans = 90%
  - 3-5 ans = 80%
  - 

> 5 ans = 60%

---

### 5.2 Ajustement Pouvoir d'Achat (Onglet 1)
Objectif: Expliquer l'évolution des prix via capacité d'emprunt
Formule simplifiée:

```javascript
Prix ajusté = Prix origine × (Taux emprunt transaction / Taux emprunt actuel)
```
Exemple:
- Bien vendu 500k€ il y a 3 ans à taux 1.2%
- Taux actuel : 4%
- Prix ajusté = 500k × (1.2 / 4) = 150k€ (pouvoir d'achat équivalent)
Source données: Historique taux emprunt (Banque de France, API externe ou CSV)

---

### 5.3 Visualisation Cartographique
Onglets 1 & 2 : Carte au-dessus du tableau
Éléments carte:
- 🔴 Marqueur spécial : bien à estimer
- Points colorés : gradient selon score similarité
  - 🟢 Vert foncé : > 80%
  - 🟡 Jaune : 60-80%
  - 🟠 Orange : < 60%
Interaction au clic:
1. Clic sur marqueur comparable
1. Ouverture panneau latéral (ou popup)
1. Contenu :
  - Photo Street View du bien
  - Adresse, prix, surface, date, score
  - Bouton sélection/déselection
Technologies:
- Folium ou Leaflet (carte)
- Google Street View API (photos)

---

### 5.4 Intégrations API Perplexity
Usage 1 - Onglet 2 : Scan annonces web
- Prompt : "Trouve les biens [type] à vendre à [commune] similaires à [caractéristiques]"
- Output structuré : JSON avec adresse, prix, surface, URL annonce
Usage 2 - Onglet 3 : Prix terrain + construction
- Prompt 1 : "Prix moyen terrain constructible €/m² à [commune]"
- Prompt 2 : "Coût construction neuf maison €/m² à [commune]"
Usage 3 - Onglet 4 : Taux rendement locatif
- Prompt : "Taux de rendement locatif attendu pour [type bien] à [commune]"

---

## 6. Stack Technique

### Framework & Hébergement
- Framework: Streamlit (Python 3.11+)
- Hébergement: Streamlit Cloud ou Render

### Base de données
- Supabase PostgreSQL + PostGIS
- Tables DVF+ (mutation, local, disposition_parcelle)
- Indexes spatiaux pour performances

### APIs externes
- Perplexity API : scan web, recherches prix zones
- API Adresse Etalab : géocodage (gratuit)
- Google Street View API : photos biens
- Taux emprunt : Banque de France ou équivalent

### Librairies Python
- pandas + geopandas : traitement données
- folium + streamlit-folium : cartes interactives
- plotly : graphiques (boxplot, barres horizontales)
- psycopg2 : connexion Supabase

### État & Cache
- st.session_state : gestion onglets, sélections
- @st.cache_data : optimisation requêtes lourdes

---

## 7. Scope & Contraintes

### Dans le scope v1.0 MVP Streamlit
✅ 5 onglets fonctionnels (4 méthodes + synthèse)
✅ Calcul automatique similarité + sélection manuelle
✅ Carte interactive + Street View au clic
✅ Intégration API Perplexity (3 usages)
✅ Ajustement pouvoir d'achat (taux emprunt)
✅ Pondération ajustable avec contrainte 100%
✅ Graphique comparatif synthèse
✅ Export résultats (à définir : PDF/Excel)

### Hors scope v1.0 (futures versions)
❌ Score de fiabilité automatique (mis de côté)
❌ Import automatique depuis Notion CRM
❌ Génération rapport client complet stylisé
❌ Historique comparatif estimations multiples
❌ Application mobile
❌ Migration Next.js (planifiée v2.0+)

### Contraintes techniques
- Budget API Google Maps : 200€/mois max (Street View)
- Budget API Perplexity : à définir selon volumétrie
- Données DVF+ : mise à jour semestrielle (Cerema)
- Couverture Street View : partielle en zone rurale
- Performance : calculs < 3s par onglet

### Contraintes métier
- Outil d'assistance, validation humaine obligatoire
- Spécificités Chablais nécessitent expertise agent
- Dépendance qualité données DVF+ (erreurs possibles)

---

## 8. Roadmap & Jalons

### Phase 0 – Setup & Data (1 semaine)

### Phase 1 – Onglets 1 & 2 (3 semaines)

### Phase 2 – Onglets 3 & 4 (2 semaines)

### Phase 3 – Onglet 5 Synthèse (1 semaine)

### Phase 4 – Production (1 semaine)
Durée totale estimée : 8 semaines

---

## 9. Risques & Mitigations

---

## 10. Mesure du Succès

### Après 2 mois utilisation
Critères de succès:
- ✅ 80% des estimations produites avec l'outil
- ✅ Temps moyen réduit à 2.5h (vs 5h avant) = 50% gain
- ✅ 3-4 méthodes utilisées systématiquement (vs 2 avant)
- ✅ Feedback agents : 8/10 satisfaction
- ✅ Validation visuelle facilitée (carte + Street View)
KPIs de suivi:
- Nombre estimations/semaine
- Temps moyen par estimation
- Nombre méthodes utilisées par estimation
- Taux utilisation API Perplexity
- Taux visualisation Street View

---

## 11. Prochaines Étapes Immédiates
Actions semaine 1:
1. Setup technique (2j):
1. Exploration données (1j):
1. POC Onglet 1 (2j):
Décisions urgentes requises:
- ✅ Budget API Perplexity mensuel à valider
- ✅ Source historique taux emprunt à identifier
- ✅ Format export final (PDF/Excel/autre)

---

> ✅ Status: PRD v1.0 mis à jour - Architecture 5 onglets validée
  Owner: Jean-Baptiste CHOLAT
  Date mise à jour: 20 novembre 2025
  Prochaine revue: Fin Phase 1 (estimation: mi-janvier 2026)


