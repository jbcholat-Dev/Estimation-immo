#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utility: Google Street View Static API
"""

from .config import Config

def get_street_view_url(
    lat: float, 
    lon: float, 
    size: str = "600x400", 
    heading: int = None, 
    pitch: int = 0
) -> str:
    """
    Génère l'URL pour l'API Google Street View Static.
    
    Args:
        lat: Latitude
        lon: Longitude
        size: Taille image (ex: "600x400")
        heading: Orientation (0-360). Si None, Google choisit l'angle par défaut.
        pitch: Inclinaison (-90 à 90). 0 par défaut.
        
    Returns:
        URL complète signée (si implémenté) ou avec clé API.
    """
    if not Config.GOOGLE_MAPS_API_KEY:
        return ""
        
    base_url = "https://maps.googleapis.com/maps/api/streetview"
    params = [
        f"size={size}",
        f"location={lat},{lon}",
        f"key={Config.GOOGLE_MAPS_API_KEY}",
        f"pitch={pitch}"
    ]
    
    if heading is not None:
        params.append(f"heading={heading}")
        
    # Note: Pour la prod, il faudrait signer l'URL si un secret est configuré
    # Mais pour le MVP, la clé API suffit (avec restrictions HTTP referrer recommandées)
        
    return f"{base_url}?{'&'.join(params)}"


def get_street_view_embed_url(
    lat: float, 
    lon: float, 
    heading: int = None, 
    pitch: int = 0
) -> str:
    """
    Génère l'URL pour l'API Google Maps Embed (Street View interactif).
    
    Args:
        lat: Latitude
        lon: Longitude
        heading: Orientation (0-360).
        pitch: Inclinaison (-90 à 90).
        
    Returns:
        URL pour iframe.
    """
    if not Config.GOOGLE_MAPS_API_KEY:
        return ""
        
    base_url = "https://www.google.com/maps/embed/v1/streetview"
    params = [
        f"key={Config.GOOGLE_MAPS_API_KEY}",
        f"location={lat},{lon}",
        f"pitch={pitch}"
    ]
    
    if heading is not None:
        params.append(f"heading={heading}")
        
    return f"{base_url}?{'&'.join(params)}"
