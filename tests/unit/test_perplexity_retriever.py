#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests unitaires pour le service Perplexity Retriever.
Phase 5 - EPIC 2: Comparables en Vente
"""

import pytest
import asyncio
import json
from unittest.mock import AsyncMock, MagicMock, patch
from httpx import AsyncClient, HTTPStatusError, TimeoutException, Response

from src.perplexity_retriever import (
    PerplexityRetriever,
    PerplexityProperty,
    PerplexityResponse,
    PropertyType,
)


class TestPerplexityProperty:
    """Tests pour le schéma PerplexityProperty"""

    def test_valid_property(self):
        """Test création d'une propriété valide"""
        prop = PerplexityProperty(
            address="123 Rue de la Paix, 74200 Thonon-les-Bains",
            price=350000.0,
            surface=120.0,
            rooms=4,
            property_type="house",
            listing_url="https://example.com/listing/123",
            publication_date="2024-11-20",
        )
        assert prop.address == "123 Rue de la Paix, 74200 Thonon-les-Bains"
        assert prop.price == 350000.0
        assert prop.rooms == 4

    def test_negative_price_validation(self):
        """Test validation du prix négatif"""
        with pytest.raises(ValueError, match="Le prix doit être positif"):
            PerplexityProperty(
                address="Test",
                price=-1000.0,
            )

    def test_negative_surface_validation(self):
        """Test validation de la surface négative"""
        with pytest.raises(ValueError, match="La surface doit être positive"):
            PerplexityProperty(
                address="Test",
                surface=-50.0,
            )

    def test_optional_fields(self):
        """Test que les champs optionnels peuvent être None"""
        prop = PerplexityProperty(address="Test Address")
        assert prop.price is None
        assert prop.surface is None
        assert prop.rooms is None
        assert prop.latitude is None
        assert prop.longitude is None


