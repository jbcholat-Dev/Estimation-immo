# US-12 : Pondération

**EPIC:** EPIC-005 - Onglet Synthèse et Pondération
**Sprint:** 4
**Priorité:** Must Have
**Story Points:** 7 SP

## User Story

En tant qu'agent immobilier, je veux ajuster manuellement le poids de chaque méthode d'estimation via des sliders, pour obtenir une estimation finale personnalisée selon mon expertise et les spécificités du bien.

## Critères d'acceptation

- [ ] L'onglet affiche les 4 estimations :
  - DVF+ (Comparables vendues)
  - Comparables en vente (Perplexity)
  - Méthode additionnelle (si maison)
  - Méthode locative (si appartement)
- [ ] Des sliders permettent d'ajuster le poids de chaque méthode :
  - DVF+ : 20-50% (défaut : 40%)
  - Comparables vente : 10-30% (défaut : 25%)
  - Additionnelle/Locative : 10-30% (défaut : 20%)
  - Expertise agent : 10-30% (défaut : 15%)
- [ ] La somme des poids doit toujours égaler 100%
- [ ] Un message d'erreur s'affiche si la somme != 100%
- [ ] Le calcul de l'estimation pondérée se fait en temps réel
- [ ] L'estimation finale s'affiche en grand format avec fourchette (±10%)
- [ ] Un bouton "Réinitialiser" remet les valeurs par défaut
- [ ] Les poids sont sauvegardés dans le session state

## Notes techniques

### Dépendances
- Session state avec résultats des 4 méthodes
- Streamlit sliders avec contrainte somme = 100%
- Module de calcul pondération

### Stack technique
- **Frontend:** Streamlit (st.slider, st.metric)
- **Calculs:** Python, numpy
- **Validation:** Contrainte somme = 100%

### Estimation détaillée
- Interface sliders avec contrainte : 3h
- Calcul pondération temps réel : 2h
- Validation et gestion erreurs : 2h
- Affichage résultats : 2h
- Tests et optimisation : 3h
- **Total : 12h (7 SP)**

### Formule de calcul

```python
def calculer_estimation_ponderee(
    estimation_dvf: float,
    estimation_vente: float,
    estimation_additionnelle: float,  # ou locative
    poids_dvf: float,
    poids_vente: float,
    poids_additionnelle: float,
    poids_expertise: float,
    ajustement_expertise: float = 0.0  # % d'ajustement manuel
) -> dict:
    """
    Calcule l'estimation finale pondérée.

    Args:
        estimation_dvf: Estimation méthode DVF+
        estimation_vente: Estimation comparables vente
        estimation_additionnelle: Estimation méthode additionnelle/locative
        poids_*: Poids en % (somme = 100)
        ajustement_expertise: Ajustement manuel agent (-20% à +20%)

    Returns:
        dict avec estimation finale, fourchette, détails
    """
    # Validation somme poids
    somme_poids = poids_dvf + poids_vente + poids_additionnelle + poids_expertise
    if abs(somme_poids - 100) > 0.01:
        raise ValueError(f"La somme des poids doit être 100% (actuel: {somme_poids}%)")

    # Calcul base pondérée (sans expertise)
    poids_total_methodes = poids_dvf + poids_vente + poids_additionnelle

    estimation_base = (
        (estimation_dvf * poids_dvf +
         estimation_vente * poids_vente +
         estimation_additionnelle * poids_additionnelle) / poids_total_methodes
    )

    # Application ajustement expertise
    estimation_avec_expertise = estimation_base * (1 + ajustement_expertise / 100)

    # Calcul final pondéré
    estimation_finale = (
        estimation_base * (100 - poids_expertise) / 100 +
        estimation_avec_expertise * poids_expertise / 100
    )

    # Fourchette ±10%
    fourchette_min = estimation_finale * 0.90
    fourchette_max = estimation_finale * 1.10

    return {
        "estimation_finale": round(estimation_finale, 0),
        "fourchette_min": round(fourchette_min, 0),
        "fourchette_max": round(fourchette_max, 0),
        "details": {
            "dvf": round(estimation_dvf * poids_dvf / 100, 0),
            "vente": round(estimation_vente * poids_vente / 100, 0),
            "additionnelle": round(estimation_additionnelle * poids_additionnelle / 100, 0),
            "expertise": round(estimation_avec_expertise * poids_expertise / 100, 0)
        }
    }
```

### Interface Streamlit

