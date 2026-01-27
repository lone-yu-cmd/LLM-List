# Spec: Fix Model Connectivity Issues

## 1. Background
The `registry-validator` tool has identified discrepancies between the models listed in our local registry and the models actually returned by the providers' APIs. Several models are "Missing in remote", leading to potential runtime errors for users.

## 2. Goals
- Ensure the registry only contains models that are verified to exist and be accessible via the provider APIs.
- Fix the validation errors reported by `scripts/verify_connectivity.py`.

## 3. User Scenarios
- **Scenario 1**: A user queries the registry for available models. They should only see models that they can successfully use.
- **Scenario 2**: A developer runs the `verify_connectivity.py` script. It should report "Success" for all models and "Failed: 0".

## 4. Functional Requirements

### 4.1. Clean up Google Provider
- Remove the following models from `registry/providers/google.json`:
    - `gemini-1.5-pro`
    - `gemini-1.5-flash`
    - `gemma-3`

### 4.2. Clean up OpenAI Provider
- Remove the following models from `registry/providers/openai.json`:
    - `gpt-oss-120b`
    - `gpt-oss-20b`
    - `o3-deep-research`
    - `o4-mini-deep-research`

### 4.3. Clean up Zhipu AI Provider
- Remove the following models from `registry/providers/zhipuai.json`:
    - `glm-4-plus`
    - `glm-4-air-250414`
    - `glm-4-long`
    - `glm-4-airx`
    - `glm-4-flashx-250414`
    - `glm-4-flash-250414`
    - `glm-z1-air`
    - `glm-z1-airx`
    - `glm-z1-flashx`
    - `glm-z1-flash`
    - `glm-4.1v-thinking-flash`
    - `glm-4v-plus-0111`
    - `glm-4v-flash`
    - `cogvideox-3`
    - `cogvideox-2`
    - `cogvideox-flash`
    - `vidu-q1`
    - `vidu-2`
    - `cogview-4`
    - `cogview-3-flash`
    - `glm-realtime`
    - `glm-4-voice`
    - `charglm-4`
    - `emohaa`
    - `codegeex-4`
    - `rerank`
    - `embedding-3`
    - `embedding-2`

### 4.4. Build Registry
- Run `scripts/build_registry.py` to update the main `llm_registry.json`.

## 5. Success Criteria
- Running `python3 .trae/skills/registry-validator/scripts/verify_connectivity.py` returns `❌ Failed: 0` and no "Model missing in remote" errors for the verified providers.
