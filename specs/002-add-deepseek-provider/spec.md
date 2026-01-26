# Feature Specification: Add DeepSeek Provider

**Feature Branch**: `feature/add-deepseek-provider`
**Created**: 2026-01-27
**Status**: Draft
**Input**: User description: "调用spec-kit 帮我添加deepseek模型"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Integrate DeepSeek Provider (Priority: P1)

As a developer using LLM-List, I want to access DeepSeek's latest models (V3.2 Chat and Reasoner) so that I can use their cost-effective and high-performance reasoning capabilities.

**Why this priority**: DeepSeek is a major provider with competitive models (V3.2) that users explicitly requested.

**Independent Test**:
- Can be tested by running the registry build and verifying `deepseek.json` is included.
- Can be tested by running `test_registry_data.py` to ensure schema compliance.

**Acceptance Scenarios**:

1. **Given** the registry build script is run, **When** I check the output, **Then** `deepseek` should be listed as a provider.
2. **Given** the generated `llm_registry.json`, **When** I inspect the DeepSeek provider, **Then** it should contain `deepseek-chat` and `deepseek-reasoner` models with correct context windows (128k).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST include a new provider file `registry/providers/deepseek.json`.
- **FR-002**: The DeepSeek provider MUST be configured with Base URL `https://api.deepseek.com`.
- **FR-003**: The DeepSeek provider MUST include `deepseek-chat` (V3.2 Non-thinking) with 128k context.
- **FR-004**: The DeepSeek provider MUST include `deepseek-reasoner` (V3.2 Thinking) with 128k context.
- **FR-005**: The system MUST validate the new provider against the registry schema.
- **FR-006**: The system MUST rebuild the `llm_registry.json` artifact including DeepSeek.

### Key Entities

- **Provider**: DeepSeek (ID: `deepseek`)
- **Models**:
    - `deepseek-chat` (Context: 128k, Output: 8k)
    - `deepseek-reasoner` (Context: 128k, Output: 64k)
