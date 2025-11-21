# US-7 : Prix ajusté

**EPIC:** EPIC-001 - Onglet Comparables Vendues (DVF+)
**Sprint:** 2
**Priorité:** Should Have
**Story Points:** 3 SP

## User Story

En tant qu'agent immobilier, je veux voir une colonne "Prix ajusté" tenant compte des taux d'emprunt historiques, pour comparer les transactions passées en valeur actuelle et affiner mon estimation.

## Critères d'acceptation

- [ ] Une colonne "Prix ajusté" s'ajoute au tableau des comparables
- [ ] Le prix ajusté est calculé en fonction du taux d'emprunt historique
- [ ] Les données de taux proviennent de la Banque de France
- [ ] La variation du prix est proportionnelle à l'évolution des taux
- [ ] Un tooltip/explication décrit la formule de calcul
- [ ] Le prix ajusté est utilisé dans les métriques (médiane, boxplot)
- [ ] Un toggle permet de basculer entre prix brut et prix ajusté
- [ ] Les taux sont mis à jour trimestriellement

## Notes techniques

### Dépendances
- API Banque de France (taux d'emprunt immobilier)
- Dataframe pandas des comparables
- Date de transaction de chaque comparable
- Module de calcul d'ajustement

### Stack technique
- **Source données :** API Banque de France (gratuite)
- **Stockage taux :** Supabase (table taux_emprunt)
- **Calculs :** pandas (vectorisation)
- **Affichage :** Streamlit (tooltip, toggle)

### Estimation détaillée
- Intégration API Banque de France : 2h
- Calcul prix ajusté (formule) : 2h
- Ajout colonne au tableau : 1h
- Toggle prix brut/ajusté : 1h
- Tooltip explicatif : 1h
- Tests et validation : 2h
- **Total : 9h (3 SP)**

### Formule de calcul

```python
def calculer_prix_ajuste(prix_transaction, date_transaction, taux_actuel, taux_historique):
    """
    Ajuste le prix en fonction de l'évolution des taux d'emprunt.

    Hypothèse : Une hausse de 1% des taux réduit le pouvoir d'achat de ~10%
    (relation empirique marché immobilier français)
    """
    delta_taux = taux_actuel - taux_historique
    coefficient_ajustement = 1 - (delta_taux * 0.10)

    prix_ajuste = prix_transaction * coefficient_ajustement

    return round(prix_ajuste, 0)
```

### Exemple de calcul

- **Transaction 2020 :** 300,000 € (taux 1.2%)
- **Taux actuel 2024 :** 3.5%
- **Delta taux :** 3.5% - 1.2% = 2.3%
- **Coefficient :** 1 - (2.3 * 0.10) = 0.77
- **Prix ajusté :** 300,000 × 0.77 = 231,000 €

### Source des taux

**API Banque de France :**
- Endpoint : `/webstat/fr/downloadFile.do`
- Série : Taux moyen des crédits immobiliers aux particuliers
- Fréquence : Mensuelle
- Gratuit et fiable

**Table Supabase :**
```sql
CREATE TABLE taux_emprunt (
    id SERIAL PRIMARY KEY,
    date_mois DATE NOT NULL,
    taux_moyen DECIMAL(4,2) NOT NULL,
    source VARCHAR(100) DEFAULT 'Banque de France'
);
```

### Affichage

```python
# Toggle
afficher_prix_ajuste = st.toggle("Afficher prix ajustés selon taux", value=True)

# Tooltip
st.info("""
**Prix ajusté :** Le prix de vente est corrigé selon l'évolution des taux d'emprunt.
Une hausse de 1% des taux réduit le pouvoir d'achat de ~10%.

Exemple : Un bien vendu 300k€ en 2020 (taux 1.2%) équivaut à ~231k€ aujourd'hui (taux 3.5%).
""")
```

### Risques
- Formule simpliste → Validation avec expert immobilier
- Taux Banque de France indisponibles → Cache local + update manuel
- Effet non linéaire des taux → Ajustement formule si nécessaire

---

**Lien EPIC parent:** [README.md](./README.md)
