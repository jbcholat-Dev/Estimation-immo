#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Component: EPIC 2 - Comparables en Vente (API Perplexity)
US-8 / US-9: Recherche biens en vente + visualisation interactive
Phase 5 - Streamlit MVP
"""

import streamlit as st
import pandas as pd
import logging
import asyncio
import folium
from streamlit_folium import st_folium
from datetime import datetime
from io import StringIO
from typing import Optional, Dict, List

from src.perplexity_retriever import get_perplexity_retriever
from src.utils.geocoding import get_coordinates

logger = logging.getLogger(__name__)


@st.cache_resource(show_spinner=False)
def get_perplexity_service():
    """Retourne instance singleton Perplexity (cache)"""
    logger.info("[INFO] Initialisation Perplexity service...")
    try:
        service = get_perplexity_retriever()
        logger.info("[OK] Perplexity service initialisé")
        return service
    except Exception as e:
        logger.error(f"[ERROR] Exception Perplexity init: {e}")
        return None


def _build_property_map(properties: pd.DataFrame, center_lat: float, center_lon: float) -> folium.Map:
    """
    Construit une carte Folium avec marqueurs pour les biens en vente.

    Args:
        properties: DataFrame avec colonnes latitude, longitude, price, address, etc.
        center_lat: Latitude du bien à estimer (center)
        center_lon: Longitude du bien à estimer (center)

    Returns:
        Carte Folium interactive
    """
    # Créer la carte centrée sur le bien
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=13,
        tiles="OpenStreetMap"
    )

    # Ajouter marqueur pour le bien cible (bleu)
    folium.Marker(
        location=[center_lat, center_lon],
        popup="🏠 Bien à estimer",
        tooltip="Bien cible",
        icon=folium.Icon(color="blue", icon="info-sign"),
    ).add_to(m)

    # Déterminer les plages de prix pour la coloration
    if len(properties) > 0 and 'price' in properties.columns:
        price_min = properties['price'].min()
        price_max = properties['price'].max()
        price_range = price_max - price_min if price_max > price_min else 1
    else:
        price_min = price_max = price_range = 0

    # Ajouter marqueurs pour chaque bien (colorés par prix)
    for idx, row in properties.iterrows():
        if pd.isna(row.get('latitude')) or pd.isna(row.get('longitude')):
            continue

        # Déterminer couleur basée sur le prix
        if price_range > 0:
            price_ratio = (row['price'] - price_min) / price_range if 'price' in row else 0.5
        else:
            price_ratio = 0.5

        if price_ratio < 0.33:
            color = "green"
        elif price_ratio < 0.66:
            color = "orange"
        else:
            color = "red"

        # Construire popup avec infos
        popup_text = f"""
        <b>{row.get('address', 'N/A')}</b><br>
        <b>Prix:</b> {row.get('price', 'N/A'):,.0f}€<br>
        <b>Surface:</b> {row.get('surface', 'N/A')} m²<br>
        <b>Type:</b> {row.get('property_type', 'N/A')}<br>
        <b>Pièces:</b> {row.get('rooms', 'N/A')}<br>
        <b>Publication:</b> {row.get('publication_date', 'N/A')}<br>
        """

        if row.get('listing_url'):
            popup_text += f'<a href="{row["listing_url"]}" target="_blank">Voir l\'annonce</a>'

        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=folium.Popup(popup_text, max_width=300),
            tooltip=f"{row.get('address', 'N/A')} - {row.get('price', 'N/A')}€",
            icon=folium.Icon(color=color, icon="home"),
        ).add_to(m)

    return m


def _apply_filters(properties: pd.DataFrame, price_min: Optional[float], price_max: Optional[float],
                  publication_after: Optional[str]) -> pd.DataFrame:
    """
    Applique les filtres au DataFrame des biens.

    Args:
        properties: DataFrame à filtrer
        price_min: Prix minimum (ou None)
        price_max: Prix maximum (ou None)
        publication_after: Date minimale de publication (ou None)

    Returns:
        DataFrame filtré
    """
    filtered = properties.copy()

    if price_min is not None:
        filtered = filtered[filtered['price'] >= price_min]

    if price_max is not None:
        filtered = filtered[filtered['price'] <= price_max]

    if publication_after:
        try:
            filtered = filtered[filtered['publication_date'] >= publication_after]
        except Exception as e:
            logger.warning(f"[WARNING] Erreur filtrage date: {e}")

    return filtered


def _get_csv_download_link(df: pd.DataFrame) -> bytes:
    """
    Convertit un DataFrame en CSV téléchargeable.

    Args:
        df: DataFrame à exporter

    Returns:
        Bytes du fichier CSV
    """
    csv = StringIO()
    df.to_csv(csv, index=False, encoding='utf-8-sig')
    return csv.getvalue().encode('utf-8-sig')


def render():
    """
    Fonction principale pour afficher l'EPIC 2 : Comparables en Vente (Perplexity)
    Utilise les paramètres du bien saisi dans le formulaire principal.
    """
    st.markdown("## 🏪 Comparables en Vente (Web)")
    st.markdown("Biens actuellement en vente trouvés via IA - Perplexity API")

    # --- Vérification: bien_params dans session_state ---
    if 'bien_params' not in st.session_state or st.session_state['bien_params'] is None:
        st.info("""
        ℹ️ **Aucun bien saisie**

        Pour voir les comparables en vente, veuillez d'abord :
        1. Remplir le formulaire dans la barre latérale
        2. Cliquer sur "🚀 Estimer"
        """)
        return

    bien_params = st.session_state['bien_params']

    # --- Initialisation Service Perplexity ---
    perplexity_service = get_perplexity_service()
    if perplexity_service is None:
        st.error("[ERROR] Service Perplexity non initialisé. Vérifiez configuration PERPLEXITY_API_KEY")
        return

    # --- Layout: Sidebar pour filtres ---
    with st.sidebar:
        st.markdown("### 🔍 Filtres - Comparables Vente")

        # Rayon de recherche
        rayon_km = st.slider(
            "Rayon de recherche (km)",
            min_value=1,
            max_value=50,
            value=5,
            step=1,
            help="Rayon autour du bien"
        )

        # Type de bien
        property_type_options = ["all", "apartment", "house", "studio", "townhouse"]
        property_type = st.selectbox(
            "Type de bien",
            options=property_type_options,
            index=0,
            help="Filtrer par type de bien"
        )

        # Fourchette de prix
        st.markdown("**Fourchette de prix (€)**")
        col1, col2 = st.columns(2)
        with col1:
            price_min = st.number_input(
                "Prix min",
                min_value=0,
                value=100000,
                step=50000,
                key="price_min_filter"
            )
        with col2:
            price_max = st.number_input(
                "Prix max",
                min_value=100000,
                value=1000000,
                step=50000,
                key="price_max_filter"
            )

        # Date minimale de publication
        publication_after = st.date_input(
            "Annonces publiées après le",
            value=None,
            help="Laisser vide pour voir toutes les annonces"
        )

        st.markdown("---")

        # Bouton recherche
        search_button = st.button(
            "🔍 Rechercher comparables en vente",
            use_container_width=True,
            type="primary"
        )

    # --- Logique de recherche ---
    if search_button or st.session_state.get('perplexity_results_cached'):
        # Marquer recherche comme déjà effectuée
        st.session_state['perplexity_results_cached'] = True

        # Afficher spinner pendant recherche
        with st.spinner("⏳ Recherche sur le web via Perplexity..."):
            try:
                # Construire la query pour Perplexity
                logger.info(f"[INFO] Recherche Perplexity: {bien_params['address']}")

                # Appel API asynchrone
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

                results = loop.run_until_complete(
                    perplexity_service.search_properties_for_sale(
                        city=bien_params.get('address', '').split(',')[0],  # Extraire ville
                        postal_code=bien_params.get('address', '').split(',')[-1].strip()[:5],  # Extraire code postal
                        property_type=property_type,
                        price_min=price_min,
                        price_max=price_max,
                        radius_km=rayon_km,
                    )
                )

                loop.close()

                if not results:
                    st.warning("⚠️ Aucun bien trouvé avec ces critères.")
                    return

                # Convertir en DataFrame
                results_df = pd.DataFrame(results)

                # Appliquer filtres supplémentaires
                if publication_after:
                    publication_after_str = publication_after.strftime("%Y-%m-%d")
                    results_df = _apply_filters(results_df, None, None, publication_after_str)

                st.success(f"✅ {len(results_df)} bien(s) trouvé(s)")

                # Stocker dans session_state
                st.session_state['perplexity_results'] = results_df

            except Exception as e:
                st.error(f"[ERROR] Erreur recherche Perplexity: {e}")
                logger.error(f"Perplexity error: {e}")
                return

    # --- Affichage des résultats (si existent) ---
    if st.session_state.get('perplexity_results') is not None:
        results_df = st.session_state['perplexity_results']

        if len(results_df) == 0:
            st.warning("⚠️ Aucun résultat à afficher.")
            return

        # --- TAB 1: Tableau des résultats ---
        tab1, tab2, tab3 = st.tabs(["📋 Tableau", "🗺️ Carte", "📊 Statistiques"])

        with tab1:
            st.markdown(f"### Résultats: {len(results_df)} bien(s)")

            # Formater le DataFrame pour affichage
            display_df = results_df.copy()

            # Formatter les colonnes
            if 'price' in display_df.columns:
                display_df['price'] = display_df['price'].apply(
                    lambda x: f"{x:,.0f}€" if pd.notna(x) else "N/A"
                )

            if 'surface' in display_df.columns:
                display_df['surface'] = display_df['surface'].apply(
                    lambda x: f"{x:.0f} m²" if pd.notna(x) else "N/A"
                )

            if 'listing_url' in display_df.columns:
                display_df['listing_url'] = display_df['listing_url'].apply(
                    lambda x: f'[Lien](http://{x})' if pd.notna(x) and x else "N/A"
                )

            # Afficher le tableau
            st.dataframe(display_df, use_container_width=True, hide_index=True)

            # Bouton export CSV
            csv_data = _get_csv_download_link(results_df)
            st.download_button(
                label="📥 Télécharger CSV",
                data=csv_data,
                file_name=f"comparables_vente_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )

        # --- TAB 2: Carte ---
        with tab2:
            st.markdown(f"### Carte - {len(results_df)} biens")

            try:
                # Construire la carte
                m = _build_property_map(
                    results_df,
                    center_lat=bien_params['latitude'],
                    center_lon=bien_params['longitude']
                )

                # Afficher la carte
                st_folium(m, width=1200, height=600)

            except Exception as e:
                st.error(f"[ERROR] Erreur affichage carte: {e}")
                logger.error(f"Map error: {e}")

        # --- TAB 3: Statistiques ---
        with tab3:
            st.markdown(f"### Statistiques - {len(results_df)} biens")

            col1, col2, col3, col4 = st.columns(4)

            # Prix
            if 'price' in results_df.columns and results_df['price'].notna().any():
                with col1:
                    st.metric(
                        "Prix moyen",
                        f"{results_df['price'].mean():,.0f}€"
                    )

            # Surface
            if 'surface' in results_df.columns and results_df['surface'].notna().any():
                with col2:
                    st.metric(
                        "Surface moy.",
                        f"{results_df['surface'].mean():.0f} m²"
                    )

            # Pièces
            if 'rooms' in results_df.columns and results_df['rooms'].notna().any():
                with col3:
                    st.metric(
                        "Pièces moy.",
                        f"{results_df['rooms'].mean():.1f}"
                    )

            # Prix au m²
            if 'price' in results_df.columns and 'surface' in results_df.columns:
                results_df['price_per_m2'] = results_df['price'] / results_df['surface']
                with col4:
                    st.metric(
                        "Prix/m² moyen",
                        f"{results_df['price_per_m2'].mean():,.0f}€/m²"
                    )

            # Distribution par type
            st.markdown("---")
            if 'property_type' in results_df.columns:
                st.markdown("**Distribution par type**")
                type_dist = results_df['property_type'].value_counts()
                st.bar_chart(type_dist)

            # Distribution par prix
            if 'price' in results_df.columns:
                st.markdown("**Distribution des prix**")
                st.histogram(results_df['price'], bins=20)


if __name__ == "__main__":
    render()
