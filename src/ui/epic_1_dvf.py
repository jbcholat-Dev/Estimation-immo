import streamlit as st
import pandas as pd
import logging
from src.supabase_data_retriever import SupabaseDataRetriever
from src.estimation_algorithm import EstimationAlgorithm
from src.streamlit_components.form_input import render_form_input
from src.streamlit_components.comparables_table import render_comparables_table
from src.streamlit_components.map_viewer import render_map_viewer
from src.streamlit_components.pdf_export import render_pdf_export
from src.utils.finance import calculate_adjusted_price
from datetime import datetime

logger = logging.getLogger(__name__)

# ===================================
# CACHE & SERVICES
# ===================================

@st.cache_resource(show_spinner=False)
def init_supabase_retriever():
    """Initialiser connexion Supabase (cache)"""
    try:
        retriever = SupabaseDataRetriever()
        if retriever.test_connection():
            return retriever
        return retriever
    except Exception as e:
        logger.error(f"[ERROR] Exception Supabase: {e}")
        return None

@st.cache_resource
def init_estimation_algorithm():
    """Initialiser algorithme estimation"""
    return EstimationAlgorithm()

def render():
    """
    Fonction principale pour afficher l'EPIC 1 : Comparables Vendus (DVF+)
    """
    st.markdown("## 🏘️ Comparables Vendus (DVF+)")
    st.markdown("Analyse des transactions passées similaires (Base DVF+ 2014-2025)")

    # --- Initialisation Services ---
    retriever = init_supabase_retriever()
    estimator = init_estimation_algorithm()

    if not retriever or not estimator:
        st.error("Erreur d'initialisation des services backend.")
        return

    # --- Layout: Sidebar pour filtres globaux de l'EPIC ---
    with st.sidebar:
        st.markdown("### 🔍 Paramètres DVF+")
        rayon_km = st.slider(
            "Rayon de recherche (km)",
            min_value=1, max_value=20, value=3, step=1
        )
        anciennete_max_ans = st.slider(
            "Ancienneté max (ans)",
            min_value=1, max_value=10, value=3, step=1
        )
        surface_tolerance_pct = st.slider(
            "Tolérance surface (%)",
            min_value=10, max_value=50, value=20, step=5
        )
        st.markdown("---")

        st.markdown("---")
        
        st.markdown("### 📝 Votre Bien")
        # Formulaire dans la sidebar (sidebar=True)
        well_params = render_form_input(sidebar=True)
        
        if well_params:
            st.session_state['bien_params'] = well_params
            # Auto-trigger analysis when form is submitted via the component's "Estimer" button
            st.session_state['trigger_dvf_analysis'] = True

    # --- Layout: Résultats (Main Area) ---
    # Plus de colonnes, tout l'espace pour les résultats
    container_results = st.container()
    
    # --- Logique d'Analyse ---
    if st.session_state.get('trigger_dvf_analysis') and st.session_state.get('bien_params'):
        bien_params = st.session_state['bien_params']
        
        with container_results:
            # Paramètres actuels pour détection de changement
            current_params = {
                "lat": bien_params['latitude'],
                "lon": bien_params['longitude'],
                "surface": bien_params['surface'],
                "type": bien_params['type_bien'],
                "rayon": rayon_km,
                "anciennete": anciennete_max_ans,
                "tolerance": surface_tolerance_pct
            }

            # Vérifier si on doit relancer la recherche (nouveaux paramètres)
            last_params = st.session_state.get('last_dvf_params')
            should_refresh = (last_params != current_params) or ('comparables_df' not in st.session_state)

            if should_refresh:
                # 1. Récupération Comparables (Seulement si params changent)
                with st.spinner("Recherche des comparables DVF+..."):
                    try:
                        comparables_df = retriever.get_comparables(
                            latitude=bien_params['latitude'],
                            longitude=bien_params['longitude'],
                            type_bien=bien_params['type_bien'],
                            surface_min=bien_params['surface'] * (1 - surface_tolerance_pct / 100),
                            surface_max=bien_params['surface'] * (1 + surface_tolerance_pct / 100),
                            rayon_km=rayon_km,
                            annees=anciennete_max_ans,
                            limit=100
                        )
                        st.session_state['comparables_df'] = comparables_df
                        st.session_state['last_dvf_params'] = current_params
                    except Exception as e:
                        st.error(f"Erreur récupération comparables: {e}")
                        return

                # 2. Calcul Estimation Initiale (Seulement si params changent)
                if not comparables_df.empty:
                    with st.spinner("Calcul du scoring et de l'estimation..."):
                        try:
                            comparables_list = comparables_df.to_dict('records')
                            estimation_result = estimator.estimate(
                                target_latitude=bien_params['latitude'],
                                target_longitude=bien_params['longitude'],
                                target_surface=bien_params['surface'],
                                target_type=bien_params['type_bien'],
                                comparables=comparables_list
                            )
                            st.session_state['estimation_result'] = estimation_result
                            
                            # Mise à jour DF avec scores (CRITIQUE pour affichage colonne Score)
                            if estimation_result.get('success') and estimation_result.get('comparables_with_scores'):
                                st.session_state['comparables_df'] = pd.DataFrame(estimation_result['comparables_with_scores'])
                            
                        except Exception as e:
                            st.error(f"Erreur calcul estimation: {e}")
                            return
                else:
                    st.warning("Aucun comparable trouvé avec ces critères.")
                    st.session_state['estimation_result'] = None
            
            # Récupérer le DF du state (soit frais, soit existant)
            comparables_df = st.session_state.get('comparables_df', pd.DataFrame())

            # 3. Affichage Résultats
            if st.session_state.get('estimation_result') and st.session_state['estimation_result'].get('success'):
                
                # Toggle Prix Ajusté
                show_adjusted = st.toggle(
                    "📉 Afficher prix ajustés selon taux d'emprunt",
                    value=True,
                    help="Ajuste les prix de vente historiques en fonction de l'évolution des taux d'emprunt (Source: Banque de France)"
                )

                # Préparation Dataframe Comparables
                df_comparables = st.session_state['comparables_df'].copy()
                
                # Calcul Prix Ajusté
                if not df_comparables.empty:
                    df_comparables['prix_ajuste'] = df_comparables.apply(
                        lambda row: calculate_adjusted_price(
                            row['valeurfonc'],
                            pd.to_datetime(row['datemut'], dayfirst=True)
                        ),
                        axis=1
                    )

                # Callback pour recalcul (si filtrage dans le tableau)
                def recalculate_callback(latitude, longitude, surface, type_bien, comparables, filtered=False):
                    new_est = estimator.estimate(latitude, longitude, surface, type_bien, comparables)
                    st.session_state['estimation_result'] = new_est
                
                # Layout: Carte d'abord, puis Tableau
                
                # A. Carte Interactive (US-003)
                st.subheader("📍 Carte des Comparables")
                
                # Utiliser les comparables filtrés/scorés pour la carte si disponibles
                if st.session_state.get('estimation_result') and st.session_state['estimation_result'].get('comparables_with_scores'):
                    df_map = pd.DataFrame(st.session_state['estimation_result']['comparables_with_scores'])
                else:
                    df_map = df_comparables

                render_map_viewer(
                    bien_coords=(bien_params['latitude'], bien_params['longitude']),
                    comparables_df=df_map,
                    rayon_km=rayon_km,
                    bien_address=bien_params.get('address')
                )
                
                st.markdown("---")

                # B. Tableau Comparables (US-005)
                st.subheader("📋 Liste des Comparables")
                render_comparables_table(
                    df_comparables,
                    recalculate_callback,
                    bien_params,
                    show_adjusted_price=show_adjusted
                )

                st.markdown("---")

                # C. Export PDF
                render_pdf_export(
                    st.session_state['estimation_result'],
                    df_comparables,
                    bien_address=bien_params.get('address')
                )

    elif not st.session_state.get('bien_params'):
        with container_results:
            st.info("👈 Veuillez saisir les informations du bien dans la barre latérale et lancer l'analyse.")
