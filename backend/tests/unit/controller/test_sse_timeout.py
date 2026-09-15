import asyncio
import time

import pytest

from app.controller.chat_controller import timeout_stream_wrapper
from app.model.chat import sse_json


@pytest.mark.unit
class TestSseTimeoutWrapper:
    @pytest.mark.asyncio
    async def test_yields_error_event_on_timeout(self):
        async def silent_stream():
            await asyncio.sleep(2)
            yield "should-not-appear"

        events = []
        async for event in timeout_stream_wrapper(silent_stream(), timeout_seconds=0.05):
            events.append(event)

        assert len(events) == 1
        assert "Connection timeout" in events[0]
        assert '"step": "error"' in events[0] or '"step":"error"' in events[0]

    @pytest.mark.asyncio
    async def test_clamps_non_positive_remaining_timeout(self):
        async def one_event():
            yield "first"

        wrapper = timeout_stream_wrapper(one_event(), timeout_seconds=0)
        # Patch elapsed so remaining would be negative without the clamp
        events = [event async for event in wrapper]
        assert events[0] == "first"

    @pytest.mark.asyncio
    async def test_passes_through_stream_events(self):
        async def stream():
            yield sse_json("notice", {"notice": "hello"})
            yield sse_json("end", {"content": "done"})

        events = [event async for event in timeout_stream_wrapper(stream(), timeout_seconds=2)]
        assert len(events) == 2
        assert "hello" in events[0]
        assert "done" in events[1]
