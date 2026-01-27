const registry = require('./data/llm_registry.json');

class LLMRegistry {
  constructor(data) {
    this.registry = data || registry;
  }

  /**
   * Get all providers
   * @returns {Array} List of all providers
   */
  getProviders() {
    return this.registry.providers || [];
  }

  /**
   * Get a provider by ID
   * @param {string} providerId - The provider ID (e.g., "openai")
   * @returns {Object|null} The provider object or null if not found
   */
  getProvider(providerId) {
    return this.getProviders().find(p => p.id === providerId) || null;
  }

  /**
   * Get all models for a specific provider
   * @param {string} providerId - The provider ID
   * @returns {Array} List of models
   */
  getModels(providerId) {
    const provider = this.getProvider(providerId);
    return provider ? provider.models : [];
  }

  /**
   * Get a specific model by ID from a provider
   * @param {string} providerId - The provider ID
   * @param {string} modelId - The model ID
   * @returns {Object|null} The model object or null
   */
  getModel(providerId, modelId) {
    const models = this.getModels(providerId);
    return models.find(m => m.id === modelId) || null;
  }

  /**
   * Get all chat models across all providers
   * @returns {Array} List of all chat models with provider info
   */
  getAllChatModels() {
    const allModels = [];
    this.getProviders().forEach(provider => {
      if (provider.models) {
        provider.models.forEach(model => {
          if (model.type === 'chat') {
            allModels.push({
              ...model,
              provider_id: provider.id,
              provider_name: provider.name
            });
          }
        });
      }
    });
    return allModels;
  }
}

// Export a default instance
const defaultRegistry = new LLMRegistry();
module.exports = defaultRegistry;
module.exports.LLMRegistry = LLMRegistry;
