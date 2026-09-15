from app.model.provider.provider import ProviderIn, ProviderOut, VaildStatus


def test_provider_in_accepts_is_valid_boolean():
    provider = ProviderIn.model_validate(
        {
            "provider_name": "openai",
            "model_type": "gpt-4o",
            "api_key": "sk-test",
            "endpoint_url": "https://api.openai.com/v1",
            "is_valid": True,
        }
    )
    assert provider.is_vaild == VaildStatus.is_valid


def test_provider_out_exposes_is_valid():
    provider = ProviderOut(
        provider_name="openai",
        model_type="gpt-4o",
        api_key="sk-test",
        endpoint_url="https://api.openai.com/v1",
        is_vaild=VaildStatus.is_valid,
        id=1,
        user_id=1,
        prefer=True,
    )
    assert provider.is_valid is True
    assert provider.model_dump()["is_valid"] is True
