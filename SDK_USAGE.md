# SDK 使用指南

本项目提供了 Python、Node.js (JavaScript) 和 Go 三种语言的 SDK，方便开发者快速集成。

## 1. Python SDK

### 安装
目前支持通过本地路径或 Git 仓库安装。

**方式 A: 本地开发安装 (推荐)**
在你的项目环境中，指向本项目本地路径：
```bash
# 假设 LLM-List 位于 ../LLM-List
pip install -e ../LLM-List/sdks/python
```

**方式 B: 从 GitHub 直接安装**
```bash
pip install "git+https://github.com/lone-yu-cmd/LLM-List.git#subdirectory=sdks/python"
```

### 使用示例
```python
import llm_list

# 获取所有厂商
providers = llm_list.get_providers()
print(f"Total providers: {len(providers)}")

# 获取 OpenAI 的所有聊天模型
openai_models = llm_list.get_models("openai")
for model in openai_models:
    print(f"- {model['name']} ({model['id']})")
```

---

## 2. Node.js (JavaScript) SDK

### 安装
**方式 A: 从 NPM 安装 (推荐)**
```bash
npm install llm-list
# 或者
pnpm add llm-list
# 或者
yarn add llm-list
```

**方式 B: 本地依赖 (用于开发调试)**
在你的 `package.json` 中添加：
```json
{
  "dependencies": {
    "llm-list": "file:../LLM-List/sdks/js"
  }
}
```
然后运行安装命令。

**方式 C: 从 Git 安装**
*注意：标准 npm 不支持直接安装 Git 仓库的子目录。*
如果您想通过 Git 安装，建议克隆整个仓库并使用 `npm link` 或 `file:` 协议。
或者，如果您使用 Yarn (v2+)，可以使用：
```bash
yarn add "https://github.com/lone-yu-cmd/LLM-List.git#workspace=llm-list"
```
(前提是仓库配置了 yarn workspaces)

目前最稳妥的方式是下载/克隆本仓库，然后通过本地路径引用。

### 使用示例
```javascript
const registry = require('llm-list');

// 获取所有 Provider
const providers = registry.getProviders();
console.log(`Loaded ${providers.length} providers`);

// 获取特定模型
const claude = registry.getModel('anthropic', 'claude-3-5-sonnet-20241022');
console.log(claude);
```

---

## 3. Go SDK

### 安装
使用 `go get` 获取模块：

```bash
go get github.com/lone-yu-cmd/LLM-List/sdks/go
```

### 使用示例
```go
package main

import (
    "fmt"
    "log"
    "github.com/lone-yu-cmd/LLM-List/sdks/go" // 包名为 llmlist
)

func main() {
    // 获取所有 Provider
    providers, err := llmlist.GetProviders()
    if err != nil {
        log.Fatal(err)
    }
    
    fmt.Printf("Loaded %d providers\n", len(providers))
    
    // 获取特定 Provider
    openai, _ := llmlist.GetProvider("openai")
    fmt.Printf("OpenAI Website: %s\n", openai.Website)
}
```