```python
st.header("Synthèse et Pondération")

# Récupération estimations depuis session state
estimation_dvf = st.session_state.get('estimation_dvf', 0)
estimation_vente = st.session_state.get('estimation_vente', 0)
estimation_additionnelle = st.session_state.get('estimation_additionnelle', 0)

# Affichage estimations individuelles
col1, col2, col3 = st.columns(3)
col1.metric("DVF+ (Vendues)", f"{estimation_dvf:,.0f} €")
col2.metric("Comparables Vente", f"{estimation_vente:,.0f} €")
col3.metric("Méthode Additionnelle", f"{estimation_additionnelle:,.0f} €")

st.divider()

# Sliders de pondération
st.subheader("Pondération des méthodes")

col1, col2 = st.columns(2)
with col1:
    poids_dvf = st.slider("DVF+ (%)", min_value=20, max_value=50, value=40, step=5)
    poids_vente = st.slider("Comparables Vente (%)", min_value=10, max_value=30, value=25, step=5)

with col2:
    poids_additionnelle = st.slider("Méthode Additionnelle (%)", min_value=10, max_value=30, value=20, step=5)
    poids_expertise = st.slider("Expertise Agent (%)", min_value=10, max_value=30, value=15, step=5)

# Validation somme = 100%
somme_poids = poids_dvf + poids_vente + poids_additionnelle + poids_expertise
if somme_poids != 100:
    st.error(f"⚠️ La somme des poids doit être 100% (actuel: {somme_poids}%)")
else:
    st.success(f"✓ Total: {somme_poids}%")

# Ajustement expertise
ajustement_expertise = st.slider(
    "Ajustement expertise (%)",
    min_value=-20,
    max_value=20,
    value=0,
    step=5,
    help="Ajustement manuel basé sur votre connaissance du marché local"
)

# Calcul estimation finale
if somme_poids == 100:
    result = calculer_estimation_ponderee(
        estimation_dvf,
        estimation_vente,
        estimation_additionnelle,
        poids_dvf,
        poids_vente,
        poids_additionnelle,
        poids_expertise,
        ajustement_expertise
    )

    st.divider()

    # Affichage estimation finale
    st.subheader("Estimation Finale")
    col1, col2, col3 = st.columns(3)
    col1.metric("Fourchette Basse", f"{result['fourchette_min']:,.0f} €")
    col2.metric("ESTIMATION", f"{result['estimation_finale']:,.0f} €", delta=None)
    col3.metric("Fourchette Haute", f"{result['fourchette_max']:,.0f} €")

    # Détails contribution
    with st.expander("Voir le détail des contributions"):
        st.write("**Contribution de chaque méthode à l'estimation finale :**")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("DVF+", f"{result['details']['dvf']:,.0f} €", f"{poids_dvf}%")
        col2.metric("Vente", f"{result['details']['vente']:,.0f} €", f"{poids_vente}%")
        col3.metric("Additionnelle", f"{result['details']['additionnelle']:,.0f} €", f"{poids_additionnelle}%")
        col4.metric("Expertise", f"{result['details']['expertise']:,.0f} €", f"{poids_expertise}%")

# Bouton réinitialiser
if st.button("Réinitialiser les poids"):
    st.session_state.poids_dvf = 40
    st.session_state.poids_vente = 25
    st.session_state.poids_additionnelle = 20
    st.session_state.poids_expertise = 15
    st.session_state.ajustement_expertise = 0
    st.rerun()
```

### Contrainte somme = 100%

```python
# Validation en temps réel
def validate_weights_sum(poids_list: list) -> bool:
    return abs(sum(poids_list) - 100) < 0.01

# Ajustement automatique (optionnel)
def auto_adjust_weights(poids_list: list) -> list:
    """
    Ajuste automatiquement le dernier poids pour atteindre 100%.
    """
    current_sum = sum(poids_list[:-1])
    poids_list[-1] = 100 - current_sum
    return poids_list
```

### Valeurs par défaut optimisées

| Méthode | Poids défaut | Justification |
|---------|--------------|---------------|
| DVF+ | 40% | Données historiques fiables |
| Comparables vente | 25% | Reflet marché actuel |
| Additionnelle/Locative | 20% | Validation technique |
| Expertise agent | 15% | Connaissance locale |

### Risques
- Somme != 100% → Blocage calcul + message clair
- Poids expertise trop élevé → Limite 30% max
- Ajustement expertise biaisé → Limite ±20%

---

**Lien EPIC parent:** [README.md](./README.md)
