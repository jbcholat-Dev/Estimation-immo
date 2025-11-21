#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Component: Tableau comparables avec filtres
US3 - Filtrer comparables manuellement
"""

import streamlit as st
import pandas as pd
from typing import Optional


def render_comparables_table(
    comparables_df: pd.DataFrame,
    estimation_callback: callable,
    bien_params: dict,
    show_adjusted_price: bool = False
) -> None:
    """
    Affiche tableau interactif des comparables avec filtres et recalcul.

    Args:
        comparables_df: DataFrame avec colonnes: idmutation, datemut, valeurfonc, sbati, distance_km, score
        estimation_callback: Fonction callback pour recalcul estimation avec comparables filtrés
        bien_params: Dict paramètres bien (pour recalcul)
        show_adjusted_price: Si True, affiche la colonne 'prix_ajuste'
    """

    if comparables_df is None or len(comparables_df) == 0:
        st.warning("⚠️ Aucun comparable disponible")
        return

    # === SECTION 1 : FILTRES ===
    with st.expander("🔍 Filtres avancés", expanded=False):
        col1, col2, col3 = st.columns(3)

        with col1:
            score_min = st.slider(
                "Score minimum",
                min_value=0,
                max_value=100,
                value=40,
                step=5,
                help="Filtrer comparables par score de similarité"
            )

        with col2:
            distance_max = st.slider(
                "Distance maximum (km)",
                min_value=1,
                max_value=20,
                value=10,
                step=1,
                help="Distance maximale depuis le bien"
            )

        with col3:
            prix_min_filter = st.number_input(
                "Prix minimum (€)",
                min_value=0,
                value=0,
                step=10000,
                help="Filtrer par prix minimum"
            )

        col1, col2 = st.columns(2)

        with col1:
            prix_max_filter = st.number_input(
                "Prix maximum (€)",
                min_value=0,
                value=1000000,
                step=10000,
                help="Filtrer par prix maximum"
            )

        with col2:
            anciennete_max = st.number_input(
                "Ancienneté max (mois)",
                min_value=1,
                value=36,
                step=6,
                help="Transactions de moins de X mois"
            )

    # === SECTION 2 : APPLICATION FILTRES ===
    df_filtered = comparables_df.copy()

    # Appliquer filtres
    if 'score' in df_filtered.columns:
        df_filtered = df_filtered[df_filtered['score'] >= score_min]

    if 'distance_km' in df_filtered.columns:
        df_filtered = df_filtered[df_filtered['distance_km'] <= distance_max]

    if 'valeurfonc' in df_filtered.columns:
        df_filtered = df_filtered[
            (df_filtered['valeurfonc'] >= prix_min_filter) &
            (df_filtered['valeurfonc'] <= prix_max_filter)
        ]

    # === SECTION 3 : AFFICHAGE TABLEAU (DATA EDITOR) ===
    
    # Ajouter colonne de sélection par défaut True
    if 'selection' not in df_filtered.columns:
        df_filtered.insert(0, 'selection', True)

    # Calcul du nombre de pièces (logique dérivée des colonnes nb*pp)
    def calculate_pieces(row):
        # Si nb_pieces existe déjà (fallback), on le garde
        if 'nb_pieces' in row and pd.notnull(row['nb_pieces']):
            return row['nb_pieces']
            
        type_bien = str(row.get('libtypbien', '')).upper()
        
        # Helper pour récupérer valeur safe (0 si NaN ou None)
        def get_val(col):
            val = row.get(col, 0)
            return 0 if pd.isna(val) else val
        
        if 'MAISON' in type_bien:
            if get_val('nbmai5pp') > 0: return 5
            if get_val('nbmai4pp') > 0: return 4
            if get_val('nbmai3pp') > 0: return 3
            if get_val('nbmai2pp') > 0: return 2
            if get_val('nbmai1pp') > 0: return 1
        elif 'APPARTEMENT' in type_bien:
            if get_val('nbapt5pp') > 0: return 5
            if get_val('nbapt4pp') > 0: return 4
            if get_val('nbapt3pp') > 0: return 3
            if get_val('nbapt2pp') > 0: return 2
            if get_val('nbapt1pp') > 0: return 1
            
        return row.get('nblocmut', 0) # Fallback sur nb locaux

    # Appliquer le calcul si les colonnes sont présentes
    cols_to_check = ['nbmai5pp', 'nbapt5pp'] # Vérif rapide si colonnes existent
    if any(col in df_filtered.columns for col in cols_to_check):
        df_filtered['nb_pieces'] = df_filtered.apply(calculate_pieces, axis=1)

    # Préparer colonnes pour affichage
    display_cols = ['selection']
    
    # Score en 2ème position (renommé Similarité)
    if 'score' in df_filtered.columns:
        display_cols.append('score')
    
    if 'adresse' in df_filtered.columns:
        display_cols.append('adresse')
    if 'libtypbien' in df_filtered.columns:
        display_cols.append('libtypbien')
    if 'datemut' in df_filtered.columns:
        display_cols.append('datemut')
    if 'valeurfonc' in df_filtered.columns:
        display_cols.append('valeurfonc')
    
    # Ajout colonne Prix Ajusté
    if show_adjusted_price and 'prix_ajuste' in df_filtered.columns:
        display_cols.append('prix_ajuste')

    if 'sbati' in df_filtered.columns:
        display_cols.append('sbati')
    if 'prix_m2' in df_filtered.columns:
        display_cols.append('prix_m2')
    if 'nb_pieces' in df_filtered.columns:
        display_cols.append('nb_pieces')
    if 'distance_km' in df_filtered.columns:
        display_cols.append('distance_km')


    df_display = df_filtered[display_cols].copy()

    # Formatter colonnes
    col_config = {
        "selection": st.column_config.CheckboxColumn(
            "Utiliser",
            help="Sélectionner pour inclure dans l'estimation",
            default=True
        )
    }
    if 'score' in df_display.columns:
        col_config['score'] = st.column_config.NumberColumn(
            "Similarité",
            format="%.0f",
            width="small"
        )
    if 'adresse' in df_display.columns:
        col_config['adresse'] = st.column_config.TextColumn("Adresse", width="large")
    if 'libtypbien' in df_display.columns:
        col_config['libtypbien'] = st.column_config.TextColumn("Type", width="medium")
    if 'datemut' in df_display.columns:
        col_config['datemut'] = st.column_config.TextColumn("Date vente", width="small")
    if 'valeurfonc' in df_display.columns:
        col_config['valeurfonc'] = st.column_config.NumberColumn(
            "Prix vente",
            format="%,.0f €",
            width="medium"
        )
    if 'prix_ajuste' in df_display.columns:
        col_config['prix_ajuste'] = st.column_config.NumberColumn(
            "Prix Ajusté",
            format="%,.0f €",
            width="medium",
            help="Prix ajusté selon taux d'emprunt"
        )
    if 'sbati' in df_display.columns:
        col_config['sbati'] = st.column_config.NumberColumn(
            "Surface (m²)",
            format="%.0f",
            width="small"
        )
    if 'prix_m2' in df_display.columns:
        col_config['prix_m2'] = st.column_config.NumberColumn(
            "Prix/m²",
            format="%,.0f €",
            width="small"
        )
    if 'nb_pieces' in df_display.columns:
        col_config['nb_pieces'] = st.column_config.NumberColumn(
            "Nb pièces",
            format="%.0f",
            width="small",
            help="Nombre de pièces principales (estimé)"
        )
    if 'score' in df_display.columns:
        col_config['score'] = st.column_config.NumberColumn(
            "Similarité",
            format="%.0f",
            width="small"
        )
    if 'distance_km' in df_display.columns:
        col_config['distance_km'] = st.column_config.NumberColumn(
            "Distance (km)",
            format="%.1f",
            width="small"
        )

    # Afficher data editor
    edited_df = st.data_editor(
        df_display,
        use_container_width=True,
        column_config=col_config,
        height=400,
        hide_index=True,
        num_rows="fixed"
    )

    # Filtrer sur la sélection utilisateur
    selected_rows = edited_df[edited_df['selection'] == True]
    
    # Mettre à jour df_filtered pour les stats et le callback
    # On doit mapper les lignes sélectionnées au df original filtré
    # Comme on a caché l'index, on suppose que l'ordre est préservé ou on utilise l'index original
    # Ici edited_df a le même index que df_filtered car on a fait un copy()
    
    # Récupérer les indices sélectionnés
    selected_indices = selected_rows.index
    df_final_selection = df_filtered.loc[selected_indices]

    st.markdown(f"**✅ {len(df_final_selection)} / {len(comparables_df)} comparables utilisés pour l'estimation**")

    st.markdown("---")

    # === SECTION 4 : STATISTIQUES (Sur sélection) ===
    st.markdown("### 📊 Statistiques comparables sélectionnés")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        if 'valeurfonc' in df_final_selection.columns:
            prix_median = df_final_selection['valeurfonc'].median()
            st.metric("Prix médian", f"{prix_median:,.0f}€")

    with col2:
        if 'prix_m2' in df_final_selection.columns:
            prix_m2_median = df_final_selection['prix_m2'].median()
            st.metric("Prix médian/m²", f"{prix_m2_median:,.0f}€")

    with col3:
        if 'sbati' in df_final_selection.columns:
            surface_moy = df_final_selection['sbati'].mean()
            st.metric("Surface moy", f"{surface_moy:.0f}m²")

    with col4:
        if 'distance_km' in df_final_selection.columns:
            distance_moy = df_final_selection['distance_km'].mean()
            st.metric("Distance moy", f"{distance_moy:.1f}km")

    with col5:
        if 'score' in df_final_selection.columns:
            score_moy = df_final_selection['score'].mean()
            st.metric("Score moy", f"{score_moy:.0f}")

    st.markdown("---")

    # === SECTION 4.5 : ESTIMATION SIMPLE ===
    st.markdown("### 💰 Estimation du bien")
    
    if 'prix_m2' in df_final_selection.columns:
        prix_m2_median = df_final_selection['prix_m2'].median()
        surface_bien = bien_params.get('surface', 0)
        
        if surface_bien > 0:
            estimation_simple = prix_m2_median * surface_bien
            
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col1:
                st.metric(
                    "Surface du bien",
                    f"{surface_bien:.0f} m²"
                )
            
            with col2:
                st.metric(
                    "Prix médian/m²",
                    f"{prix_m2_median:,.0f} €"
                )
            
            with col3:
                st.metric(
                    "Valeur estimée",
                    f"{estimation_simple:,.0f} €",
                    help="Calcul: Surface × Prix médian/m²"
                )
            
            st.info(
                f"💡 **Calcul**: {surface_bien:.0f} m² × {prix_m2_median:,.0f} €/m² = **{estimation_simple:,.0f} €**"
            )
        else:
            st.warning("⚠️ Surface du bien non définie")
    else:
        st.warning("⚠️ Prix au m² non disponible pour les comparables sélectionnés")

    st.markdown("---")

    # === SECTION 5 : RECALCUL ===
    st.markdown("### 🔄 Recalculer estimation")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.info(
            "💡 **Utiliser la sélection**\n\n"
            "Décochez les comparables non pertinents dans le tableau ci-dessus "
            "puis cliquez sur Recalculer."
        )

    with col2:
        if st.button("🚀 Recalculer", use_container_width=True):
            if len(df_final_selection) > 0:
                # Convertir filtrés en list de dicts pour estimation_callback
                comparables_list = df_final_selection.to_dict('records')

                # Appeler callback
                estimation_callback(
                    latitude=bien_params['latitude'],
                    longitude=bien_params['longitude'],
                    surface=bien_params['surface'],
                    type_bien=bien_params['type_bien'],
                    comparables=comparables_list,
                    filtered=True
                )
                st.rerun()
            else:
                st.error("❌ Sélectionnez au moins 1 comparable")
