from unittest.mock import MagicMock, patch

from camel.toolkits.function_tool import FunctionTool

from app.utils.toolkit.search_toolkit import SearchToolkit


def test_get_can_use_tools_always_includes_search_google():
    with patch("app.utils.toolkit.search_toolkit.env", return_value=None):
        tools = SearchToolkit.get_can_use_tools("task-1")

    assert any(isinstance(tool, FunctionTool) and tool.func.__name__ == "search_google" for tool in tools)


def test_search_google_returns_clear_error_without_credentials():
    toolkit = SearchToolkit("task-1")
    toolkit._config_loaded = True
    toolkit._user_google_api_key = None
    toolkit._user_search_engine_id = None

    with patch("app.utils.toolkit.search_toolkit.env", return_value=None), \
         patch("app.utils.listen.toolkit_listen.get_task_lock", return_value=MagicMock()):
        result = toolkit.search_google("eigent ai")

    assert isinstance(result, list)
    assert result[0]["error"].startswith("search_google is not configured")
