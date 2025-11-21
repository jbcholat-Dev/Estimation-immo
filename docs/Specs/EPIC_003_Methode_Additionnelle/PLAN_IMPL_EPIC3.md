# Plan d'implémentation : EPIC 3 - Méthode Additionnelle (Maisons)

Ce plan découpe l'implémentation de l'EPIC 3 en phases séquentielles pour une livraison incrémentale et testable. L'objectif est d'estimer la valeur d'une maison en calculant séparément la valeur du terrain et celle de la construction.

## Phase 1 : Logique de Calcul et Récupération des Données (Backend)

1.  **Mise à jour du `perplexity_retriever.py`** :
    *   Ajouter une nouvelle fonction asynchrone `get_local_market_prices(city: str, postal_code: str) -> dict`.
    *   Cette fonction utilisera Perplexity pour récupérer le **prix au m² du terrain constructible** et le **prix au m² pour une construction neuve** dans une localité donnée, comme spécifié dans la User Story US-10.
    *   La fonction doit gérer les erreurs d'API et le parsing de la réponse JSON.

2.  **Créer un module de calcul `src/estimation_methods/additional_method.py`** :
    *   Créer ce nouveau dossier et fichier pour héberger la logique métier.
    *   Implémenter la fonction principale `calculate_additional_method(...) -> dict`.
    *   Cette fonction intégrera la logique des **coefficients de vétusté** (basés sur l'âge du bien) et des **coefficients de finition** (Basique, Standard, Haut de gamme).
    *   La formule finale sera : `Estimation = (Surface terrain × Prix/m² terrain) + (Surface habitable × Prix/m² construction × Coef. Vétusté × Coef. Finition)`.

3.  **Tests Unitaires** :
    *   Dans `tests/unit/test_perplexity_retriever.py`, ajouter des tests pour la nouvelle fonction `get_local_market_prices` en simulant ("mockant") la réponse de l'API.
    *   Créer `tests/unit/test_additional_method.py` pour valider la logique de calcul des coefficients et de l'estimation finale avec des valeurs d'entrée fixes.

## Phase 2 : Intégration dans l'Interface Streamlit (Frontend)

1.  **Créer le fichier UI `src/ui/epic_3_additional.py`** :
    *   Créer une fonction `render()` qui ne s'affichera que si le type de bien sélectionné est "Maison".
    *   Dans `main.py`, ajouter un nouvel onglet **"3. Méthode Additionnelle"** qui appelle cette fonction `render()`. L'onglet sera désactivé si le bien n'est pas une maison.

2.  **Construire l'Interface Utilisateur** :
    *   Ajouter les champs de saisie spécifiques à cette méthode : `surface_terrain`, `annee_construction`, et `niveau_finition`.
    *   Ajouter un bouton "Calculer par méthode additionnelle".

3.  **Connecter l'UI à la Logique Backend** :
    *   Au clic du bouton, déclencher l'appel à `get_local_market_prices` puis à `calculate_additional_method`.
    *   Stocker les résultats (valeur terrain, valeur construction, estimation totale) dans `st.session_state` pour une utilisation future dans la synthèse (EPIC 5).
    *   Afficher les résultats à l'aide de `st.metric`.
    *   Implémenter le graphique en barres empilées avec Plotly pour visualiser la décomposition de la valeur (Terrain vs. Construction).

4.  **Tests d'Intégration** :
    *   Ajouter un test dans `tests/integration/` pour vérifier le workflow complet de l'EPIC 3, de la saisie à l'affichage du résultat.
