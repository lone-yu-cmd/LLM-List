# Spec: Registry Sync Skill

## 1. Background
The project maintains a central registry of LLM providers in `registry/providers/*.json`. These files are aggregated into a root `llm_registry.json`. Currently, this file also needs to be distributed to various SDKs (`sdks/go`, `sdks/js`, `sdks/python`) to ensure they have the latest model definitions. While a `scripts/build_registry.py` script exists that handles this, there is no dedicated "Skill" to expose this capability within the agentic workflow or to allow for future enhancements (like validation hooks).

## 2. Goals
- Create a new skill named `registry-syncer` (or similar).
- The skill should provide a command to rebuild the registry from source files.
- The skill must ensure the rebuilt registry is distributed to all supported SDKs.
- The skill should be the canonical way to update registry data across the project.

## 3. User Stories
- **As a developer**, after I add a new model to `registry/providers/openai.json`, I want to run a simple skill command so that the change is reflected in the Go, Python, and JS SDKs immediately.

## 4. Functional Requirements
1.  **Skill Registration**: The skill must be registered in `.trae/skills/` with a `SKILL.md`.
2.  **Execution**: The skill should execute the existing `scripts/build_registry.py` script, which already contains the logic for merging and distribution.
3.  **Feedback**: The skill should report success or failure to the user.
4.  **Extensibility**: The skill structure should allow adding validation steps (like `registry-validator`) before or after the sync in the future.

## 5. Success Criteria
- Invoking the skill successfully updates `llm_registry.json` in the root and all SDK directories.
- The skill is discoverable via `ls .trae/skills`.
