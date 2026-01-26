---
name: "context-aware-coding"
description: "Ensures AI understands directory context and keeps documentation up-to-date. Invoke BEFORE starting implementation in a directory AND AFTER finishing code changes."
---

# Context Aware Coding

This skill ensures that the AI developer is always aware of the specific context of the directory they are working in, and that this context is maintained for future sessions.

## When to Use

1.  **BEFORE Coding**: When user asks to implement a feature or modify code in a specific directory (e.g., `registry/`, `scripts/`).
2.  **AFTER Coding**: When a task is completed and code changes have been applied.

## Workflow

### Step 1: Context Acquisition (Pre-implementation)

Before writing or editing any code:

1.  Identify the target directory for the task.
2.  Check for the existence of `AI_README.md` in that directory.
3.  **Action**: Read the `AI_README.md` content.
4.  **Reasoning**: Use the rules, structure, and purpose defined in that file to guide your implementation.

### Step 2: Documentation Maintenance (Post-implementation)

After code changes are verified:

1.  Review the changes you just made.
2.  Ask: "Did I introduce a new pattern, file structure, or important rule?"
3.  **Action**:
    -   If **YES**: Update the `AI_README.md` in that directory to reflect the new reality.
    -   If **NO**: No action needed.

## Example Scenarios

*   **User**: "Add a new script to crawl Anthropic docs."
    *   **Agent**:
        1.  Target dir: `scripts/`.
        2.  Read `scripts/AI_README.md`.
        3.  See rule: "Use Python 3.10+, add type hints".
        4.  Implement script following these rules.
        5.  (Post-task) Update `scripts/AI_README.md` to list the new script in "Key Scripts".

*   **User**: "Add a new provider DeepSeek."
    *   **Agent**:
        1.  Target dir: `registry/`.
        2.  Read `registry/AI_README.md`.
        3.  See rule: "Do NOT put all providers in one file".
        4.  Create `registry/providers/deepseek.json`.
