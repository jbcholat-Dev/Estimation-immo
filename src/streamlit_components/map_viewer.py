#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Component: Carte Folium interactive
US4 - Visualiser bien + comparables sur carte
"""

import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
from typing import Tuple, Optional


def render_map_viewer(
    bien_coords: Tuple[float, float],
    comparables_df: pd.DataFrame,
    rayon_km: float = 10.0,
    bien_address: Optional[str] = None
) -> None:
    """
    Affiche carte Folium interactive avec bien cible et comparables.

    Args:
        bien_coords: Tuple (latitude, longitude) du bien
        comparables_df: DataFrame avec colonnes: latitude, longitude, valeurfonc, sbati, score, datemut
        rayon_km: Rayon de recherche en km (pour cercle)
        bien_address: Adresse du bien (optionnel, pour popup)
    """

    if not bien_coords or comparables_df is None or len(comparables_df) == 0:
        st.warning("⚠️ Données insuffisantes pour afficher la carte")
        return

    st.markdown("## 🗺️ Carte interactive")

    # Initialiser carte Folium
    m = folium.Map(
        location=bien_coords,
        zoom_start=13,
        tiles="OpenStreetMap"
    )

    # === MARKER BIEN CIBLE (ROUGE) ===
    folium.Marker(
        location=bien_coords,
        popup=folium.Popup(
            f"<b>Bien à estimer</b><br>{bien_address or 'N/A'}",
            max_width=250
        ),
        tooltip="Bien à estimer",
        icon=folium.Icon(color="red", icon="home", prefix="fa")
    ).add_to(m)

    # === CERCLE RAYON RECHERCHE ===
    # Convertir km en degrés (approximation)
    # 1 degré ≈ 111 km
    rayon_degres = rayon_km / 111.0

    folium.Circle(
        location=bien_coords,
        radius=rayon_km * 1000,  # Folium utilise mètres
        color="blue",
        fill=True,
        fillColor="blue",
        fillOpacity=0.1,
        weight=2,
        popup=f"Rayon: {rayon_km}km",
        tooltip=f"Zone de recherche: {rayon_km}km"
    ).add_to(m)

    # === MARKERS COMPARABLES (VERTS) ===
    if 'latitude' in comparables_df.columns and 'longitude' in comparables_df.columns:
        for idx, row in comparables_df.iterrows():
            lat = row['latitude']
            lon = row['longitude']

            # Déterminer couleur/taille par score
            if 'score' in row and row['score'] is not None:
                score = row['score']
                if score >= 80:
                    color = "darkgreen"
                    size = 8
                elif score >= 70:
                    color = "green"
                    size = 7
                elif score >= 60:
                    color = "orange"
                    size = 6
                else:
                    color = "red"
                    size = 5
            else:
                color = "green"
                size = 6

            # Construire popup
            popup_text = "<b>Comparable</b><br>"
            if 'valeurfonc' in row and row['valeurfonc']:
                popup_text += f"Prix: {row['valeurfonc']:,.0f}€<br>"
            if 'sbati' in row and row['sbati']:
                popup_text += f"Surface: {row['sbati']:.0f}m²<br>"
            if 'score' in row and row['score'] is not None:
                popup_text += f"Score: {row['score']:.0f}<br>"
            if 'datemut' in row and row['datemut']:
                popup_text += f"Date: {row['datemut']}<br>"

            folium.CircleMarker(
                location=[lat, lon],
                radius=size,
                popup=folium.Popup(popup_text, max_width=250),
                tooltip=f"Score: {row.get('score', 'N/A')}",
                color=color,
                fill=True,
                fillColor=color,
                fillOpacity=0.7,
                weight=2
            ).add_to(m)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Component: Carte Folium interactive
US4 - Visualiser bien + comparables sur carte
"""

import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
from typing import Tuple, Optional


