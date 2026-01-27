# Plan: Strict Zhipu Validation

## 1. Analysis
The user demands strict consistency between the registry and the API. This simplifies the validation logic but requires updating the data to match the "future" state of the environment (2026).

## 2. Technical Approach
- **Step 1**: Revert `verify_connectivity.py` to its previous state (or cleaner).
- **Step 2**: Update `zhipuai.json`. Since I don't have detailed metadata for the new models (`glm-4.5` etc.) other than their existence, I will use reasonable defaults based on the naming convention (e.g., `air` = cost effective, `flash` = fast).

## 3. Files to Modify
- `.trae/skills/registry-validator/scripts/verify_connectivity.py`
- `registry/providers/zhipuai.json`

## 4. Verification
- Run `verify_connectivity.py`.
