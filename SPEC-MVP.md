# SignalPilot CLI - MVP Specification

## Overview

Build a minimal, beautiful CLI tool called `sp` that initializes a SignalPilot workspace and launches JupyterLab. The tool should be installable via a single `curl | sh` command and rival the UX quality of tools like `uv`, `mise`, and `claude`.

## User Journey

```
curl -sSf https://get.signalpilot.dev | sh   # Install CLI
sp init                                       # Set up workspace
sp lab                                        # Launch JupyterLab
```

## Directory Structure to Create

```
signalpilot-cli/
├── install.sh              # Shell installer (curl | sh)
├── pyproject.toml          # Package definition
├── README.md
└── sp/
    ├── __init__.py
    ├── main.py             # Typer CLI entry point
    ├── config.py           # Paths and constants
    ├── commands/
    │   ├── __init__.py
    │   ├── init.py         # sp init
    │   └── lab.py          # sp lab
    ├── core/
    │   ├── __init__.py
    │   ├── environment.py  # uv/venv management
    │   └── jupyter.py      # Kernel registration, launch
    └── ui/
        ├── __init__.py
        └── console.py      # Rich console, branded output
```

## SignalPilot Home Structure

When `sp init` runs, create this structure at `~/SignalPilotHome`:

```
~/SignalPilotHome/
├── notebooks/              # User notebooks
├── skills/                 # SignalPilot skills
├── connections/            # Connection configs
├── config/                 # Jupyter config, app config
└── system/
    ├── signal_pilot/       # Default Python venv
    ├── jupyter/
    │   ├── runtime/
    │   └── kernels/
    ├── logs/
    └── cache/
```

---

## Component Specifications

### 1. `install.sh`

**Purpose**: Zero-dependency installer that bootstraps uv and the CLI.

**Requirements**:
- Must work on macOS, Linux, and WSL with only `curl` and `sh`
- Install `uv` if not present (via official installer)
- Create isolated venv at `~/.signalpilot/venv`
- Install `signalpilot-cli` package into that venv
- Create wrapper script at `~/.signalpilot/bin/sp`
- Add `~/.signalpilot/bin` to PATH in `.bashrc` and `.zshrc`
- Print success message with next steps

**Output on success**:
```
✓ SignalPilot installed!

  Restart your terminal, or run:
    export PATH="${HOME}/.signalpilot/bin:${PATH}"

  Then run:
    sp init
```

---

### 2. `sp init`

**Purpose**: Initialize SignalPilot workspace and default environment.

**Options**:
```
--python, -p     Python version (default: 3.12)
--minimal        Install only core packages (skip data science extras)
--skip-warmup    Skip Jupyter cache warmup
```

**Steps**:
1. Display branded banner
2. Check/install uv if not present
3. Create directory structure at `~/SignalPilotHome`
4. Install Python via `uv python install 3.12`
5. Create venv at `~/SignalPilotHome/system/signal_pilot`
6. Install packages via uv:
   - Core: `jupyterlab`, `ipykernel`, `pandas`, `numpy`
   - Data science (unless --minimal): `matplotlib`, `seaborn`, `scikit-learn`
   - SignalPilot: `signalpilot-ai`
7. Register Jupyter kernel named "signalpilot"
8. Disable JupyterLab announcements extension
9. (Unless --skip-warmup) Start Jupyter briefly to warm caches
10. Print success with next steps

**Kernel registration**:
Create kernel spec at `~/SignalPilotHome/system/jupyter/kernels/signalpilot/kernel.json`:
```json
{
  "argv": [
    "~/SignalPilotHome/system/signal_pilot/bin/python",
    "-Xfrozen_modules=off",
    "-m", "ipykernel_launcher",
    "-f", "{connection_file}"
  ],
  "display_name": "SignalPilot (Python 3.12)",
  "language": "python",
  "metadata": { "debugger": true }
}
```

**Environment variables for Jupyter**:
```
JUPYTER_CONFIG_DIR=~/SignalPilotHome/config
JUPYTER_DATA_DIR=~/SignalPilotHome/system/jupyter
JUPYTER_RUNTIME_DIR=~/SignalPilotHome/system/jupyter/runtime
```

