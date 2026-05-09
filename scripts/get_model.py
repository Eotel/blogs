#!/usr/bin/env python3
"""Detect the current coding agent's model ID from environment / config files.

Supports: Kimi Code CLI, Claude Code, Codex, and generic env overrides.

Priority:
1. Detect which agent is actually running by walking the process tree
2. Read ONLY that agent's config (to avoid picking up stale configs from other tools)
3. Fallback to environment variables if config is missing
4. Empty string as last resort
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


def get_parent_process_names() -> list[str]:
    """Walk up the process tree and collect parent process names."""
    names: list[str] = []
    pid = os.getpid()
    for _ in range(20):  # safety limit
        try:
            result = subprocess.run(
                ["ps", "-o", "ppid=,comm=", "-p", str(pid)],
                capture_output=True,
                text=True,
                check=False,
            )
            line = result.stdout.strip().split("\n")[0].strip()
            parts = line.split()
            if len(parts) >= 2:
                ppid = int(parts[0])
                comm = " ".join(parts[1:])
                names.append(comm)
                pid = ppid
                if pid <= 1:
                    break
        except Exception:
            break
    return names


def detect_agent() -> str | None:
    """Return 'kimi', 'claude', 'codex', or None."""
    names = get_parent_process_names()
    names_lower = [n.lower() for n in names]
    for name in names_lower:
        if "kimi" in name:
            return "kimi"
        if "claude" in name:
            return "claude"
        if "codex" in name:
            return "codex"
    return None


def from_env() -> str | None:
    for key in (
        "KIMI_MODEL",
        "CLAUDE_MODEL",
        "CODEX_MODEL",
        "ANTHROPIC_MODEL",
        "OPENAI_MODEL",
    ):
        val = os.environ.get(key)
        if val:
            return val
    return None


def from_kimi_config() -> str | None:
    config_path = Path.home() / ".kimi" / "config.toml"
    if not config_path.exists():
        return None
    try:
        import tomllib

        with config_path.open("rb") as f:
            data = tomllib.load(f)
        return data.get("default_model") or None
    except Exception:
        return None


def from_claude_config() -> str | None:
    for config_path in (
        Path.home() / ".claude" / "settings.json",
        Path.home() / ".config" / "claude" / "settings.json",
    ):
        if not config_path.exists():
            continue
        try:
            with config_path.open("r", encoding="utf-8") as f:
                data = json.load(f)
            return (
                data.get("model")
                or data.get("defaultModel")
                or data.get("env", {}).get("CLAUDE_MODEL")
                or None
            )
        except Exception:
            continue
    return None


def from_codex_config() -> str | None:
    config_path = Path.home() / ".codex" / "config.toml"
    if not config_path.exists():
        return None
    try:
        import tomllib

        with config_path.open("rb") as f:
            data = tomllib.load(f)
        return data.get("model") or None
    except Exception:
        return None


def detect_model() -> str:
    agent = detect_agent()

    # Try agent-specific config first
    if agent == "kimi":
        val = from_kimi_config()
        if val:
            return val
    elif agent == "claude":
        val = from_claude_config()
        if val:
            return val
    elif agent == "codex":
        val = from_codex_config()
        if val:
            return val

    # Fallback to env vars (useful when agent was launched with explicit model)
    val = from_env()
    if val:
        return val

    # If agent detection failed entirely, try all configs as last resort
    if agent is None:
        for fn in (from_kimi_config, from_claude_config, from_codex_config):
            val = fn()
            if val:
                return val

    return ""


def main(argv: list[str] | None = None) -> int:
    print(detect_model())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
