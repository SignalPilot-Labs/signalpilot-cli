# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SignalPilot CLI (`sp`) is a self-bootstrapping CLI tool that creates a global workspace for Jupyter-powered data analysis with built-in AI agent support. It follows the **Config SPEC** architecture with a single `~/SignalPilotHome/` workspace containing user and team workspaces.

**User journey:**
```bash
# 1. Install uv (via trusted package manager)
brew install uv

# 2. Self-bootstrap SignalPilot (one-time)
uvx sp-cli activate

# 3. Initialize workspace
sp init

# 4. Launch JupyterLab
sp lab
```

**Total time: <3 minutes** from zero to working environment.

## Development Commands

### Local Development

```bash
# Create venv and install in dev mode
uv venv .venv && uv pip install -e ".[dev]"

# Run CLI commands
.venv/bin/sp --help
.venv/bin/sp activate          # Test self-bootstrap (uses dev install)
.venv/bin/sp init              # Test workspace initialization
.venv/bin/sp lab --no-browser  # Test Jupyter Lab launch
.venv/bin/sp lab --team        # Test team workspace
.venv/bin/sp install           # Test repair/reinstall
.venv/bin/sp upgrade           # Test upgrade mechanism

# Run tests
.venv/bin/pytest tests/ -v

# Run single test
.venv/bin/pytest tests/test_cli.py::TestCLI::test_help -v
```

### Docker Testing Environment

Test in a clean environment with Docker:

```bash
# Quick start (interactive script)
./docker-test.sh

# Or manually:
docker-compose up -d
docker-compose exec sp-cli-dev /bin/bash

# Inside container:
sp init
sp lab --port 9999 --no-browser

# Access Jupyter Lab:
# http://localhost:9999

# Cleanup
docker-compose down -v
```

**Docker benefits:**
- Clean environment for each test
- No pollution of your local system
- Test installation flow from scratch
- Consistent Python 3.12 environment

## Directory Structure

### Repository Structure
```
sp-cli/
├── Dockerfile                  # Docker testing image
├── docker-compose.yml          # Docker compose config
├── docker-test.sh              # Docker test helper
├── pyproject.toml              # Package definition
├── tests/                      # Test suite
│   ├── test_cli.py
│   ├── test_activate.py
│   ├── test_init.py
│   ├── test_lab.py
│   ├── test_install.py
│   └── test_upgrade.py
└── sp/
    ├── __init__.py
    ├── main.py                 # Typer CLI entry point
    ├── config.py               # Config SPEC constants
    ├── commands/
    │   ├── activate.py         # sp activate
    │   ├── init.py             # sp init
    │   ├── lab.py              # sp lab
    │   ├── install.py          # sp install
    │   └── upgrade.py          # sp upgrade
    ├── core/
    │   ├── environment.py      # uv/venv management
    │   └── jupyter.py          # JupyterLab launch
    └── ui/
        └── console.py          # Rich console, branded output
```

### Global Workspace Structure (Config SPEC)
Created at `~/SignalPilotHome/` by `sp init`:
```
~/SignalPilotHome/
├── .signalpilot/
│   ├── defaults/                       # Shipped defaults (updated on upgrade)
│   │   ├── sp-core.toml
│   │   ├── jupyter_server_config.py
│   │   └── cli.toml
│   ├── user-sp-core.toml               # User overrides
│   ├── user-jupyter_server_config.py
│   └── user-cli.toml
├── default-skills/                     # Built-in agent skills
│   └── sql-optimization/SKILL.md
├── default-rules/                      # Built-in agent rules
│   ├── analyze.md
│   ├── explain.md
│   └── investigate.md
├── connect/                            # Credentials (NEVER agent-accessible)
│   ├── db.toml
│   ├── mcp.json
│   ├── .env
│   └── folders/manifest.toml
├── system/                             # Installation metadata
│   ├── version.toml
│   ├── logs/
│   └── migrations/
├── .venv/                              # Shared Python environment
├── pyproject.toml                      # Shared dependencies
├── user-workspace/                     # ═══ AGENT WORKSPACE (personal) ═══
│   ├── demo-project/
│   │   └── demo-quickstart.ipynb
│   ├── skills/
│   │   └── skill-upload-registry.json
│   └── rules/
└── team-workspace/                     # ═══ AGENT WORKSPACE (team) ═══
    ├── notebooks/
    ├── scripts/
    ├── skills/
    │   └── skill-upload-registry.json
    └── rules/
```

## Key Technical Details

### Dependencies
- `typer>=0.12.0` - CLI framework
- `rich>=13.0.0` - Beautiful terminal output
- `pytest>=8.0.0` - Testing (dev dependency)

### Environment Variables for Jupyter
SignalPilot only customizes the Jupyter config directory:
```python
JUPYTER_CONFIG_DIR=~/SignalPilotHome/.signalpilot
```

