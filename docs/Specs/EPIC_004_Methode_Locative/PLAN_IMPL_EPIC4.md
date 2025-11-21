# Plan d'implémentation : EPIC 4 - Méthode Locative (Appartements)

Ce plan structure l'implémentation de l'EPIC 4, qui vise à estimer la valeur d'un appartement en se basant sur son rendement locatif.

## Phase 1 : Logique de Calcul et Récupération des Données (Backend)

1.  **Mise à jour du `perplexity_retriever.py`** :
    *   Ajouter une fonction asynchrone `get_average_rental_yield(city: str, postal_code: str) -> float`.
    *   Cette fonction interrogera Perplexity pour obtenir le **taux de rendement locatif moyen** pour un appartement dans une zone donnée.
    *   Prévoir une valeur de secours (fallback) si l'API ne retourne pas de réponse valide (par exemple, un taux moyen de 4.5% pour la zone Chablais/Annemasse).

2.  **Créer un module de calcul `src/estimation_methods/rental_method.py`** :
    *   Créer ce nouveau fichier pour la logique métier de l'EPIC 4.
    *   Implémenter la fonction `calculate_rental_method(...) -> dict` qui contiendra les formules de calcul spécifiées dans la User Story US-11 :
        *   Rendement brut et net.
        *   Estimation par capitalisation (`Loyer annuel / Taux de rendement de la zone`).
        *   Indicateur de comparaison par rapport à la moyenne de la zone.

3.  **Tests Unitaires** :
    *   Dans `tests/unit/test_perplexity_retriever.py`, ajouter des tests pour `get_average_rental_yield`.
    *   Créer `tests/unit/test_rental_method.py` pour valider les formules de calcul des rendements et de l'estimation.

## Phase 2 : Intégration dans l'Interface Streamlit (Frontend)

1.  **Créer le fichier UI `src/ui/epic_4_rental.py`** :
    *   Créer une fonction `render()` qui ne s'affichera que si le type de bien sélectionné est "Appartement".
    *   Dans `main.py`, ajouter un onglet **"4. Méthode Locative"**, qui sera désactivé si le bien n'est pas un appartement.

2.  **Construire l'Interface Utilisateur** :
    *   Ajouter les champs de saisie spécifiques : `loyer_mensuel_potentiel`, `charges_annuelles`, `taxe_fonciere`, `autres_frais`.
    *   Ajouter un bouton "Calculer par méthode locative".

3.  **Connecter l'UI à la Logique Backend** :
    *   Au clic du bouton, appeler `get_average_rental_yield` puis `calculate_rental_method`.
    *   Stocker le résultat dans `st.session_state`.
    *   Afficher les indicateurs clés (Rendement brut, Rendement net, etc.) avec `st.metric`. Utiliser le paramètre `delta` pour afficher visuellement la comparaison avec la moyenne de la zone.
    *   Implémenter le graphique en barres avec Plotly pour comparer les rendements (Brut, Net, Zone).
    *   Ajouter un `st.info` avec un tooltip expliquant les formules de calcul.

4.  **Tests d'Intégration** :
    *   Ajouter un test dans `tests/integration/` pour l'EPIC 4 afin de valider le workflow complet.
