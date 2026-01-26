# AI Context: Specs Directory

> **Note for AI Agents**: This directory implements the Spec-Driven Development workflow.

## Structure
*   Each subdirectory (e.g., `001-core-registry/`) represents a distinct Feature or Epic.
*   Directory names follow the pattern: `{number}-{short-name}`.

## File Standards
Inside each feature directory:
*   **`spec.md`**: (Source of Truth) The functional requirements and user stories.
*   **`plan.md`**: The technical implementation plan and architecture decisions.
*   **`tasks.md`**: The execution checklist.

## Usage
*   When starting a task, **READ** the `plan.md` in the relevant subdirectory to understand context.
*   When completing a task, **UPDATE** the `tasks.md` to mark it as `[x]`.
