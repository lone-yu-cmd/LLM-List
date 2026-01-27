# LLMList

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**LLMList** 是一个标准化的大模型信息收集开源库。我们的目标是打造一个统一的、机器可读的 LLM 信息源，降低开发者集成不同大模型 API 的成本。

用户可以通过调用我们的 SDK 或直接读取 JSON 数据，快速获取主流大模型厂商的 API 协议、模型列表及配置信息。

## 项目所需依赖

- Python 3.8+
- Node.js 14+
- npm 或 yarn
- Playwright (用于 API 文档爬取)

### 项目启动命令

```bash
pip3 install -r requirements.txt
python3 -m playwright install chromium
```

## 📂 项目结构

本项目采用 Monorepo 结构，核心数据与多语言 SDK 位于同一仓库，确保协议与实现的一致性。

```
LLM-List/
├── registry/
│   └── providers/             # 厂商数据源：每个厂商一个独立的 JSON 文件
│       └── openai.json
├── llm_registry.json          # 自动生成的完整注册表（构建产物）
├── schema/                    # JSON Schema 定义文件
├── scripts/                   # 维护脚本
│   ├── build_registry.py      # 构建脚本
│   ├── generate_schema.py     # Schema 生成脚本
│   ├── validate_format.py     # Schema 格式校验脚本
│   ├── crawl_api_docs.py      # API 文档爬虫脚本
│   └── scrape_content.py      # 文档内容抓取脚本
├── sdks/                      # 多语言 SDK
│   ├── python/                # Python SDK (llm-list)
│   ├── go/                    # Go SDK (github.com/lone-yu-cmd/LLM-List/sdks/go)
│   └── js/                    # Node.js SDK (llm-list)
├── LICENSE                    # MIT 许可证
├── README.md                  # 项目说明
├── SDK_USAGE.md               # SDK 使用指南
└── CONTRIBUTING.md            # 贡献指南
```

## 🚀 快速开始

### 📦 使用 SDK (推荐)

我们提供了 Python, Node.js 和 Go 的官方 SDK。详细安装和使用说明请参考 [SDK 使用指南](SDK_USAGE.md)。

**Python**
```bash
pip install "git+https://github.com/lone-yu-cmd/LLM-List.git#subdirectory=sdks/python"
```

**Node.js**
```bash
npm install github:lone-yu-cmd/LLM-List#subdirectory=sdks/js
```

**Go**
```bash
go get github.com/lone-yu-cmd/LLM-List/sdks/go
```

### 直接使用 JSON 数据

核心数据存储在根目录的 [llm_registry.json](llm_registry.json) 文件中。这个文件是自动构建生成的，包含了所有支持的厂商信息。你可以直接在你的应用中加载此文件来获取最新的模型列表。

### 脚本说明
```bash
# 生成最新的 llm_registry.json
npm run build
```

```bash
# 校验 Schema 格式完整性 (检查是否缺失 format 字段)
npm run validate:format
```

```bash
# 爬取厂商 API 文档页面中的所有链接
# 用法: npm run crawl -- <url>
npm run crawl -- https://open.bigmodel.cn/dev/api
```

```bash
# 爬取文档内容并转换为 Markdown
# 用法: npm run scrape -- <url1> [url2 ...] [urls.json]
npm run scrape -- https://example.com/docs
```

## 🛠️ 数据协议说明

为了覆盖不同厂商的差异，我们设计了一套标准化的 JSON 协议。

- **Providers**: 顶级数组，包含所有接入的厂商。
- **API Config**: 描述如何进行 HTTP 调用（Base URL, Auth Header 等）。
- **Models**: 该厂商支持的模型列表，包含上下文窗口、定价（可选）和功能特性（如 Vision, Function Calling）。

## 🤝 贡献指南

欢迎提交 PR 添加新的模型或修正现有信息！请阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详情。

## 📄 许可证

本项目基于 [MIT License](LICENSE) 开源。

## 后续计划

- 完善多语言 SDK 实现
- 增加模型评估指标（如速度、成本）
- 持续更新模型列表，保持与厂商同步
- 加入厂商MCP调用说明
