# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SignalPilot CLI (`sp`) is a minimal, self-bootstrapping CLI tool that sets up project workspaces and launches JupyterLab. The tool rivals the UX quality of tools like `uv`, `mise`, and `rustup` with a "install on first run" pattern.

**User journey:**
```bash
# 1. Install uv (via trusted package manager)
brew install uv

# 2. Self-bootstrap SignalPilot (one-time)
uvx sp-cli activate

# 3. Initialize a project
cd ~/my-project
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
.venv/bin/sp init              # Test project initialization
.venv/bin/sp lab --no-browser  # Test Jupyter Lab launch
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
├── pyproject.toml          # Package definition
├── tests/                  # Test suite
│   └── test_cli.py
└── sp/
    ├── __init__.py
    ├── main.py             # Typer CLI entry point
    ├── config.py           # Paths and constants
    ├── commands/
    │   ├── activate.py     # sp activate - self-bootstrap
    │   ├── init.py         # sp init - project setup
    │   ├── lab.py          # sp lab - launch Jupyter
    │   ├── install.py      # sp install - repair/reinstall
    │   └── upgrade.py      # sp upgrade - update CLI
    ├── core/
    │   ├── environment.py  # uv/venv management
    │   ├── jupyter.py      # Kernel registration, launch
    │   └── project.py      # Project detection logic
    └── ui/
        └── console.py      # Rich console, branded output
```

### Global Installation Structure
Created at `~/SignalPilotHome/` by `sp activate`:
```
~/SignalPilotHome/
├── bin/
│   └── sp                  # CLI wrapper script (added to PATH)
├── .venv/                  # CLI's Python environment
├── .signalpilot/
│   └── config.toml         # Global configuration
└── cache/                  # CLI cache and metadata
```

### Project Structure
Created by `sp init` in any directory:
```
my-project/
├── .venv/                  # Project Python environment
├── .signalpilot/
│   └── config.toml         # Project configuration (blank template)
├── custom-skills/          # Project-specific skills
│   └── .keep
├── custom-rules/           # Project-specific rules
│   └── .keep
├── notebooks/              # User notebooks (optional)
├── data/                   # User data (optional)
└── .gitignore              # Updated with .venv, .env rules
```

## Key Technical Details

### Dependencies
- `typer>=0.12.0` - CLI framework
- `rich>=13.0.0` - Beautiful terminal output
- `pytest>=8.0.0` - Testing (dev dependency)

## Key Architecture Decisions

### Self-Bootstrapping Installation
- Primary installation: `uvx sp-cli activate` (no curl|sh needed)
- Users install `uv` via trusted package managers (brew, winget, cargo)
- `sp activate` installs itself to `~/SignalPilotHome/` and adds to PATH
- More trustworthy than `curl | sh` patterns

### Project-Level Isolation
- Each project gets its own `.venv` and configuration
- No shared global workspace - projects are independent and portable
- Smart detection: `sp lab` finds `.signalpilot/` in current or parent directories
- Benefits: reproducibility, no dependency conflicts, easy to version control

### Five Core Commands
1. **`sp activate`** - Self-bootstrap system installation (run via `uvx`)
2. **`sp init`** - Initialize current directory as project
3. **`sp lab`** - Launch Jupyter Lab with smart project detection
4. **`sp install`** - Repair/reinstall system (with `--force` flag)
5. **`sp upgrade`** - Upgrade CLI to latest version

### Configuration Pattern
- Global config: `~/SignalPilotHome/.signalpilot/config.toml`
- Project config: `./.signalpilot/config.toml`
- Both use same `.signalpilot/` folder pattern for consistency

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
- Always print working directory when launching `sp lab`
- Display branded panels for major operations (`sp activate`, `sp init`)

## Command Implementation Details

### `sp activate` (Self-Bootstrap)
- Detects if running via `uvx` (temp environment)
- Creates `~/SignalPilotHome/` structure
- Installs `sp` to `~/SignalPilotHome/bin/sp`
- Adds to PATH in shell rc files (.bashrc, .zshrc, .profile)
- Uses `uv` for Python environment management

### `sp init` (Project Setup)
- Idempotent - safe to run multiple times
- Creates `.venv/` if doesn't exist (Python 3.12+)
- Creates `.signalpilot/config.toml` (blank template)
- Creates `custom-skills/` and `custom-rules/` with `.keep` files
- Updates `.gitignore` with appropriate rules

### `sp lab` (Smart Launcher)
- Walks up directory tree to find `.signalpilot/`
- Prints working directory and Python environment being used
- Supports `--port` flag for custom port (default: 8888)
- Supports `--no-browser` flag
- Falls back to current directory if no `.signalpilot/` found

### `sp install` (Repair)
- Verifies `~/SignalPilotHome/` installation
- Reinstalls CLI dependencies
- With `--force`: prompts for confirmation, then full reset

### `sp upgrade` (Update)
- Fetches latest version from PyPI
- Shows changelog
- Prompts for confirmation
- Installs via `uv`

## Development Workflow

When implementing commands:
1. Use Typer for CLI framework (type-hint based)
2. Use Rich for all terminal output (spinners, colors, formatting)
3. Follow UI patterns (✓ for success, ✗ for errors, → for info)
4. Always provide helpful error messages with next steps
5. Make operations idempotent where possible
6. Print clear output about what's happening

## Testing

Test scenarios to cover:
- Clean installation (no existing `~/SignalPilotHome/`)
- Existing installation (idempotent behavior)
- Project detection (with and without `.signalpilot/`)
- Multiple projects in different directories
- Error cases (no uv, wrong Python version, permission issues)

## Future Work (v1.1+)
- `sp doctor` - Health check and troubleshooting command
- Chat history integration (V1.5: auto-attach to notebooks)
- VS Code extension integration for skills/rules management
- R language support (see SPEC-R-SUPPORT.md if it exists)