**Output on success**:
```
╭─────────────────────────────────────────────────────────────╮
│                                                             │
│   SignalPilot                                               │
│   Your Trusted CoPilot for Data Analysis                    │
│                                                             │
╰─────────────────────────────────────────────────────────────╯

→ Creating SignalPilot home at ~/SignalPilotHome
✓ Directory structure ready
✓ Python 3.12 ready
✓ Environment created with 12 packages
✓ Registered kernel: signalpilot
✓ JupyterLab optimized
✓ Installation complete!

  Your workspace is at: ~/SignalPilotHome

╭─ Next steps ────────────────────────────────────────────────╮
│   sp lab              Launch JupyterLab                     │
│   sp status           Check installation                    │
╰─────────────────────────────────────────────────────────────╯
```

---

### 3. `sp lab`

**Purpose**: Launch JupyterLab with the SignalPilot environment.

**Options**:
```
--port, -p       Port number (default: 8888)
--dir, -d        Notebook directory (default: ~/SignalPilotHome/notebooks)
--no-browser     Don't open browser automatically
MOVE TO v2: --background, -b Run in background
```

**Subcommands**:
```
sp lab           Launch JupyterLab (default)
MOVE TO v2: sp lab stop      Stop background JupyterLab instances
MOVE TO v2: sp lab status    Check if JupyterLab is running
```

**Steps**:
1. Validate environment exists
2. Display connection info (env, notebook dir, URL)
3. Set Jupyter environment variables
4. Launch `jupyter lab` with appropriate flags
5. Handle SIGINT/SIGTERM gracefully

**Output on launch**:
```
  ● Environment: default
  ● Notebooks:   ~/SignalPilotHome/notebooks
  ● URL:         http://localhost:8888

→ Starting JupyterLab... (Ctrl+C to stop)
```

---

### 4. `sp status`

**Purpose**: Show SignalPilot installation status.

**Output**:
```
╭─────────────────────────────────────────────────────────────╮
│   SignalPilot                                               │
│   Your Trusted CoPilot for Data Analysis                    │
╰─────────────────────────────────────────────────────────────╯

  Home          ✓   ~/SignalPilotHome
  Environment   ✓   default (Python 3.12)
  Kernels       ✓   signalpilot
  JupyterLab    ○   Not running
```

---

## Technical Requirements

### Dependencies (pyproject.toml)

```toml
[project]
name = "signalpilot-cli"
version = "0.1.0"
description = "SignalPilot CLI - Your Trusted CoPilot for Data Analysis"
requires-python = ">=3.10"
dependencies = [
    "typer>=0.12.0",
    "rich>=13.0.0",
]

[project.scripts]
sp = "sp.main:app"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
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

1. **Banner**: Displayed on `sp init` and `sp status`
2. **Progress**: Use Rich spinners for long operations
3. **Success/Error**: Prefix with ✓ or ✗ with appropriate color
4. **Info**: Prefix with → in muted color
5. **Next steps**: Panel at end of successful commands

### Error Handling

- If `uv` not found and can't install: clear error message with manual install instructions
- If environment doesn't exist when running `sp lab`: suggest running `sp init`
- If port in use: suggest alternative port

---

## Testing Checklist

- [ ] `install.sh` works on fresh macOS
- [ ] `install.sh` works on fresh Ubuntu
- [ ] `install.sh` works in WSL
- [ ] `sp init` creates correct directory structure
- [ ] `sp init` registers kernel correctly
- [ ] `sp lab` launches JupyterLab
- [ ] `sp lab` respects --port flag
- [ ] `sp lab stop` kills background processes
- [ ] `sp status` shows correct information
- [ ] All commands have --help text

---

## Out of Scope (v1.1+)

- Multiple environment management (`sp env create/switch`)
- MCP server configuration (`sp mcp add`)
- R language support (`sp r install/convert`)
- Shell completions
- Self-update mechanism
