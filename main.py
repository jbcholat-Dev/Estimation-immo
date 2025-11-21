#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Estimateur Immobilier v2.0 - Main Entry Point
Structure modulaire par EPIC
"""

import streamlit as st
import logging
from src.utils.config import Config

# Configuration logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ===================================
# CONFIGURATION STREAMLIT
# ===================================

st.set_page_config(
    page_title="Estimateur Immobilier 74",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé global
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
        margin-bottom: 2rem;
        border-bottom: 3px solid #1f77b4;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1f77b4;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# ===================================
# SESSION STATE INITIALIZATION
# ===================================

if 'bien_params' not in st.session_state:
    st.session_state['bien_params'] = None

# ===================================
# HEADER
# ===================================

st.markdown(
    '<h1 class="main-header">🏠 Estimateur Immobilier Chablais/Annemasse</h1>',
    unsafe_allow_html=True
)

# ===================================
# NAVIGATION (TABS)
# ===================================

# Import des modules UI (Lazy import pour éviter les erreurs circulaires si besoin)
# from src.ui import epic_1_dvf, epic_2_vente, epic_3_additionnelle, epic_4_locative, epic_5_synthese

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "1. Comparables Vendus (DVF+)",
    "2. Comparables en Vente",
    "3. Méthode Additionnelle",
    "4. Méthode Locative",
    "5. Synthèse & Rapport"
])

with tab1:
    try:
        from src.ui import epic_1_dvf
        epic_1_dvf.render()
    except ImportError:
        st.info("Module EPIC 1 en cours de construction...")
    except Exception as e:
        st.error(f"Erreur dans EPIC 1: {e}")

with tab2:
    st.info("🚧 EPIC 2 : Comparables en Vente (Perplexity) - À venir")

with tab3:
    st.info("🚧 EPIC 3 : Méthode Additionnelle (Maisons) - À venir")

with tab4:
    st.info("🚧 EPIC 4 : Méthode Locative (Appartements) - À venir")

with tab5:
    st.info("🚧 EPIC 5 : Synthèse & Pondération - À venir")

# ===================================
# FOOTER
# ===================================

st.markdown("---")
st.markdown("""
<center>
<small>
🏠 <b>Estimateur Immobilier v2.0</b> - Chablais/Annemasse (74)<br>
Données DVF+ & Perplexity AI
</small>
</center>
""", unsafe_allow_html=True)
