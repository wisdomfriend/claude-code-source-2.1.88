# Claude Code Source (v2.1.88)

从 `@anthropic-ai/claude-code` npm 包的 `cli.js.map` 还原出的 TypeScript 源码，可在本项目内编译并运行。

## 快速开始

三步即可运行：

```bash
# 1. 安装依赖
bun install

# 2. 构建
bun run build

# 3. 运行
bun dist/cli.js
```

验证：

```bash
bun dist/cli.js --version
# 2.1.88 (Claude Code)
```

## 环境要求

| 工具 | 版本 | 用途 |
|------|------|------|
| Bun | >= 1.3.5 | 安装依赖 + 构建打包 |
| Node.js | >= 18 | 运行时 |
| Conda 环境 | `cherry-studio` | 你当前使用的本地环境 |

## 你的环境一条龙步骤（PowerShell）

```powershell
# 1) 进入环境
conda activate your-env

# 2) 检查运行时
node -v
npm -v

# 3) 如果 Bun 未安装（只需一次）
npm i -g bun
bun --version

# 4) 安装依赖并构建
cd claude-code-source
bun install
bun run build

# 5) 验证版本
bun dist/cli.js --version

# 6) node调试
# node .\cli.js --version
# node .\cli.js

# 7) docker调试官方版本 - 本项目提供了docker部署
# docker compose exec official-claude claude

# 8) docker源码版本
# docker compose exec custom-claude node /workspace/cli.js
```

## 修改版本号

```powershell
$env:CLAUDE_CODE_VERSION='2.1.88 (wisdomfriend)'
bun run build
bun dist/cli.js --version
# 期望输出：2.1.88 (wisdomfriend) (Claude Code)
```

清除变量：

```powershell
Remove-Item Env:CLAUDE_CODE_VERSION
```

## 构建原理

### `bun install` 做了什么

除了安装公开 npm 依赖外，`postinstall`（`scripts/postinstall.js`）会自动做两件事：

1. 创建私有包存根（stub）  - 源码包里缺少了一些
2. patch `commander` 支持多字符短参数（如 `-d2e`）

### 私有包存根列表

| 包名 | 作用 | 存根行为 |
|------|------|---------|
| `color-diff-napi` | 彩色 diff | 回退为纯文本能力 |
| `modifiers-napi` | macOS 修饰键检测 | 固定返回 `false` |
| `@ant/claude-for-chrome-mcp` | Chrome MCP | 功能禁用（不影响核心） |
| `@anthropic-ai/mcpb` | MCP bundle | 降级处理 |
| `@anthropic-ai/sandbox-runtime` | Linux 沙箱 | 返回不支持 |

### `bun run build` 做了什么

`build.ts` 使用 Bun bundler 编译 `src/entrypoints/cli.tsx` 到 `dist/cli.js`（约 21MB），并处理：

- `bun:bundle` 的 `feature()` 特性开关
- `MACRO.*` 编译期常量（版本、构建时间等）
- `.md/.txt` 文本资源导入
- `.node` 与部分可选 SDK external 处理

## 本地运行

```powershell
bun dist/cli.js
```

或：

```powershell
node dist/cli.js
```

## 容器部署（可选）

最小 `Dockerfile` 示例：

```dockerfile
FROM node:20-bookworm
WORKDIR /app
COPY dist/cli.js /app/dist/cli.js
COPY package.json /app/package.json
CMD ["node", "dist/cli.js", "--version"]
```

构建与运行：

```bash
docker build -t claude-cli-local .
docker run --rm claude-cli-local
```

## 常见问题

### 1) `Could not resolve "xxx"`

- 先执行 `bun install`，确认 `postinstall` 已成功运行。
- 若是新增私有包缺失，在 `scripts/postinstall.js` 添加对应存根。

### 2) 版本号不生效

- PowerShell 必须用：`$env:CLAUDE_CODE_VERSION='...'`
- `set CLAUDE_CODE_VERSION=...` 是 cmd 写法，不适用于 PowerShell。

### 3) 运行时报某功能不可用

- 部分私有包用的是降级存根，核心 CLI 可用，但个别高级功能可能受限。





```python

# 本地调试
# node .\cli.js --version
# node .\cli.js

# docker调试官方版本
# docker compose exec official-claude claude

# docker提示源码版本
# docker compose exec custom-claude node /workspace/cli.js

# 环境安装
# CLAUDE_CODE_VERSION
# CLAUDE_CODE_BUILD_TIME
# CLAUDE_CODE_FEATURES（逗号分隔，例如 BRIDGE_MODE,BG_SESSIONS）
# CLAUDE_CODE_VERSION_CHANGELOG
# CLAUDE_CODE_PACKAGE_URL
# CLAUDE_CODE_NATIVE_PACKAGE_URL
# npm install -D esbuild
# set CLAUDE_CODE_VERSION='2.1.88 (wisdomfriend)
# 

# conda activate cherry-studio
# cd D:\个人\文档\obsidian\python\claude\claude-code-source
# bun install
# bun run build
# bun dist/cli.js --version
# $env:CLAUDE_CODE_VERSION='2.1.88 (wisdomfriend)'
# bun run build
# bun dist/cli.js --version
# Remove-Item Env:CLAUDE_CODE_VERSION

```