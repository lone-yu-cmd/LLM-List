# Tasks: Add DeepSeek Provider

**Plan**: [plan.md](./plan.md)

## User Story 1: Integrate DeepSeek Provider

- [x] [T-001] Create `registry/providers/deepseek.json` with provider metadata and API config
- [x] [T-002] Add `deepseek-chat` and `deepseek-reasoner` models to the JSON file
- [x] [T-003] Run schema validation (`npm run validate:format`)
- [x] [T-004] Run registry build (`npm run build`)
- [x] [T-005] Run integrity tests (`python3 .trae/skills/registry-validator/scripts/test_registry_data.py`)
