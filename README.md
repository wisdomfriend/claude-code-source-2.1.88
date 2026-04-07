# Claude Code

![](https://img.shields.io/badge/Node.js-18%2B-brightgreen?style=flat-square) [![npm]](https://www.npmjs.com/package/@anthropic-ai/claude-code)

[npm]: https://img.shields.io/npm/v/@anthropic-ai/claude-code.svg?style=flat-square

Claude Code is an agentic coding tool that lives in your terminal, understands your codebase, and helps you code faster by executing routine tasks, explaining complex code, and handling git workflows -- all through natural language commands. Use it in your terminal, IDE, or tag @claude on Github.

**Learn more at [Claude Code Homepage](https://claude.com/product/claude-code)** | [Documentation](https://code.claude.com/docs/en/overview)

<img src="https://github.com/anthropics/claude-code/blob/main/demo.gif?raw=1" />

## Get started

1. Install Claude Code:

```sh
npm install -g @anthropic-ai/claude-code
```

2. Navigate to your project directory and run `claude`.

## Reporting Bugs

We welcome your feedback. Use the `/bug` command to report issues directly within Claude Code, or file a [GitHub issue](https://github.com/anthropics/claude-code/issues).

## Connect on Discord

Join the [Claude Developers Discord](https://anthropic.com/discord) to connect with other developers using Claude Code. Get help, share feedback, and discuss your projects with the community.

## Data collection, usage, and retention

When you use Claude Code, we collect feedback, which includes usage data (such as code acceptance or rejections), associated conversation data, and user feedback submitted via the `/bug` command.

### How we use your data

See our [data usage policies](https://code.claude.com/docs/en/data-usage).

### Privacy safeguards

We have implemented several safeguards to protect your data, including limited retention periods for sensitive information and restricted access to user session data.

For full details, please review our [Commercial Terms of Service](https://www.anthropic.com/legal/commercial-terms) and [Privacy Policy](https://www.anthropic.com/legal/privacy).



# 调试代码

```python
$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"
$env:CONDA_NO_PLUGINS = "true"
conda activate cherry-studio

node --version
cd "D:\个人\文档\obsidian\python\claude\claude-code-source"
node .\cli.js --version
node .\cli.js


改的是 docker-compose.yml 里的环境变量/挂载/命令等：
不需要“编译镜像”，但需要重建容器生效：
docker compose up -d
（通常会自动重建相关容器）

改的是 Dockerfile 或镜像构建相关内容：
需要重新构建镜像：
docker compose up -d --build

想强制确保一定重建容器（即使 Compose 没检测到变化）：
docker compose up -d --force-recreate

官方 Claude Code:
docker compose exec official-claude claude

你自己的 cli.js：
docker compose exec custom-claude node /workspace/cli.js

参考博文:
https://zhuanlan.zhihu.com/p/2004933500453818798

```

![image-20260408053503972](C:\Users\62792\AppData\Roaming\Typora\typora-user-images\image-20260408053503972.png)
