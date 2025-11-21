# Plan d'implémentation : EPIC 2 - Comparables en Vente (Perplexity)

Voici une proposition de plan pour implémenter l'EPIC 2, en découpant le travail en phases logiques et séquentielles, afin de construire la fonctionnalité de manière incrémentale et testable.

## Phase 1 : Création du service de recherche (Logique Backend)

L'objectif de cette phase est de créer une fonction robuste pour interroger l'API Perplexity, indépendamment de l'interface Streamlit.

1.  **Configuration** :
    *   Ajouter la clé `PERPLEXITY_API_KEY` dans le fichier `.env.example` pour la documentation et s'assurer qu'elle est dans votre `.env` local.
    *   Mettre à jour le module `src/utils/config.py` pour charger cette nouvelle clé.

2.  **Créer un nouveau module `src/perplexity_retriever.py`** :
    *   Ce module sera dédié aux interactions avec l'API Perplexity.
    *   Implémenter une fonction asynchrone `search_properties_for_sale(city: str, postal_code: str, ...) -> list[dict]`, en utilisant `httpx` comme suggéré dans la User Story US-8.
    *   Construire le prompt en suivant le format de l'exemple fourni.
    *   Gérer les erreurs d'API (e.g., `httpx.HTTPStatusError`, timeouts) et retourner une liste vide ou lever une exception claire.

3.  **Implémenter le parsing et l'enrichissement des données** :
    *   Dans le même module, créer une fonction `parse_perplexity_response(response: dict) -> pd.DataFrame` qui transforme la réponse JSON de l'API en un DataFrame Pandas structuré.
    *   Après le parsing, enrichir le DataFrame en y ajoutant les colonnes `latitude` et `longitude` en réutilisant le service de géocodage existant (`src/utils/geocoding.py`).

4.  **Tests unitaires** :
    *   Créer un fichier de test `tests/unit/test_perplexity_retriever.py`.
    *   Utiliser des "mocks" pour simuler les appels à l'API Perplexity et tester la logique de parsing et de gestion d'erreur sans effectuer de vrais appels réseau.

## Phase 2 : Création de la page Streamlit (Interface Frontend)

Avec la logique backend prête, nous pouvons maintenant construire l'interface utilisateur.

1.  **Intégrer le nouvel EPIC dans l'UI principale** :
    *   Créer un nouveau fichier `src/ui/epic_2_perplexity.py`.
    *   Dans `main.py`, ajouter un nouvel onglet (tab) **"2. Comparables en Vente"** qui appellera une fonction `render()` de ce nouveau module.

2.  **Construire le formulaire de recherche** :
    *   Dans `epic_2_perplexity.py`, ajouter les widgets Streamlit dans la sidebar (`st.sidebar`) pour les critères de recherche (localité, code postal, type de bien, fourchette de prix, rayon).
    *   Ajouter un bouton `"Rechercher les biens en vente"`.

3.  **Connecter l'UI à la logique backend** :
    *   Lorsque l'utilisateur clique sur le bouton, appeler la fonction `search_properties_for_sale`.
    *   Afficher un `st.spinner` pendant la recherche.
    *   Stocker le DataFrame résultant dans le `st.session_state` pour éviter de refaire l'appel à chaque interaction de l'utilisateur sur la page.
    *   Afficher le tableau de résultats brut avec `st.dataframe`.

## Phase 3 : Ajout des visualisations interactives et des filtres

Cette phase se concentre sur l'amélioration de l'expérience utilisateur, comme décrit dans la User Story US-9.

1.  **Intégrer la carte Folium** :
    *   Ajouter les filtres de visualisation (fourchette de prix, date de publication) dans le corps principal de la page.
    *   Filtrer le DataFrame stocké en `session_state` en fonction de ces filtres.
    *   Implémenter la logique de la carte Folium :
        *   Ajouter des `folium.Marker` pour chaque propriété.
        *   Personnaliser les popups avec les détails de l'annonce (prix, surface, lien, etc.).
        *   Colorer les marqueurs en fonction du prix.
        *   Afficher la carte avec `st_folium`.

2.  **Améliorer le tableau de données** :
    *   Utiliser la configuration des colonnes (`column_config`) de `st.dataframe` pour formater les prix en euros (€) et rendre les URLs des annonces cliquables.

3.  **Implémenter l'export CSV** :
    *   Ajouter un bouton `st.download_button` qui permet de télécharger le contenu du DataFrame filtré au format CSV.

## Phase 4 : Finalisation et optimisation

1.  **Tests d'intégration** :
    *   Créer `tests/integration/test_epic_2.py` pour simuler le workflow complet : recherche, affichage, filtrage et export.

2.  **Gestion du cache API** :
    *   Pour limiter les coûts et les temps de réponse, envelopper l'appel à `search_properties_for_sale` avec le décorateur `@st.cache_data` de Streamlit, en définissant une durée d'expiration (e.g., 24 heures).

3.  **Documentation** :
    *   Mettre à jour le `PROJECT_STATUS.md` pour refléter l'implémentation de l'EPIC 2.
