#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Claude Code launcher with DeepSeek-compatible settings.

Usage:
  python run.py
  python run.py --mode claude
  python run.py --mode node -- --version
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
ENV_FILE = ROOT / ".env"


def load_env_file(env_path: Path) -> None:
    """以最小依赖方式读取 .env 文件。"""
    if not env_path.exists():
        return

    for raw in env_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def ensure_deepseek_defaults() -> None:
    os.environ.setdefault("ANTHROPIC_BASE_URL", "https://api.deepseek.com/anthropic")
    os.environ.setdefault("ANTHROPIC_MODEL", "deepseek-chat")
    os.environ.setdefault("ANTHROPIC_SMALL_FAST_MODEL", "deepseek-chat")


def validate_env() -> None:
    token = os.environ.get("ANTHROPIC_AUTH_TOKEN", "").strip()
    if not token:
        print("Error: ANTHROPIC_AUTH_TOKEN is not set.", file=sys.stderr)
        print("Please set ANTHROPIC_AUTH_TOKEN in .env to your DeepSeek API key.", file=sys.stderr)
        sys.exit(1)


def build_command(mode: str, passthrough: list[str]) -> list[str]:
    if mode == "claude":
        return ["claude", *passthrough]
    if mode == "node":
        return ["node", str(ROOT / "cli.js"), *passthrough]

    if shutil.which("claude"):
        return ["claude", *passthrough]
    return ["node", str(ROOT / "cli.js"), *passthrough]


def main() -> None:
    parser = argparse.ArgumentParser(description="Launch Claude Code in DeepSeek mode.")
    parser.add_argument(
        "--mode",
        choices=["auto", "claude", "node"],
        default="auto",
        help="auto prefers 'claude' and falls back to 'node cli.js'.",
    )
    parser.add_argument(
        "extra",
        nargs=argparse.REMAINDER,
        help="Extra args passed to claude/node. Use '--' before extra args.",
    )
    args = parser.parse_args()

    load_env_file(ENV_FILE)
    ensure_deepseek_defaults()
    validate_env()

    passthrough = args.extra
    if passthrough and passthrough[0] == "--":
        passthrough = passthrough[1:]

    cmd = build_command(args.mode, passthrough)

    print("== DeepSeek settings ==")
    print(f"ANTHROPIC_BASE_URL={os.environ.get('ANTHROPIC_BASE_URL', '')}")
    print(f"ANTHROPIC_MODEL={os.environ.get('ANTHROPIC_MODEL', '')}")
    print(f"ANTHROPIC_SMALL_FAST_MODEL={os.environ.get('ANTHROPIC_SMALL_FAST_MODEL', '')}")
    print(f"Command: {' '.join(cmd)}")

    try:
        completed = subprocess.run(cmd, cwd=str(ROOT), env=os.environ.copy())
        raise SystemExit(completed.returncode)
    except FileNotFoundError:
        print(f"Error: executable not found: {cmd[0]}", file=sys.stderr)
        print("Please install the required runtime (claude or node).", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()

