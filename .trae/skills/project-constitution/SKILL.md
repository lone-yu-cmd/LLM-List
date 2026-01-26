---
name: "project-constitution"
description: "Contains the core architecture, development guidelines, and contribution rules for the LLM-List project. Invoke when user asks about project rules, architecture, or how to contribute."
---

# LLM-List Project Constitution

## 1. 核心架构设计

本项目采用 **"分散管理，集中构建" (Distributed Management, Centralized Build)** 的 Monorepo 模式。

### 目录结构
```text
LLM-List/
├── llm_registry.json          # [自动生成] 最终产物，包含所有厂商的完整信息
├── docs_dump/                 # [自动生成] 爬虫抓取的原始文档 (Markdown 格式)
├── registry/                  # 核心数据源目录
│   ├── providers/             # 厂商层级：每个厂商一个独立的 JSON 文件
│   │   ├── openai.json
│   │   └── zhipuai.json
│   ├── schemas/               # 接口定义层级：存放具体的 API 参数定义
│   │   └── {provider_id}/     # 按厂商隔离
│   │       └── endpoints/     # 接口业务分类
│   │           └── chat_completions.json  # 具体的接口定义文件
│   └── i18n/                  # 国际化错误码层级
│       └── {provider_id}/     # 按厂商隔离
│           ├── en.json        # 英文错误描述
│           └── zh.json        # 中文错误描述
├── sdks/                      # 多语言 SDK 目录
│   ├── js/                    # JavaScript SDK
│   │   ├── index.js
│   │   └── package.json
│   └── [python/go/...]        # 其他语言 SDK
├── scripts/
│   ├── build_registry.py      # 构建脚本：负责合并 providers、解析 $ref、生成 llm_registry.json
│   ├── validate_format.py     # 校验脚本：检查 Schema 是否缺失 format 字段
│   ├── crawl_api_docs.py      # 爬虫脚本：自动提取厂商 API 文档页面的所有链接
│   └── scrape_content.py      # 抓取脚本：利用 Playwright 抓取网页内容并转为 Markdown
└── package.json               # 任务管理：通过 npm run 触发各类 Python 脚本
```

## 2. 数据协议规范 (JSON Protocol)

### 2.1 厂商配置 (Provider Config)
位于 `registry/providers/{provider_id}.json`。
*   **id**: 厂商唯一标识 (如 `openai`, `zhipuai`)。
*   **api_config**:
    *   **protocol**: 协议类型 (如 `rest`).
    *   **protocol_format**: 兼容格式声明 (如 `openai` 表示完全兼容 OpenAI SDK).
    *   **base_url**: 基础 API 地址.
    *   **auth**: 鉴权配置 (type, header_key, token_prefix, instructions).
    *   **endpoints**: 接口列表，**必须**使用 `$ref` 引用 `schemas/` 下的独立文件.
    *   **error_codes**: 错误码列表 (code, description).
*   **models**: 模型列表，包含 `id`, `context_window`, `max_output_tokens`, `pricing`, `features` 等元数据.

### 2.2 接口定义 (Endpoint Schema)
位于 `registry/schemas/{provider_id}/endpoints/{endpoint_name}.json`。
*   **文件名**: 使用下划线命名法，对应 API 路径 (如 `/chat/completions` -> `chat_completions.json`).
*   **内容**: 必须包含完整的接口元数据。
    *   `path`: 接口相对路径 (如 `/chat/completions`).
    *   `method`: HTTP 方法 (如 `POST`).
    *   `request_parameters`: 请求参数定义 (JSON Schema 风格)，必须包含 `type` 和 `format`。
    *   `response_parameters`: 响应参数定义 (JSON Schema 风格)，必须包含 `type` 和 `format`。

### 2.3 国际化 (i18n)
位于 `registry/i18n/{provider_id}/{lang}.json`。
*   Key: 错误码 (String).
*   Value: 本地化的错误描述 (String).

## 3. 自动化与工具链

项目提供了一系列 npm 命令来辅助开发：

*   **构建**: `npm run build`
    *   运行 `scripts/build_registry.py`，合并所有分散文件生成 `llm_registry.json`。
*   **校验**: `npm run validate:format`
    *   运行 `scripts/validate_format.py`，递归检查所有 Schema 字段是否包含 OpenAPI 风格的 `format` 定义。
*   **爬取链接**: `npm run crawl -- <url>`
    *   运行 `scripts/crawl_api_docs.py`，从文档主页提取侧边栏链接。
*   **抓取内容**: `npm run scrape -- <url> [urls...]`
    *   运行 `scripts/scrape_content.py`，支持批量 URL 抓取，利用 Playwright 处理动态渲染页面，并保存为 Markdown 到 `docs_dump/` 目录。

## 4. SDK 开发规范

所有的 SDK 位于 `sdks/` 目录下。

1.  **数据源**: SDK **不应**在自身目录内维护 `llm_registry.json` 的副本。
2.  **引用方式**: SDK 必须直接读取项目根目录的 `../../llm_registry.json` 文件。
3.  **标准方法**: 所有语言的 SDK 应至少提供以下标准方法：
    *   `getProviders()`: 获取厂商列表。
    *   `getProviderModels(providerId)`: 获取指定厂商的模型列表。
    *   `getProviderWebsite(providerId)`: 获取厂商官网。
    *   `getProviderAuth(providerId)`: 获取厂商鉴权配置。

## 5. 开发流程 (Workflow)

1.  **数据采集**:
    *   使用 `npm run scrape` 抓取厂商最新的模型文档或 API 文档。
    *   分析 `docs_dump/` 下的 Markdown 文件，提取模型参数和接口定义。
2.  **数据录入**:
    *   **不要**直接编辑根目录的 `llm_registry.json`。
    *   新增厂商：在 `registry/providers/` 创建新文件。
    *   修改接口：在 `registry/schemas/` 修改对应的 Schema 文件。
    *   更新模型：在 `registry/providers/{id}.json` 的 `models` 数组中添加/更新模型。
3.  **构建与校验**:
    *   运行 `npm run validate:format` 确保 Schema 规范。
    *   运行 `npm run build` 生成最终文件。
4.  **SDK 验证**:
    *   进入 `sdks/{lang}/` 目录运行测试，确保 SDK 能正确读取新的 Registry 数据。

## 6. 关键原则

1.  **Single Source of Truth**: `registry/` 目录下的分散文件是唯一真实数据源。
2.  **高内聚**: 接口的 `path`, `method`, `request_parameters`, `response_parameters` 必须定义在同一个 Schema 文件中。
3.  **Schema First**: 所有的接口变更应优先修改 Schema 定义。
4.  **OpenAPI 风格**: 参数定义应尽可能遵循 OpenAPI (Swagger) 的字段规范，特别是 `type` 和 `format` 必须成对出现 (如 `type: integer, format: int64`)，以便于生成强类型 SDK。
5.  **自动化优先**: 优先编写或使用脚本完成重复性工作（如格式检查、文档抓取）。
