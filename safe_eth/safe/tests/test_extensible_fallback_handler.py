from .safe_test_case import SafeTestCaseMixin


class TestExtensibleFallbackHandler(SafeTestCaseMixin):
    def test_safe_with_extensible_fallback_handler(self):
        """
        Test that a Safe can be deployed with ExtensibleFallbackHandler as fallback handler
        """
        safe = self.deploy_test_safe_v1_5_0(
            fallback_handler=self.extensible_fallback_handler_V1_5_0.address
        )
        self.assertIsNotNone(safe)
        self.assertEqual(safe.retrieve_version(), "1.5.0")
