# Spec: Strict Zhipu Validation

## 1. Background
The user has requested strict validation for Zhipu AI models. Any model that fails the connectivity check (i.e., is missing from the remote API list) should be removed from the registry, regardless of documentation. The previous "special handling" in the validator must be removed.

## 2. Goals
- Ensure the registry (`zhipuai.json`) strictly matches the models returned by the Zhipu API (`glm-4.5`, `glm-4.6`, etc.).
- Remove the "Warning only" logic from `verify_connectivity.py` and enforce strict failure for missing models.

## 3. User Scenarios
- **Scenario 1**: User runs `verify_connectivity.py`. It should return `✅ Success` only if all local models are present in the remote list.
- **Scenario 2**: User queries the registry. They should see `glm-4.5`, `glm-4.5-air`, `glm-4.6`, `glm-4.7` (as returned by the API).

## 4. Functional Requirements

### 4.1. Update Validator
- Revert the changes in `.trae/skills/registry-validator/scripts/verify_connectivity.py`.
- Remove the `if provider.get('id') == 'zhipuai':` check.
- Restore the standard `print(f"   ❌ Model missing in remote: {lid}")` behavior.

### 4.2. Update Zhipu Registry
- Replace the content of `registry/providers/zhipuai.json` models list.
- **New Models** (based on API response):
    - `glm-4.5`: "Latest flagship model (2025)."
    - `glm-4.5-air`: "Cost-effective version of GLM-4.5."
    - `glm-4.6`: "Next-generation model (2025)."
    - `glm-4.7`: "Advanced reasoning model (2026)."
- **Remove**: All previous models (`glm-4-plus`, `glm-4-air-250414`, etc.) that are not in the API list.

## 5. Success Criteria
- `verify_connectivity.py` returns exit code 0.
- No special case code exists in `verify_connectivity.py`.
