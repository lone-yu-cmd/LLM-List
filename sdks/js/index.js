const registry = require('../../llm_registry.json');

class LLMRegistry {
    constructor(data) {
        this.registry = data || registry;
    }

    /**
     * Method 1: Get all providers
     * @returns {Array} List of all providers
     */
    getProviders() {
        return this.registry.providers;
    }

    /**
     * Method 2: Get models for a specific provider
     * @param {string} providerId - The ID of the provider
     * @returns {Array} List of models for the provider
     */
    getProviderModels(providerId) {
        const provider = this.registry.providers.find(p => p.id === providerId);
        if (!provider) {
            throw new Error(`Provider with ID '${providerId}' not found.`);
        }
        return provider.models || [];
    }

    /**
     * Method 3: Get provider's API website
     * @param {string} providerId - The ID of the provider
     * @returns {string} The website URL of the provider
     */
    getProviderWebsite(providerId) {
        const provider = this.registry.providers.find(p => p.id === providerId);
        if (!provider) {
            throw new Error(`Provider with ID '${providerId}' not found.`);
        }
        return provider.website;
    }

    /**
     * Method 4: Get provider's auth configuration
     * @param {string} providerId - The ID of the provider
     * @returns {Object} The auth configuration object
     */
    getProviderAuth(providerId) {
        const provider = this.registry.providers.find(p => p.id === providerId);
        if (!provider) {
            throw new Error(`Provider with ID '${providerId}' not found.`);
        }
        return provider.api_config && provider.api_config.auth ? provider.api_config.auth : null;
    }
}

module.exports = new LLMRegistry();
module.exports.LLMRegistry = LLMRegistry;
