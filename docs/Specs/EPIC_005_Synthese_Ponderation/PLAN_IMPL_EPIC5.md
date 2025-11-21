# Plan d'implémentation : EPIC 5 - Synthèse et Pondération

Ce plan détaille les étapes pour implémenter l'EPIC 5, qui consolide toutes les méthodes d'estimation en un rapport final interactif et exportable.

## Phase 1 : Logique de Calcul de Synthèse (Backend)

1.  **Créer un module `src/synthesis_engine.py`** :
    *   Ce module centralisera la logique de consolidation.
    *   Implémenter la fonction `calculate_weighted_estimation(...) -> dict` :
        *   Elle prendra en entrée les estimations des EPICs précédents (stockées dans `st.session_state`) et les poids définis par l'utilisateur.
        *   Elle calculera l'estimation finale pondérée.
    *   Implémenter la fonction `calculate_confidence_score(...) -> dict` :
        *   Elle calculera un score de confiance (0-100%) basé sur des critères comme l'écart-type entre les méthodes, le nombre de comparables trouvés, etc.

2.  **Tests Unitaires** :
    *   Créer `tests/unit/test_synthesis_engine.py`.
    *   Tester la fonction de calcul de pondération et la logique du score de confiance avec des données d'entrée contrôlées.

## Phase 2 : Moteur de Génération de PDF (Backend)

1.  **Créer un module `src/pdf_generator.py`** :
    *   Implémenter une fonction `generate_estimation_report(...)` en utilisant la bibliothèque **ReportLab**.
    *   Cette fonction sera responsable de la mise en page complète du rapport : en-tête, résumé, graphiques, tableaux, et pied de page.
    *   Les graphiques Plotly devront être sauvegardés en tant qu'images temporaires (e.g., `.png`) avant d'être insérés dans le PDF.

2.  **Tests** :
    *   Créer un test simple qui appelle `generate_estimation_report` et vérifie que le fichier PDF est bien créé, non vide, et a une taille de fichier raisonnable.

## Phase 3 : Intégration dans l'Interface Streamlit (Frontend)

1.  **Créer le fichier UI `src/ui/epic_5_synthesis.py`** :
    *   Dans `main.py`, ajouter l'onglet final **"5. Synthèse"**.
    *   Cette interface récupérera toutes les estimations calculées dans les onglets précédents via `st.session_state`.

2.  **Construire l'Interface de Pondération (US-12)** :
    *   Afficher les estimations de chaque méthode.
    *   Ajouter les **sliders de pondération** et implémenter une logique de validation pour s'assurer que leur somme est toujours égale à 100%.
    *   Afficher en temps réel l'estimation finale pondérée et sa fourchette de prix.

3.  **Construire les Visualisations Graphiques (US-13)** :
    *   Créer et afficher les graphiques Plotly :
        *   **Radar chart** pour comparer les 4 méthodes.
        *   **Histogram** pour montrer la distribution des prix des comparables.
        *   **Box plot** pour visualiser la cohérence et les outliers des estimations.
    *   Afficher le score de confiance calculé.

4.  **Intégrer les Exports (PDF et CSV)** :
    *   Ajouter les boutons **"Générer PDF"** et **"Télécharger CSV"**.
    *   Connecter le bouton PDF à la fonction `generate_estimation_report` et gérer le téléchargement du fichier généré.

5.  **Tests d'Intégration** :
    *   Créer un test d'intégration complet pour l'EPIC 5, simulant la récupération des données depuis `session_state`, l'interaction avec les sliders, et le déclenchement des exports.
