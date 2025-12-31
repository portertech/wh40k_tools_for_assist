"""Test the WH40k search tools."""

from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from custom_components.wh40k_tools_for_assist.const import DOMAIN
from custom_components.wh40k_tools_for_assist.wh40k_fandom import SearchWh40kFandomTool
from custom_components.wh40k_tools_for_assist.wh40k_lexicanum import (
    SearchWh40kLexicanumTool,
)
from custom_components.wh40k_tools_for_assist.wh40k_wahapedia import (
    SearchWh40kWahapediaTool,
    extract_sections_from_html,
    normalize_faction_name,
    search_sections,
)


class TestNormalizeFactionName:
    """Test faction name normalization."""

    def test_exact_match(self) -> None:
        """Test exact faction slug match."""
        assert normalize_faction_name("space-marines") == "space-marines"

    def test_with_spaces(self) -> None:
        """Test faction name with spaces."""
        assert normalize_faction_name("Space Marines") == "space-marines"

    def test_partial_match(self) -> None:
        """Test partial faction name match."""
        result = normalize_faction_name("marines")
        assert result == "space-marines"

    def test_unknown_faction(self) -> None:
        """Test unknown faction returns None."""
        assert normalize_faction_name("unknown-faction") is None

    def test_empty_faction(self) -> None:
        """Test empty faction returns None."""
        assert normalize_faction_name("") is None


class TestExtractSectionsFromHtml:
    """Test HTML section extraction."""

    def test_extracts_sections(self, wahapedia_html_content: str) -> None:
        """Test that sections are extracted from HTML."""
        sections = extract_sections_from_html(
            wahapedia_html_content, "https://test.com"
        )

        assert len(sections) == 2
        assert sections[0]["title"] == "Shooting Phase"
        assert "ranged weapons" in sections[0]["content"]
        assert sections[0]["url"] == "https://test.com"

    def test_empty_html(self) -> None:
        """Test empty HTML returns empty list."""
        sections = extract_sections_from_html(
            "<html><body></body></html>", "https://test.com"
        )
        assert sections == []


class TestSearchSections:
    """Test section search functionality."""

    def test_title_match_priority(self) -> None:
        """Test that title matches come before content matches."""
        sections = [
            {"title": "Other Title", "content": "shooting weapons"},
            {"title": "Shooting Phase", "content": "some content"},
        ]
        results = search_sections(sections, "shooting", 2)

        assert len(results) == 2
        assert results[0]["title"] == "Shooting Phase"  # Title match first

    def test_limit_results(self) -> None:
        """Test that results are limited."""
        sections = [
            {"title": "Section 1", "content": "test content"},
            {"title": "Section 2", "content": "test content"},
            {"title": "Section 3", "content": "test content"},
        ]
        results = search_sections(sections, "test", 2)

        assert len(results) == 2


class TestSearchWh40kLexicanumTool:
    """Test Lexicanum search tool."""

    @pytest.fixture
    def lexicanum_tool(self) -> SearchWh40kLexicanumTool:
        """Create Lexicanum tool instance."""
        return SearchWh40kLexicanumTool()

    def test_tool_attributes(self, lexicanum_tool: SearchWh40kLexicanumTool) -> None:
        """Test tool has correct attributes."""
        assert lexicanum_tool.name == "search_wh40k_lexicanum"
        assert "Lexicanum" in lexicanum_tool.description
        assert "query" in lexicanum_tool.parameters.schema

    @pytest.mark.asyncio
    async def test_search_success(
        self,
        lexicanum_tool: SearchWh40kLexicanumTool,
        mock_hass: MagicMock,
        mock_config_entry: MagicMock,
        lexicanum_search_results: dict[str, Any],
    ) -> None:
        """Test successful search."""
        mock_hass.data[DOMAIN] = {"config": {}}
        mock_hass.config_entries.async_entries.return_value = [mock_config_entry]

        tool_input = MagicMock()
        tool_input.tool_args = {"query": "Space Marines"}

        llm_context = MagicMock()

        with (
            patch(
                "custom_components.wh40k_tools_for_assist.wh40k_lexicanum.async_get_clientsession"
            ) as mock_session,
            patch(
                "custom_components.wh40k_tools_for_assist.wh40k_lexicanum.SQLiteCache"
            ) as mock_cache,
        ):
            # Mock cache miss
            mock_cache_instance = MagicMock()
            mock_cache_instance.get.return_value = None
            mock_cache.return_value = mock_cache_instance

            # Mock HTTP response
            mock_response = AsyncMock()
            mock_response.status = 200
            mock_response.json = AsyncMock(return_value=lexicanum_search_results)

            mock_session_instance = MagicMock()
            mock_session_instance.get.return_value.__aenter__ = AsyncMock(
                return_value=mock_response
            )
            mock_session_instance.get.return_value.__aexit__ = AsyncMock()
            mock_session.return_value = mock_session_instance

            result = await lexicanum_tool.async_call(mock_hass, tool_input, llm_context)

            assert "results" in result or "result" in result


class TestSearchWh40kFandomTool:
    """Test Fandom search tool."""

    @pytest.fixture
    def fandom_tool(self) -> SearchWh40kFandomTool:
        """Create Fandom tool instance."""
        return SearchWh40kFandomTool()

    def test_tool_attributes(self, fandom_tool: SearchWh40kFandomTool) -> None:
        """Test tool has correct attributes."""
        assert fandom_tool.name == "search_wh40k_fandom"
        assert "Fandom" in fandom_tool.description
        assert "query" in fandom_tool.parameters.schema


class TestSearchWh40kWahapediaTool:
    """Test Wahapedia search tool."""

    @pytest.fixture
    def wahapedia_tool(self) -> SearchWh40kWahapediaTool:
        """Create Wahapedia tool instance."""
        return SearchWh40kWahapediaTool()

    def test_tool_attributes(self, wahapedia_tool: SearchWh40kWahapediaTool) -> None:
        """Test tool has correct attributes."""
        assert wahapedia_tool.name == "search_wh40k_wahapedia"
        assert "Wahapedia" in wahapedia_tool.description
        assert "query" in wahapedia_tool.parameters.schema
        assert "faction" in wahapedia_tool.parameters.schema
