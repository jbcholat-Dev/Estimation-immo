#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Service de recherche de comparables en vente via Perplexity API.
Phase 5 - EPIC 2: Comparables en Vente
"""

import httpx
import json
import logging
import asyncio
import pandas as pd
from typing import Optional, Dict, List
from pydantic import BaseModel, Field, field_validator
from enum import Enum

from .utils.config import Config
from .utils.geocoding import get_coordinates

logger = logging.getLogger(__name__)


class PropertyType(str, Enum):
    """Types de propriétés supportées"""
    APARTMENT = "apartment"
    HOUSE = "house"
    STUDIO = "studio"
    TOWNHOUSE = "townhouse"
    ALL = "all"


class PerplexityProperty(BaseModel):
    """Schéma de validation pour une propriété retournée par Perplexity"""

    address: str = Field(..., description="Adresse complète du bien")
    price: Optional[float] = Field(None, description="Prix en euros")
    surface: Optional[float] = Field(None, description="Surface en m²")
    rooms: Optional[int] = Field(None, description="Nombre de pièces")
    property_type: Optional[str] = Field(None, description="Type de bien (apartment, house, etc.)")
    listing_url: Optional[str] = Field(None, description="URL de l'annonce")
    publication_date: Optional[str] = Field(None, description="Date de publication")
    description: Optional[str] = Field(None, description="Description courte du bien")
    latitude: Optional[float] = Field(None, description="Latitude WGS84")
    longitude: Optional[float] = Field(None, description="Longitude WGS84")

    @field_validator("price")
    @classmethod
    def validate_price(cls, v):
        """Valide que le prix est positif"""
        if v is not None and v < 0:
            raise ValueError("Le prix doit être positif")
        return v

    @field_validator("surface")
    @classmethod
    def validate_surface(cls, v):
        """Valide que la surface est positive"""
        if v is not None and v < 0:
            raise ValueError("La surface doit être positive")
        return v


class PerplexityResponse(BaseModel):
    """Schéma de validation pour la réponse Perplexity"""

    properties: List[PerplexityProperty] = Field(default_factory=list)
    total_count: int = Field(default=0)
    search_query: str = Field(default="")


class PerplexityRetriever:
    """Service de recherche de comparables via API Perplexity"""

    BASE_URL = "https://api.perplexity.ai/chat/completions"
    MODEL = "sonar"
    MAX_RETRIES = 3
    RETRY_DELAY = 1  # secondes
    REQUEST_TIMEOUT = 30  # secondes

    def __init__(self):
        """Initialise le service Perplexity"""
        self.api_key = Config.PERPLEXITY_API_KEY
        if not self.api_key:
            logger.error("[ERROR] PERPLEXITY_API_KEY non configurée")
            self.client = None
        else:
            self.client = httpx.AsyncClient(
                headers={"Authorization": f"Bearer {self.api_key}"}
            )
            logger.info("[OK] Perplexity client initialisé")

    async def _make_request_with_retry(
        self,
        prompt: str,
        max_retries: int = MAX_RETRIES
    ) -> Optional[Dict]:
        """
        Effectue un appel à l'API Perplexity avec retries exponentiels.

        Args:
            prompt: Le prompt à envoyer à Perplexity
            max_retries: Nombre de tentatives maximum

        Returns:
            La réponse JSON parsée ou None en cas d'erreur
        """
        for attempt in range(max_retries):
            try:
                response = await self.client.post(
                    self.BASE_URL,
                    json={
                        "model": self.MODEL,
                        "messages": [
                            {"role": "user", "content": prompt}
                        ],
                        "temperature": 0.2,  # Réduire la variabilité
                        "top_p": 0.9,
                    },
                    timeout=self.REQUEST_TIMEOUT,
                )

                response.raise_for_status()
                return response.json()

            except httpx.TimeoutException as e:
                logger.warning(
                    f"[WARNING] Timeout Perplexity (tentative {attempt + 1}/{max_retries}): {e}"
                )
                if attempt < max_retries - 1:
                    await asyncio.sleep(self.RETRY_DELAY * (2 ** attempt))
                else:
                    logger.error("[ERROR] Max retries atteint pour timeout")
                    return None

            except httpx.HTTPStatusError as e:
                if e.response.status_code == 429:  # Rate limit
                    logger.warning(f"[WARNING] Rate limit Perplexity, attente...")
                    if attempt < max_retries - 1:
                        await asyncio.sleep(self.RETRY_DELAY * (2 ** attempt))
                    else:
                        logger.error("[ERROR] Rate limit persistant")
                        return None
                else:
                    logger.error(f"[ERROR] Erreur HTTP Perplexity {e.response.status_code}: {e}")
                    return None

            except Exception as e:
                logger.error(f"[ERROR] Erreur API Perplexity: {e}")
                return None

        return None

    def _build_search_prompt(
        self,
        city: str,
        postal_code: str,
        property_type: str = "all",
        price_min: Optional[float] = None,
        price_max: Optional[float] = None,
        radius_km: int = 5,
    ) -> str:
        """
        Construit le prompt pour rechercher les biens en vente.

        Args:
            city: Ville de recherche (ex: "Thonon-les-Bains")
            postal_code: Code postal (ex: "74200")
            property_type: Type de bien (apartment, house, studio, townhouse, all)
            price_min: Prix minimum en euros
            price_max: Prix maximum en euros
            radius_km: Rayon de recherche en km

        Returns:
            Le prompt formaté pour Perplexity
        """
        price_filter = ""
        if price_min or price_max:
            price_filter = f"- Fourchette de prix: {price_min or 'N/A'} - {price_max or 'N/A'} euros\n"

        prompt = f"""Recherche les biens immobiliers actuellement à vendre dans {city} ({postal_code}), dans un rayon de {radius_km}km.

