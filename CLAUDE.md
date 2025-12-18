# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SignalPilot CLI (`sp`) is a minimal, beautiful CLI tool that initializes a SignalPilot workspace and launches JupyterLab. The tool rivals the UX quality of tools like `uv`, `mise`, and `claude`.

**User journey:**
```
curl -sSf https://get.signalpilot.dev | sh   # Install CLI
sp init                                       # Set up workspace
sp lab                                        # Launch JupyterLab
```

## Development Commands

```bash
# Create venv and install in dev mode
uv venv .venv && uv pip install -e ".[dev]"

# Run CLI
.venv/bin/sp --help
.venv/bin/sp init --skip-warmup  # Skip warmup for faster testing
.venv/bin/sp status
.venv/bin/sp lab --no-browser

# Run tests
.venv/bin/pytest tests/ -v

# Run single test
.venv/bin/pytest tests/test_cli.py::TestCLI::test_help -v
```

## Directory Structure

```
sp-cli/
├── install.sh              # Shell installer (curl | sh)
├── pyproject.toml          # Package definition
├── tests/                  # Test suite
│   └── test_cli.py
└── sp/
    ├── __init__.py
    ├── main.py             # Typer CLI entry point
    ├── config.py           # Paths and constants
    ├── commands/
    │   ├── init.py         # sp init
    │   ├── lab.py          # sp lab
    │   └── status.py       # sp status
    ├── core/
    │   ├── environment.py  # uv/venv management
    │   └── jupyter.py      # Kernel registration, launch
    └── ui/
        └── console.py      # Rich console, branded output
```

## Key Technical Details

### Dependencies
- `typer>=0.12.0` - CLI framework
- `rich>=13.0.0` - Beautiful terminal output
- `pytest>=8.0.0` - Testing (dev dependency)

### SignalPilot Home Structure
Created at `~/SignalPilotHome`:
```
notebooks/              # User notebooks
skills/                 # SignalPilot skills
connections/            # Connection configs
config/                 # Jupyter config, app config
system/
    signal_pilot/       # Default Python venv
    jupyter/
        runtime/
        kernels/
    logs/
    cache/
```

### Environment Variables for Jupyter
```
JUPYTER_CONFIG_DIR=~/SignalPilotHome/config
JUPYTER_DATA_DIR=~/SignalPilotHome/system/jupyter
JUPYTER_RUNTIME_DIR=~/SignalPilotHome/system/jupyter/runtime
```

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
- Display branded panel on `sp init` and `sp status`

## Future Work (v1.1+)
- `sp r status/install/convert` - R language support (see SPEC-R-SUPPORT.md)
- Multiple environment management
- MCP server configuration
