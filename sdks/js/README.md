# LLM-List JS SDK

Standardized LLM registry data for Node.js.

## Installation

```bash
npm install llm-list
```

## Usage

```javascript
const registry = require('llm-list');

// Get all providers
const providers = registry.getProviders();
console.log(`Loaded ${providers.length} providers`);

// Get a specific provider
const openai = registry.getProvider('openai');
console.log(openai.api_config);

// Get a specific model
const gpt4 = registry.getModel('openai', 'gpt-4');
console.log(gpt4);
```

## Features
- **Standardized**: Unified JSON format for all providers.
- **Up-to-date**: Automatically synced with the central registry.
- **Lightweight**: Zero runtime dependencies.

## License
MIT