Critères de recherche:
- Localité: {city}
- Code postal: {postal_code}
- Type de bien: {property_type}
{price_filter}- Rayon: {radius_km}km

Retourne les résultats en format JSON structuré avec les champs suivants pour chaque bien:
{{
    "address": "adresse complète",
    "price": prix_en_euros,
    "surface": surface_en_m2,
    "rooms": nombre_de_pieces,
    "property_type": "type_bien",
    "listing_url": "url_de_l_annonce_ou_source",
    "publication_date": "date_YYYY-MM-DD_ou_N/A",
    "description": "description_courte"
}}

Retourne SEULEMENT le JSON valide sans texte supplémentaire. Si pas de résultats, retourne: {{"properties": []}}
"""
        return prompt

    async def search_properties_for_sale(
        self,
        city: str,
        postal_code: str,
        property_type: str = "all",
        price_min: Optional[float] = None,
        price_max: Optional[float] = None,
        radius_km: int = 5,
    ) -> List[Dict]:
        """
        Recherche les biens en vente via Perplexity et enrichit les données.

        Args:
            city: Ville de recherche
            postal_code: Code postal
            property_type: Type de bien
            price_min: Prix minimum
            price_max: Prix maximum
            radius_km: Rayon de recherche

        Returns:
            Liste de dictionnaires avec propriétés enrichies (lat/lon)
        """
        if not self.client:
            logger.error("[ERROR] Perplexity client non initialisé")
            return []

        try:
            # Construire le prompt
            prompt = self._build_search_prompt(
                city, postal_code, property_type, price_min, price_max, radius_km
            )
            logger.info(f"[INFO] Recherche Perplexity: {city} ({postal_code})")

            # Appel API avec retries
            response_data = await self._make_request_with_retry(prompt)
            if not response_data:
                logger.error("[ERROR] Perplexity n'a pas retourné de réponse valide")
                return []

            # Parser la réponse
            perplexity_response = self._parse_perplexity_response(response_data)
            logger.info(f"[OK] {len(perplexity_response)} bien(s) trouvé(s)")

            # Enrichir avec géocodage
            enriched = await self._enrich_with_geocoding(perplexity_response)
            return enriched

        except Exception as e:
            logger.error(f"[ERROR] Erreur lors de la recherche: {e}")
            return []

    def _parse_perplexity_response(self, response_data: Dict) -> List[PerplexityProperty]:
        """
        Parse la réponse Perplexity et valide le format.

        Args:
            response_data: La réponse JSON de Perplexity

        Returns:
            Liste de PerplexityProperty validés
        """
        try:
            # Extraire le contenu du message
            if "choices" not in response_data or not response_data["choices"]:
                logger.warning("[WARNING] Format Perplexity inattendu (pas de choices)")
                return []

            content = response_data["choices"][0].get("message", {}).get("content", "")
            if not content:
                logger.warning("[WARNING] Aucun contenu dans la réponse Perplexity")
                return []

            # Parser le JSON depuis le contenu
            try:
                parsed = json.loads(content)
            except json.JSONDecodeError:
                logger.error("[ERROR] Impossible de parser JSON depuis la réponse Perplexity")
                logger.debug(f"Contenu reçu: {content[:200]}")
                return []

            # Valider et créer les objets PerplexityProperty
            properties = []
            if "properties" in parsed:
                for prop_data in parsed["properties"]:
                    try:
                        prop = PerplexityProperty(**prop_data)
                        properties.append(prop)
                    except ValueError as e:
                        logger.warning(f"[WARNING] Propriété invalide: {e}")
                        continue

            logger.info(f"[OK] {len(properties)} propriété(s) parsée(s) avec succès")
            return properties

        except Exception as e:
            logger.error(f"[ERROR] Erreur lors du parsing Perplexity: {e}")
            return []

    async def _enrich_with_geocoding(
        self, properties: List[PerplexityProperty]
    ) -> List[Dict]:
        """
        Enrichit les propriétés avec coordonnées géographiques.

        Args:
            properties: Liste des propriétés à enrichir

        Returns:
            Liste de dictionnaires avec lat/lon ajoutées
        """
        enriched = []
        for prop in properties:
            prop_dict = prop.model_dump()

            # Si coordonnées manquantes, essayer de géocoder
            if not prop_dict.get("latitude") or not prop_dict.get("longitude"):
                coords = get_coordinates(prop_dict["address"])
                if coords:
                    prop_dict["latitude"] = coords[0]
                    prop_dict["longitude"] = coords[1]
                    logger.debug(f"[OK] Géocodage réussi: {prop_dict['address']}")
                else:
                    logger.warning(f"[WARNING] Géocodage échoué: {prop_dict['address']}")

            enriched.append(prop_dict)

        return enriched

    async def close(self):
        """Ferme la connexion HTTP"""
        if self.client:
            await self.client.aclose()


# Instance globale singleton
_perplexity_retriever: Optional[PerplexityRetriever] = None


def get_perplexity_retriever() -> PerplexityRetriever:
    """Retourne l'instance singleton PerplexityRetriever"""
    global _perplexity_retriever
    if _perplexity_retriever is None:
        _perplexity_retriever = PerplexityRetriever()
    return _perplexity_retriever


if __name__ == "__main__":
    # Test
    import sys

    logging.basicConfig(level=logging.INFO)

    async def test():
        retriever = get_perplexity_retriever()
        results = await retriever.search_properties_for_sale(
            city="Thonon-les-Bains",
            postal_code="74200",
            property_type="all",
            price_min=200000,
            price_max=500000,
            radius_km=5,
        )
        print(f"Résultats: {results}")
        await retriever.close()

    try:
        asyncio.run(test())
    except Exception as e:
        print(f"Erreur: {e}")
        sys.exit(1)
