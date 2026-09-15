from unittest.mock import MagicMock, patch

import pytest

from app.utils.toolkit import search_toolkit as search_toolkit_module
from app.utils.toolkit.search_toolkit import SearchToolkit


@pytest.mark.unit
class TestSearchToolkit:
    def setup_method(self):
        search_toolkit_module._search_tools_cache.clear()

    def test_get_can_use_tools_always_registers_search_google(self):
        tools = SearchToolkit.get_can_use_tools("project_1")

        assert len(tools) == 1
        assert tools[0].get_function_name() == "search_google"
        assert SearchToolkit.get_can_use_tools("project_1") is tools

    def test_cloud_search_google_returns_empty_on_unexpected_payload(self):
        toolkit = SearchToolkit("project_1")
        mock_response = MagicMock()
        mock_response.json.return_value = {"detail": "unauthorized"}
        mock_response.raise_for_status.return_value = None

        with patch(
            "app.utils.toolkit.search_toolkit.env_not_empty",
            side_effect=lambda key: "https://example.test" if key == "SERVER_URL" else "key",
        ), patch("app.utils.toolkit.search_toolkit.httpx.get", return_value=mock_response):
            assert toolkit.cloud_search_google("news") == []

    def test_cloud_search_google_handles_http_error(self):
        toolkit = SearchToolkit("project_1")
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = Exception("boom")

        with patch(
            "app.utils.toolkit.search_toolkit.env_not_empty",
            side_effect=lambda key: "https://example.test" if key == "SERVER_URL" else "key",
        ), patch("app.utils.toolkit.search_toolkit.httpx.get", return_value=mock_response):
            result = toolkit.cloud_search_google("news")

        assert result[0]["error"].startswith("Cloud Google Search failed")
