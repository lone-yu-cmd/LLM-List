# Plan: Registry Sync Skill

## 1. Technical Approach
We will encapsulate the existing `scripts/build_registry.py` logic into a new Trae Skill named `registry-syncer`. This aligns with the project's "Skill-Driven" architecture.

The skill will primarily act as a wrapper around the build script, ensuring consistent execution context and potentially chaining validation steps.

## 2. Architecture
- **Skill Directory**: `.trae/skills/registry-syncer`
- **Core Script**: `scripts/build_registry.py` (Existing)
- **Dependencies**: 
    - `python3`
    - `registry-validator` (Optional dependency for pre-flight checks)

## 3. Skill Definition (Draft)
- **Name**: `registry-syncer`
- **Description**: Rebuilds the LLM registry from source files and synchronizes it to all SDKs (Go, JS, Python).
- **Instructions**:
    - Locate `scripts/build_registry.py`.
    - Run the script.
    - Validate output.

## 4. Verification Plan
- **Manual Test**: Run `python3 scripts/build_registry.py` and verify file timestamps in SDKs.
- **Skill Test**: Invoke the skill via the `Skill` tool (if possible) or simulate the agent's behavior following the skill instructions.

## 5. Risks
- If `scripts/build_registry.py` is moved or renamed, the skill will break. -> *Mitigation*: The skill should verify script existence.
