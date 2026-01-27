import unittest
import sys
import os

# Add parent directory to path to allow importing llm_list
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import llm_list

class TestRegistryVerification(unittest.TestCase):
    def test_providers_loaded(self):
        print("\nRunning Python SDK Verification...")
        providers = llm_list.get_providers()
        self.assertIsInstance(providers, list)
        self.assertGreater(len(providers), 0, "Providers should not be empty")
        print(f"✓ Loaded {len(providers)} providers")

    def test_required_providers(self):
        required = ['openai', 'anthropic']
        for pid in required:
            provider = llm_list.get_provider(pid)
            self.assertIsNotNone(provider, f"Provider {pid} should exist")
            print(f"✓ Found provider: {provider.get('name')}")

    def test_chat_models(self):
        models = llm_list.get_all_chat_models()
        self.assertGreater(len(models), 0, "Should have chat models")
        print(f"✓ Loaded {len(models)} chat models")

if __name__ == '__main__':
    unittest.main()
