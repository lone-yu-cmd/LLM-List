const assert = require('assert');
const registry = require('../index');

console.log('Running JS SDK Verification...');

// Test 1: Providers should not be empty
const providers = registry.getProviders();
assert(Array.isArray(providers), 'Providers should be an array');
assert(providers.length > 0, 'Providers should not be empty');
console.log(`✓ Loaded ${providers.length} providers`);

// Test 2: Check for critical providers
const requiredProviders = ['openai', 'anthropic'];
requiredProviders.forEach(id => {
    const provider = registry.getProvider(id);
    assert(provider, `Provider ${id} should exist`);
    console.log(`✓ Found provider: ${provider.name}`);
});

// Test 3: Check Chat Models
const chatModels = registry.getAllChatModels();
assert(chatModels.length > 0, 'Should have chat models');
console.log(`✓ Loaded ${chatModels.length} chat models`);

console.log('JS SDK Verification Passed!');
