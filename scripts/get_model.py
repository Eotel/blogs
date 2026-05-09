#!/usr/bin/env python3
"""Detect the current coding agent's model ID from environment / config files.

Supports: Kimi Code CLI, Claude Code, Codex, and generic env overrides.

Priority:
1. Detect which agent is actually running by walking the process tree
2. Read ONLY that agent's config (to avoid picking up stale configs from other tools)
3. Fallback to the detected agent's environment variable
4. Empty string as last resort

If the running agent cannot be confidently identified, return empty rather than
guessing from unrelated tool configs.
"""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import Any, Callable


def _import_tomllib() -> Any:
    """Import the stdlib ``tomllib`` (3.11+), falling back to ``tomli`` (< 3.11)."""
    import importlib

    for name in ("tomllib", "tomli"):
        try:
            return importlib.import_module(name)
        except ModuleNotFoundError:
            continue
    return None


_tomllib: Any = _import_tomllib()


AGENT_ENV_VARS: dict[str, tuple[str, ...]] = {
    "kimi": ("KIMI_MODEL",),
    "claude": ("CLAUDE_MODEL", "ANTHROPIC_MODEL"),
    "codex": ("CODEX_MODEL", "OPENAI_MODEL"),
}


def get_parent_process_names() -> list[str]:
    """Walk up the process tree starting from the parent and collect process names.

    The current process is intentionally excluded so the caller (always
    ``python3``) does not pollute agent detection.
    """
    names: list[str] = []
    pid = os.getppid()
    for _ in range(20):  # safety limit
        if pid <= 1:
            break
        try:
            result = subprocess.run(
                ["ps", "-o", "ppid=,comm=", "-p", str(pid)],
                capture_output=True,
                text=True,
                check=False,
            )
        except Exception:
            break
        line = result.stdout.strip().split("\n", 1)[0].strip()
        parts = line.split()
        if len(parts) < 2:
            break
        try:
            ppid = int(parts[0])
        except ValueError:
            break
        names.append(" ".join(parts[1:]))
        pid = ppid
    return names


def detect_agent() -> str | None:
    """Return 'kimi', 'claude', 'codex', or None."""
    for name in (n.lower() for n in get_parent_process_names()):
        if "kimi" in name:
            return "kimi"
        if "claude" in name:
            return "claude"
        if "codex" in name:
            return "codex"
    return None


def from_env_for_agent(agent: str) -> str | None:
    """Return the first non-empty env var defined for the given agent."""
    for key in AGENT_ENV_VARS.get(agent, ()):
        val = os.environ.get(key)
        if val:
            return val
    return None


def _load_toml(path: Path) -> dict | None:
    if _tomllib is None or not path.exists():
        return None
    try:
        with path.open("rb") as f:
            return _tomllib.load(f)
    except Exception:
        return None


def from_kimi_config() -> str | None:
    data = _load_toml(Path.home() / ".kimi" / "config.toml")
    if not data:
        return None
    return data.get("default_model") or None


def _claude_config_paths() -> list[Path]:
    """Project-local .claude/settings.json takes precedence over user-level."""
    candidates: list[Path] = []
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR")
    if project_dir:
        candidates.append(Path(project_dir) / ".claude" / "settings.json")
    candidates.append(Path.cwd() / ".claude" / "settings.json")
    candidates.append(Path.home() / ".claude" / "settings.json")
    candidates.append(Path.home() / ".config" / "claude" / "settings.json")

    seen: set[Path] = set()
    unique: list[Path] = []
    for p in candidates:
        try:
            key = p.resolve()
        except OSError:
            key = p
        if key not in seen:
            seen.add(key)
            unique.append(p)
    return unique


def from_claude_config() -> str | None:
    for config_path in _claude_config_paths():
        if not config_path.exists():
            continue
        try:
            with config_path.open("r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            continue
        val = (
            data.get("model")
            or data.get("defaultModel")
            or (data.get("env") or {}).get("CLAUDE_MODEL")
        )
        if val:
            return val
    return None


def from_codex_config() -> str | None:
    data = _load_toml(Path.home() / ".codex" / "config.toml")
    if not data:
        return None
    return data.get("model") or None


AGENT_CONFIG_FNS: dict[str, Callable[[], str | None]] = {
    "kimi": from_kimi_config,
    "claude": from_claude_config,
    "codex": from_codex_config,
}


def detect_model() -> str:
    agent = detect_agent()
    if agent is None:
        # Without a confirmed running agent, refuse to guess from unrelated
        # tool configs — that would silently stamp posts with a stale model.
        return ""

    val = AGENT_CONFIG_FNS[agent]()
    if val:
        return val

    val = from_env_for_agent(agent)
    if val:
        return val

    return ""


def main() -> int:
    print(detect_model())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
