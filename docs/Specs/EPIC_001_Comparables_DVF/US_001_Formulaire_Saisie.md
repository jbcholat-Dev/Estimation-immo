# US-1 : Formulaire de saisie

**EPIC:** EPIC-001 - Onglet Comparables Vendues (DVF+)
**Sprint:** 1
**Priorité:** Must Have
**Story Points:** 3 SP

## User Story

En tant qu'agent immobilier, je veux saisir les caractéristiques complètes d'un bien immobilier dans un formulaire structuré, pour obtenir une estimation basée sur des comparables similaires.

## Critères d'acceptation

- [ ] Le formulaire contient tous les champs obligatoires :
  - Adresse complète (rue, code postal, ville)
  - Type de bien (Maison, Appartement, Terrain)
  - Surface habitable (m²)
  - Nombre de pièces
  - DPE (A à G)
- [ ] Le géocodage automatique fonctionne via API Adresse Etalab
- [ ] Les coordonnées GPS sont récupérées et affichées
- [ ] Les champs conditionnels s'affichent selon le type de bien
- [ ] La validation empêche la soumission si des champs obligatoires sont vides
- [ ] Les données sont stockées dans le session state Streamlit
- [ ] Un message de confirmation s'affiche après soumission réussie
- [ ] Le formulaire peut être réinitialisé

## Notes techniques

### Dépendances
- API Adresse Etalab : https://adresse.data.gouv.fr/
- Streamlit : st.form, st.text_input, st.number_input, st.selectbox
- Session state pour persistance des données
- Module utils/geocoding.py

### Stack technique
- **Frontend:** Streamlit
- **Géocodage:** API Adresse Etalab (gratuite, sans clé API)
- **Validation:** Python (Pydantic recommandé)
- **Stockage temporaire:** st.session_state

### Estimation détaillée
- Création formulaire Streamlit : 2h
- Intégration API géocodage : 2h
- Validation et gestion erreurs : 2h
- Tests et debug : 2h
- **Total : 8h (3 SP)**

### Risques
- API Adresse Etalab indisponible → Fallback manuel coordonnées GPS
- Adresse introuvable → Message erreur + saisie manuelle
- Validation côté client insuffisante → Validation serveur obligatoire

### Champs conditionnels
- **Maison uniquement :** Surface terrain, Année construction
- **Appartement uniquement :** Étage, Ascenseur
- **Tous types :** Nombre de pièces, Surface, DPE

---

**Lien EPIC parent:** [README.md](./README.md)
