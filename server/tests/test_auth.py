import pytest

from app.component import code
from app.component.auth import Auth
from app.exception.exception import TokenException


def test_decode_token_rejects_missing_token():
    with pytest.raises(TokenException) as missing:
        Auth.decode_token(None)
    assert missing.value.code == code.token_need

    with pytest.raises(TokenException) as empty:
        Auth.decode_token("")
    assert empty.value.code == code.token_need


def test_decode_token_rejects_garbage_token():
    with pytest.raises(TokenException) as invalid:
        Auth.decode_token("not-a-jwt")
    assert invalid.value.code == code.token_invalid
