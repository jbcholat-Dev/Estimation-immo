# US-2 : Calcul similarité

**EPIC:** EPIC-001 - Onglet Comparables Vendues (DVF+)
**Sprint:** 1
**Priorité:** Must Have
**Story Points:** 5 SP

## User Story

En tant que système d'estimation, je veux calculer automatiquement un score de similarité entre le bien saisi et les transactions DVF+, pour identifier les 30 comparables les plus pertinents.

## Critères d'acceptation

- [ ] L'algorithme utilise une pondération multi-critères :
  - Surface habitable : 25%
  - Nombre de pièces : 15%
  - DPE : 15%
  - Distance géographique : 20%
  - Ancienneté transaction : 10%
  - Type de bien : 15%
- [ ] Le système retourne le top 30 des comparables
- [ ] Les scores sont exprimés en pourcentage (0-100%)
- [ ] Le calcul s'effectue en moins de 3 secondes
- [ ] Les comparables sont triés par score décroissant
- [ ] Un message d'erreur s'affiche si moins de 5 comparables trouvés
- [ ] Les scores sont stockés dans le session state
- [ ] L'algorithme gère les valeurs manquantes (DPE, surface terrain)

## Notes techniques

### Dépendances
- Base de données Supabase avec 56,216 mutations DVF+
- Module src/estimation_algorithm.py
- PostGIS pour calculs de distance géographique
- pandas pour manipulation des données

### Stack technique
- **Backend:** Python 3.11+
- **Base de données:** Supabase (PostgreSQL + PostGIS)
- **Calculs:** NumPy, pandas
- **Requêtes optimisées:** Index sur colonnes clés (type_bien, surface, date_mutation)

### Estimation détaillée
- Développement algorithme scoring : 6h
- Optimisation requêtes SQL/PostGIS : 4h
- Tests unitaires (coverage ≥80%) : 4h
- Gestion cas limites : 2h
- Documentation : 2h
- **Total : 18h (5 SP)**

### Formule de calcul

```python
score_total = (
    w_surface * score_surface +
    w_pieces * score_pieces +
    w_dpe * score_dpe +
    w_distance * score_distance +
    w_anciennete * score_anciennete +
    w_type * score_type
)

# Normalisation : score_total / sum(weights) * 100
```

### Calcul par critère

- **Surface :** `1 - abs(surface_bien - surface_comparable) / surface_bien`
- **Distance :** `1 - distance_km / rayon_max_km`
- **Ancienneté :** `1 - jours_depuis_transaction / (365 * nb_annees_max)`
- **DPE :** Matrice de similarité (A=100, B=85, C=70, D=50, E=30, F=15, G=0)
- **Type bien :** 100% si identique, 0% sinon
- **Pièces :** `1 - abs(nb_pieces_bien - nb_pieces_comparable) / nb_pieces_bien`

### Risques
- Performance dégradée si >100k transactions → Indexation + cache
- Données DVF+ incomplètes → Pondération dynamique (exclure critères manquants)
- Pas assez de comparables → Élargir rayon de recherche automatiquement

---

**Lien EPIC parent:** [README.md](./README.md)
