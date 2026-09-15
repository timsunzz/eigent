from datetime import date

from app.model.user.user import User


class _CreditUser:
    last_daily_credit_date = None
    last_monthly_credit_date = None

    def save(self, session):
        self.saved = session


def test_refresh_credits_on_active_updates_stamps():
    user = _CreditUser()
    session = object()
    User.refresh_credits_on_active(user, session)

    today = date.today()
    assert user.last_daily_credit_date == today
    assert user.last_monthly_credit_date == today.replace(day=1)
    assert user.saved is session
