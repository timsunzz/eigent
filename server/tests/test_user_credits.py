from app.model.user.user import User


def test_refresh_credits_on_active_does_not_raise():
    user = User.model_construct(email="smoke@example.com")
    assert user.refresh_credits_on_active(session=None) is None
