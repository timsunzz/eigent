import os
import unittest
from unittest.mock import patch


class EnvLookupTests(unittest.TestCase):
    def test_prefers_exact_key(self):
        from app.component.environment import _getenv

        with patch.dict(os.environ, {"secret_key": "exact", "SECRET_KEY": "upper"}, clear=False):
            self.assertEqual(_getenv("secret_key"), "exact")

    def test_falls_back_to_uppercase(self):
        from app.component.environment import _getenv

        environ = {k: v for k, v in os.environ.items() if k.lower() != "secret_key"}
        environ["SECRET_KEY"] = "from-paas"
        with patch.dict(os.environ, environ, clear=True):
            self.assertEqual(_getenv("secret_key"), "from-paas")

    def test_missing_returns_none(self):
        from app.component.environment import _getenv

        environ = {k: v for k, v in os.environ.items() if k.lower() != "missing_config_key"}
        with patch.dict(os.environ, environ, clear=True):
            self.assertIsNone(_getenv("missing_config_key"))


if __name__ == "__main__":
    unittest.main()
