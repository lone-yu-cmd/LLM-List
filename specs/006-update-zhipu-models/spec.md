# Spec: Update Zhipu AI Models

## 1. Background
The current `registry/providers/zhipuai.json` file has an empty model list because the connectivity validator failed to find them in the API response. The user has provided updated documentation from `https://open.bigmodel.cn/dev/howuse/model` listing the available models.

## 2. Goals
- Populate `registry/providers/zhipuai.json` with the models listed in the provided documentation.
- Ensure the registry reflects the capabilities (context window, output tokens) described in the docs.
- Adjust `verify_connectivity.py` to accommodate the discrepancy between the Zhipu API's `/models` endpoint (which returns a limited subset) and the documentation.

## 3. User Scenarios
- **Scenario 1**: User queries the registry for Zhipu models and sees `glm-4-plus`, `glm-4-air`, etc.
- **Scenario 2**: User runs `verify_connectivity.py`. It should not fail for Zhipu models simply because they are missing from the API list, as the API list is known to be incomplete.

## 4. Functional Requirements

### 4.1. Update Zhipu Registry
- Add the following models to `registry/providers/zhipuai.json`:
    - **Language**: `glm-4-plus`, `glm-4-air-250414`, `glm-4-long`, `glm-4-airx`, `glm-4-flashx-250414`, `glm-4-flash-250414`
    - **Reasoning**: `glm-z1-air`, `glm-z1-airx`, `glm-z1-flashx`, `glm-z1-flash`
    - **Multimodal**: `glm-4.1v-thinking-flash`, `glm-4v-plus-0111`, `glm-4v-flash`
    - **Video**: `cogvideox-3`, `cogvideox-2`, `cogvideox-flash`, `vidu-q1`, `vidu-2`
    - **Image**: `cogview-4`, `cogview-3-flash`
    - **Realtime/Audio**: `glm-realtime`, `glm-4-voice`
    - **Others**: `charglm-4`, `emohaa`, `codegeex-4`, `rerank`, `embedding-3`
- **Metadata**:
    - Use descriptions, context windows, and max output tokens from the documentation.
    - Set appropriate features (e.g., `reasoning`, `video-generation`, `free`).

### 4.2. Update Validator
- Modify `.trae/skills/registry-validator/scripts/verify_connectivity.py`.
- Add a special case for `zhipuai`: If the API returns a success status (200) but the model list is small or doesn't match, verify that *at least* connection is possible, but do not fail individual models if they are missing from the remote list.
- Alternatively, print a "Warning" instead of "Error/Fail" for missing models if the provider is Zhipu.

## 5. Success Criteria
- `registry/providers/zhipuai.json` contains the full list of models.
- `verify_connectivity.py` passes (returns exit code 0) even with these models present.
