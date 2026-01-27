# Plan: Enhanced Model Verification

## 1. Logic Update (`verify_connectivity.py`)
-   [ ] **Fetch Remote Models**: Modify the script to parse the JSON response from the `/models` endpoint (or equivalent).
-   [ ] **Normalization**: Ensure we handle different response structures (e.g., OpenAI returns `{"data": [{"id": "..."}]}`, Google might differ).
-   [ ] **Cross-Check**:
    -   Load local models from `registry`.
    -   Compare local model IDs against the remote list.
    -   Log: "✅ Found" or "❌ Missing" for each local model.

## 2. Response Parsing Strategy
-   **OpenAI/DeepSeek/ZhipuAI**: Standard OpenAI format (`{"data": [{"id": "..."}]}`).
-   **Google**: Likely `{"models": [{"name": "models/..."}]}`. Need to handle the `models/` prefix stripping.
-   **Anthropic**: Does not support listing models via API in the same standard way (or requires specific handling). *Correction*: Anthropic has a `/v1/models` endpoint now? No, Anthropic usually doesn't have a public list models endpoint like OpenAI. **Constraint**: For providers without a list-models endpoint, we might skip model validation or try a minimal generation request for each model (expensive/slow).
    -   *Decision*: For now, assume list endpoint exists. If not (Anthropic), skip model check or mark as "Manual Verification Needed".

## 3. Execution
-   [ ] Run the updated script.
-   [ ] Analyze the output report.