def render_map_viewer(
    bien_coords: Tuple[float, float],
    comparables_df: pd.DataFrame,
    rayon_km: float = 10.0,
    bien_address: Optional[str] = None
) -> None:
    """
    Affiche carte Folium interactive avec bien cible et comparables.

    Args:
        bien_coords: Tuple (latitude, longitude) du bien
        comparables_df: DataFrame avec colonnes: latitude, longitude, valeurfonc, sbati, score, datemut
        rayon_km: Rayon de recherche en km (pour cercle)
        bien_address: Adresse du bien (optionnel, pour popup)
    """

    if not bien_coords or comparables_df is None or len(comparables_df) == 0:
        st.warning("⚠️ Données insuffisantes pour afficher la carte")
        return

    st.markdown("## 🗺️ Carte interactive")

    # Initialiser carte Folium
    m = folium.Map(
        location=bien_coords,
        zoom_start=13,
        tiles="OpenStreetMap"
    )

    # === MARKER BIEN CIBLE (ROUGE) ===
    folium.Marker(
        location=bien_coords,
        popup=folium.Popup(
            f"<b>Bien à estimer</b><br>{bien_address or 'N/A'}",
            max_width=250
        ),
        tooltip="Bien à estimer",
        icon=folium.Icon(color="red", icon="home", prefix="fa")
    ).add_to(m)

    # === CERCLE RAYON RECHERCHE ===
    # Convertir km en degrés (approximation)
    # 1 degré ≈ 111 km
    rayon_degres = rayon_km / 111.0

    folium.Circle(
        location=bien_coords,
        radius=rayon_km * 1000,  # Folium utilise mètres
        color="blue",
        fill=True,
        fillColor="blue",
        fillOpacity=0.1,
        weight=2,
        popup=f"Rayon: {rayon_km}km",
        tooltip=f"Zone de recherche: {rayon_km}km"
    ).add_to(m)

    # === MARKERS COMPARABLES (VERTS) ===
    if 'latitude' in comparables_df.columns and 'longitude' in comparables_df.columns:
        for idx, row in comparables_df.iterrows():
            lat = row['latitude']
            lon = row['longitude']

            # Déterminer couleur/taille par score
            if 'score' in row and row['score'] is not None:
                score = row['score']
                if score >= 80:
                    color = "darkgreen"
                    size = 8
                elif score >= 70:
                    color = "green"
                    size = 7
                elif score >= 60:
                    color = "orange"
                    size = 6
                else:
                    color = "red"
                    size = 5
            else:
                color = "green"
                size = 6

            # Construire popup
            popup_text = "<b>Comparable</b><br>"
            if 'valeurfonc' in row and row['valeurfonc']:
                popup_text += f"Prix: {row['valeurfonc']:,.0f}€<br>"
            if 'sbati' in row and row['sbati']:
                popup_text += f"Surface: {row['sbati']:.0f}m²<br>"
            if 'score' in row and row['score'] is not None:
                popup_text += f"Score: {row['score']:.0f}<br>"
            if 'datemut' in row and row['datemut']:
                popup_text += f"Date: {row['datemut']}<br>"

            folium.CircleMarker(
                location=[lat, lon],
                radius=size,
                popup=folium.Popup(popup_text, max_width=250),
                tooltip=f"Score: {row.get('score', 'N/A')}",
                color=color,
                fill=True,
                fillColor=color,
                fillOpacity=0.7,
                weight=2
            ).add_to(m)

    # === HEATMAP LEGEND ===
    st.markdown("""
    ### 📍 Légende
    - 🔴 **Bien à estimer** : Propriété à évaluer
    - 🟢 **Comparables** : Transactions similaires
    - 🔵 Cercle bleu : Zone de recherche
    """)

    st.markdown("---")

    # Layout: Carte (70%) + Street View (30%)
    col_map, col_sv = st.columns([0.7, 0.3])

    with col_map:
        # Afficher carte et capturer retour
        map_data = st_folium(m, width="100%", height=500, returned_objects=["last_object_clicked"])

    with col_sv:
        st.markdown("### 📸 Street View")
        
        # Par défaut : Bien cible
        target_lat, target_lon = bien_coords
        display_lat, display_lon = target_lat, target_lon
        caption = "Bien à estimer"
        
        # Si clic détecté
        if map_data and map_data.get("last_object_clicked"):
            clicked = map_data["last_object_clicked"]
            if clicked and 'lat' in clicked and 'lng' in clicked:
                display_lat = clicked['lat']
                display_lon = clicked['lng']
                caption = "Position sélectionnée"
                
                # Essayer de retrouver si c'est un comparable (approximatif par coords)
                # (Optionnel: pour afficher plus d'infos)

        # Générer URL Street View Interactif
        from src.utils.street_view import get_street_view_embed_url
        sv_url = get_street_view_embed_url(display_lat, display_lon)
        
        if sv_url:
            st.components.v1.iframe(sv_url, height=400)
            st.caption(f"📍 {caption} ({display_lat:.4f}, {display_lon:.4f})")
            
            # Lien vers Google Maps
            gmaps_link = f"https://www.google.com/maps/search/?api=1&query={display_lat},{display_lon}"
            st.markdown(f"[🌍 Ouvrir dans Google Maps]({gmaps_link})")
        else:
            st.warning("⚠️ Clé API Google Maps non configurée")
            st.info("Ajoutez GOOGLE_MAPS_API_KEY dans .env")