class TestPerplexityRetriever:
    """Tests pour le service PerplexityRetriever"""

    @pytest.fixture
    def retriever(self):
        """Fixture pour créer une instance de PerplexityRetriever"""
        with patch("src.perplexity_retriever.Config.PERPLEXITY_API_KEY", "test-key"):
            retriever = PerplexityRetriever()
            yield retriever

    def test_build_search_prompt_basic(self, retriever):
        """Test construction du prompt de recherche basique"""
        prompt = retriever._build_search_prompt(
            city="Thonon-les-Bains",
            postal_code="74200",
        )
        assert "Thonon-les-Bains" in prompt
        assert "74200" in prompt
        assert "JSON" in prompt

    def test_build_search_prompt_with_filters(self, retriever):
        """Test construction du prompt avec filtres de prix"""
        prompt = retriever._build_search_prompt(
            city="Annemasse",
            postal_code="74100",
            property_type="apartment",
            price_min=250000,
            price_max=400000,
            radius_km=10,
        )
        assert "Annemasse" in prompt
        assert "apartment" in prompt
        assert "250000" in prompt
        assert "400000" in prompt
        assert "10km" in prompt

    def test_parse_perplexity_response_valid(self, retriever):
        """Test parsing d'une réponse Perplexity valide"""
        mock_response = {
            "choices": [
                {
                    "message": {
                        "content": json.dumps({
                            "properties": [
                                {
                                    "address": "123 Rue Test",
                                    "price": 300000.0,
                                    "surface": 100.0,
                                    "rooms": 3,
                                    "property_type": "house",
                                    "listing_url": "https://example.com",
                                    "publication_date": "2024-11-20",
                                    "description": "Maison spacieuse",
                                }
                            ]
                        })
                    }
                }
            ]
        }

        properties = retriever._parse_perplexity_response(mock_response)
        assert len(properties) == 1
        assert properties[0].address == "123 Rue Test"
        assert properties[0].price == 300000.0
        assert properties[0].rooms == 3

    def test_parse_perplexity_response_empty(self, retriever):
        """Test parsing avec résultats vides"""
        mock_response = {
            "choices": [
                {
                    "message": {
                        "content": json.dumps({"properties": []})
                    }
                }
            ]
        }

        properties = retriever._parse_perplexity_response(mock_response)
        assert len(properties) == 0

    def test_parse_perplexity_response_invalid_json(self, retriever):
        """Test parsing avec JSON invalide"""
        mock_response = {
            "choices": [
                {
                    "message": {
                        "content": "This is not JSON"
                    }
                }
            ]
        }

        properties = retriever._parse_perplexity_response(mock_response)
        assert len(properties) == 0

    def test_parse_perplexity_response_missing_choices(self, retriever):
        """Test parsing avec format inattendu"""
        mock_response = {}

        properties = retriever._parse_perplexity_response(mock_response)
        assert len(properties) == 0

    def test_parse_perplexity_response_invalid_property(self, retriever):
        """Test parsing avec propriété invalide (skip invalid)"""
        mock_response = {
            "choices": [
                {
                    "message": {
                        "content": json.dumps({
                            "properties": [
                                {
                                    "address": "123 Rue Test",
                                    "price": 300000.0,
                                },
                                {
                                    "address": "456 Invalid",
                                    "price": -5000.0,  # Invalid price
                                }
                            ]
                        })
                    }
                }
            ]
        }

        properties = retriever._parse_perplexity_response(mock_response)
        assert len(properties) == 1  # Only valid property
        assert properties[0].address == "123 Rue Test"

    @pytest.mark.asyncio
    async def test_make_request_with_retry_success(self, retriever):
        """Test appel API avec succès"""
        mock_response = {
            "choices": [{"message": {"content": '{"properties": []}'}}]
        }

        retriever.client.post = AsyncMock()
        mock_http_response = MagicMock()
        mock_http_response.json.return_value = mock_response
        mock_http_response.raise_for_status = MagicMock()
        retriever.client.post.return_value = mock_http_response

        result = await retriever._make_request_with_retry("test prompt")
        assert result == mock_response

    @pytest.mark.asyncio
    async def test_make_request_with_retry_timeout(self, retriever):
        """Test retry sur timeout"""
        retriever.client.post = AsyncMock()
        retriever.client.post.side_effect = TimeoutException("Timeout")

        result = await retriever._make_request_with_retry("test prompt", max_retries=2)
        # Après 2 tentatives, doit retourner None
        assert result is None
        # Doit avoir tenté 2 fois
        assert retriever.client.post.call_count == 2

    @pytest.mark.asyncio
    async def test_make_request_with_retry_rate_limit(self, retriever):
        """Test retry sur rate limit (429)"""
        retriever.client.post = AsyncMock()

        # Mock Response pour HTTPStatusError
        mock_response = MagicMock()
        mock_response.status_code = 429
        mock_http_error = HTTPStatusError(
            "Rate limited",
            request=MagicMock(),
            response=mock_response,
        )

        retriever.client.post.side_effect = mock_http_error

        result = await retriever._make_request_with_retry("test prompt", max_retries=2)
        assert result is None
        assert retriever.client.post.call_count == 2

    @pytest.mark.asyncio
    async def test_make_request_with_retry_http_error(self, retriever):
        """Test erreur HTTP non-rate-limit"""
        retriever.client.post = AsyncMock()

        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_http_error = HTTPStatusError(
            "Server error",
            request=MagicMock(),
            response=mock_response,
        )

        retriever.client.post.side_effect = mock_http_error

        result = await retriever._make_request_with_retry("test prompt")
        assert result is None

    @pytest.mark.asyncio
    async def test_enrich_with_geocoding_success(self, retriever):
        """Test enrichissement géocodage réussi"""
        properties = [
            PerplexityProperty(
                address="Thonon-les-Bains, 74200",
                price=300000.0,
            )
        ]

        with patch("src.perplexity_retriever.get_coordinates") as mock_geocode:
            mock_geocode.return_value = (46.3727, 6.4774)

            enriched = await retriever._enrich_with_geocoding(properties)

            assert len(enriched) == 1
            assert enriched[0]["latitude"] == 46.3727
            assert enriched[0]["longitude"] == 6.4774
            mock_geocode.assert_called_once()

    @pytest.mark.asyncio
    async def test_enrich_with_geocoding_failure(self, retriever):
        """Test enrichissement géocodage échoué"""
        properties = [
            PerplexityProperty(
                address="Invalid Address XYZ",
                price=300000.0,
            )
        ]

        with patch("src.perplexity_retriever.get_coordinates") as mock_geocode:
            mock_geocode.return_value = None

            enriched = await retriever._enrich_with_geocoding(properties)

            assert len(enriched) == 1
            assert enriched[0]["latitude"] is None
            assert enriched[0]["longitude"] is None

    @pytest.mark.asyncio
    async def test_enrich_with_geocoding_already_has_coords(self, retriever):
        """Test enrichissement quand coords existent déjà"""
        properties = [
            PerplexityProperty(
                address="Test",
                latitude=46.3727,
                longitude=6.4774,
            )
        ]

        with patch("src.perplexity_retriever.get_coordinates") as mock_geocode:
            enriched = await retriever._enrich_with_geocoding(properties)

            # Ne doit pas appeler geocode si coords existent
            assert mock_geocode.call_count == 0
            assert enriched[0]["latitude"] == 46.3727
            assert enriched[0]["longitude"] == 6.4774

    @pytest.mark.asyncio
    async def test_search_properties_for_sale_full_workflow(self, retriever):
        """Test workflow complet de recherche"""
        mock_perplexity_response = {
            "choices": [
                {
                    "message": {
                        "content": json.dumps({
                            "properties": [
                                {
                                    "address": "Thonon-les-Bains, 74200",
                                    "price": 350000.0,
                                    "surface": 120.0,
                                    "rooms": 4,
                                    "property_type": "house",
                                }
                            ]
                        })
                    }
                }
            ]
        }

        # Mock l'appel API
        retriever.client.post = AsyncMock()
        mock_http_response = MagicMock()
        mock_http_response.json.return_value = mock_perplexity_response
        mock_http_response.raise_for_status = MagicMock()
        retriever.client.post.return_value = mock_http_response

        # Mock le géocodage
        with patch("src.perplexity_retriever.get_coordinates") as mock_geocode:
            mock_geocode.return_value = (46.3727, 6.4774)

            results = await retriever.search_properties_for_sale(
                city="Thonon-les-Bains",
                postal_code="74200",
            )

            assert len(results) == 1
            assert results[0]["address"] == "Thonon-les-Bains, 74200"
            assert results[0]["latitude"] == 46.3727
            assert results[0]["longitude"] == 6.4774

    @pytest.mark.asyncio
    async def test_search_properties_no_client(self):
        """Test recherche sans client initialisé"""
        with patch("src.perplexity_retriever.Config.PERPLEXITY_API_KEY", ""):
            retriever = PerplexityRetriever()
            results = await retriever.search_properties_for_sale(
                city="Test",
                postal_code="74200",
            )
            assert results == []


# Tests d'intégration optionnels (commentés par défaut)
# @pytest.mark.integration
# class TestPerplexityIntegration:
#     """Tests d'intégration avec la vraie API Perplexity"""
#
#     @pytest.mark.asyncio
#     async def test_real_api_call(self):
#         """Test appel réel à l'API Perplexity"""
#         retriever = PerplexityRetriever()
#         if not retriever.client:
#             pytest.skip("PERPLEXITY_API_KEY non configurée")
#
#         results = await retriever.search_properties_for_sale(
#             city="Thonon-les-Bains",
#             postal_code="74200",
#             price_min=200000,
#             price_max=500000,
#         )
#         await retriever.close()
#
#         assert isinstance(results, list)
#         # Ne pas vérifier len > 0 car peut dépendre des vrais résultats
