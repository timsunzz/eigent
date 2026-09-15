from app.model.provider.provider import ProviderIn, ProviderOut, VaildStatus


def test_provider_in_accepts_is_valid_boolean():
    provider = ProviderIn(
        provider_name="openai",
        model_type="gpt-4.1",
        api_key="sk-test",
        endpoint_url="https://api.openai.com/v1",
        is_valid=True,
    )
    assert provider.is_vaild == VaildStatus.is_valid


def test_provider_out_exposes_is_valid_alias():
    provider = ProviderOut(
        id=1,
        user_id=1,
        provider_name="openai",
        model_type="gpt-4.1",
        api_key="sk-test",
        endpoint_url="https://api.openai.com/v1",
        is_vaild=VaildStatus.is_valid,
        prefer=True,
    )
    assert provider.is_valid is True