All other Jupyter directories (data, runtime, kernels) use defaults in the `.venv`.

## Key Architecture Decisions

### Config SPEC Architecture
- **Global workspace**: Single `~/SignalPilotHome/` for all work
- **User workspace**: Personal notebooks and scripts (`user-workspace/`)
- **Team workspace**: Collaborative, git-tracked work (`team-workspace/`)
- **Agent containment**: Allowlist-based filesystem access
- **Credential isolation**: `connect/` directory NEVER accessible to agents

### Self-Bootstrapping Installation
- Primary installation: `uvx sp-cli activate` (no curl|sh needed)
- Users install `uv` via trusted package managers (brew, winget, cargo)
- `sp activate` creates wrapper script at `~/.local/bin/sp`
- More trustworthy than `curl | sh` patterns

### Five Core Commands
1. **`sp activate`** - Self-bootstrap (run via `uvx sp-cli activate`)
2. **`sp init`** - Initialize ~/SignalPilotHome/ workspace
3. **`sp lab`** - Launch Jupyter Lab from user or team workspace
4. **`sp install`** - Repair/reinstall workspace (with `--force` flag)
5. **`sp upgrade`** - Upgrade CLI to latest version

### Agent Containment
**Agent-Accessible (allowlist):**
- ✅ `user-workspace/` (full access)
- ✅ `team-workspace/` (full access)
- ✅ `default-skills/` (read-only)
- ✅ `default-rules/` (read-only)

**Agent-Inaccessible (blocklist):**
- ❌ `connect/` (credentials, API keys)
- ❌ `.signalpilot/` (system configuration)
- ❌ `system/` (installation metadata)
- ❌ `.venv/` (Python environment)

### Brand Colors (for Rich styling)
```python
BRAND_PRIMARY = "#8B5CF6"    # Soft violet
BRAND_SECONDARY = "#A78BFA"  # Light violet
BRAND_SUCCESS = "#10B981"    # Green
BRAND_WARNING = "#F59E0B"    # Amber
BRAND_ERROR = "#EF4444"      # Red
BRAND_MUTED = "#6B7280"      # Gray
```

### UI Patterns
- Use Rich spinners for long operations
- Success: prefix with ✓ in BRAND_SUCCESS
- Error: prefix with ✗ in BRAND_ERROR
- Info: prefix with → in BRAND_MUTED
- Display branded panels for major operations (`sp init`)

## Command Implementation Details

### `sp activate` (Self-Bootstrap)
- **MUST** be run via `uvx sp-cli activate` (not as `sp activate`)
- Detects if running in uvx temp environment
- Creates `~/.local/bin/sp` wrapper script
- Adds `~/.local/bin` to PATH in shell rc files (.bashrc, .zshrc)
- Does NOT create `~/SignalPilotHome/` (that's done by `sp init`)

### `sp init` (Workspace Setup)
- **Idempotent** - safe to run multiple times
- Creates full `~/SignalPilotHome/` directory structure
- Creates `.venv/` with Python 3.12
- Installs core packages: `jupyterlab`, `ipykernel`, `pandas`, `numpy`
- Creates default config files
- Creates skill and rule registries
- Creates demo notebook in `user-workspace/demo-project/`

### `sp lab` (Workspace Launcher)
- Launches Jupyter Lab from `user-workspace/` (default) or `team-workspace/`
- Usage: `sp lab [--team] [--port=8888] [--no-browser]`
- Sets `JUPYTER_CONFIG_DIR` to `~/SignalPilotHome/.signalpilot/`
- Uses shared `.venv` at `~/SignalPilotHome/.venv`

### `sp install` (Repair)
- **Repair mode** (default): Reinstalls core packages, fixes broken dependencies
- **Force mode** (`--force`): Deletes `~/SignalPilotHome/` with confirmation prompt

### `sp upgrade` (Update)
- Checks PyPI for latest version
- Shows current vs latest version
- Prompts for confirmation
- Upgrades via `uv tool upgrade sp-cli`

## Development Workflow

When implementing commands:
1. Use Typer for CLI framework (type-hint based)
2. Use Rich for all terminal output (spinners, colors, formatting)
3. Follow UI patterns (✓ for success, ✗ for errors, → for info)
4. Always provide helpful error messages with next steps
5. Make operations idempotent where possible
6. Print clear output about what's happening
7. Use constants from `sp.config` module

## Testing

Test scenarios to cover:
- Clean installation (no existing `~/SignalPilotHome/`)
- Existing installation (idempotent behavior)
- User vs team workspace selection (via `--team` flag)
- Error cases (no uv, wrong Python version, permission issues)
- Docker testing for clean environment

## Future Work (v1.1+)
- R language support (see SPEC-R-SUPPORT.md)
- Multiple environment management
- MCP server configuration
