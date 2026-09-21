import os
from unittest import TestCase, mock

from safe_eth.util.environment import get_bool_env


class TestGetBoolEnv(TestCase):
    def test_not_set_returns_default(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            self.assertFalse(get_bool_env("MISSING_VARIABLE"))
            self.assertTrue(get_bool_env("MISSING_VARIABLE", default=True))

    def test_truthy_values(self):
        for value in ("1", "true", "TRUE", "True", "yes", "on", " true "):
            with (
                self.subTest(value=value),
                mock.patch.dict(os.environ, {"VARIABLE": value}),
            ):
                self.assertTrue(get_bool_env("VARIABLE"))

    def test_falsy_values(self):
        for value in ("0", "false", "FALSE", "no", "off", " false "):
            with (
                self.subTest(value=value),
                mock.patch.dict(os.environ, {"VARIABLE": value}),
            ):
                self.assertFalse(get_bool_env("VARIABLE", default=True))

    def test_unparseable_value_returns_default(self):
        for value in ("", "maybe", "y"):
            with (
                self.subTest(value=value),
                mock.patch.dict(os.environ, {"VARIABLE": value}),
            ):
                with self.assertLogs("safe_eth.util.environment", level="WARNING"):
                    self.assertTrue(get_bool_env("VARIABLE", default=True))
                with self.assertLogs("safe_eth.util.environment", level="WARNING"):
                    self.assertFalse(get_bool_env("VARIABLE", default=False))
