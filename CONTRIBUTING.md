# 贡献指南 (Contributing Guide)

感谢你对 LLMList 的关注！我们需要社区的帮助来保持模型信息的准确性和时效性。

## 如何贡献

### 1. 添加或更新模型信息

我们采用分散管理、集中构建的模式。所有的厂商数据都存储在 `registry/providers/` 目录下，每个厂商一个 JSON 文件。

**如果你要添加新的厂商：**
1. 在 `registry/providers/` 目录下创建一个新的 JSON 文件（例如 `anthropic.json`）。
2. 参照 `openai.json` 的格式填写厂商信息。
3. 运行构建脚本 `python3 scripts/build_registry.py` 生成新的 `llm_registry.json`。

**如果你要修改现有模型：**
1. 找到对应的厂商文件（如 `registry/providers/openai.json`）。
2. 修改内容。
3. 运行构建脚本更新主文件。

**注意：** 请不要直接手动修改根目录的 `llm_registry.json`，因为它是自动生成的，下次运行脚本时会被覆盖。

**修改规范：**
- 保持 JSON 格式整洁（使用 2 空格缩进）。
- 确保 `id` 字段与厂商 API 文档中的 Model ID 完全一致。
- 尽量补充完整的 `description` 和 `context_window` 信息。

### 2. 提交代码

1. Fork 本仓库。
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)。
3. 提交你的修改 (`git commit -m 'Add some AmazingFeature'`)。
4. 推送到分支 (`git push origin feature/AmazingFeature`)。
5. 开启一个 Pull Request。

## 行为准则

请确保提交的内容真实可靠，尽量附上官方文档链接作为参考。
