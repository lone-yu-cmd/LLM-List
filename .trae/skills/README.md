# Available Skills

This directory contains the skills available to the AI agent. This file is **automatically updated** when skills are created or modified.

| Skill Name | Main Function | Trigger / When to Use |
|------------|---------------|-----------------------|
| [auto-committer](./auto-committer/SKILL.md) | Automates code commits: analyzes git diffs, updates CHANGELOG.md, generates conventional commit messages, and commits changes. Invoke when user wants to 'commit', 'finish task', or 'release'. | - User says "commit my changes"<br>- User says "I'm done with this task"<br>- User asks to "update changelog and commit" |
| [code-explainer](./code-explainer/SKILL.md) | Generates a structured analysis report for a given code snippet. Invoke when user asks to explain, understand, or analyze specific code. | Invoke this skill when the user:<br>- Asks "What does this code do?"<br>- Asks "Explain this file to me." |
| [context-aware-coding](./context-aware-coding/SKILL.md) | Ensures AI understands directory context and keeps documentation up-to-date. Invoke BEFORE starting implementation in a directory AND AFTER finishing code changes. | 1.  **BEFORE Coding**: When user asks to implement a feature or modify code in a specific directory (e.g., `registry/`, `scripts/`).<br>2.  **AFTER Coding**: When a task is completed and code changes have been applied. |
| [project-constitution](./project-constitution/SKILL.md) | Contains the core architecture, development guidelines, and contribution rules for the LLM-List project. Invoke when user asks about project rules, architecture, or how to contribute. | See details in file |
| [registry-validator](./registry-validator/SKILL.md) | Ensures data integrity by running validation tests. Invoke AUTOMATICALLY whenever JSON files in 'registry/' are modified. | **Invoke immediately after**:<br>- Creating a new provider JSON file.<br>- Modifying an existing provider or schema. |
| [spec-kit-workflow](./spec-kit-workflow/SKILL.md) | Guides the development process using GitHub Spec Kit methodology: Specify -> Plan -> Tasks -> Implement. Invoke when user wants to start a new feature or strictly follow the spec-driven workflow. | Invoke this skill when:<br>- The user wants to start a new feature ("I want to add login").<br>- The user asks to "use spec kit" or "follow the spec process". |

> **Note**: To create a new skill, use the `skill-creator` tool. This README will be updated automatically.