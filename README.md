# SignalPilot CLI

<p align="center">
  <strong>Your Trusted CoPilot for Data Analysis</strong>
</p>

<p align="center">
  A minimal, beautiful CLI tool that initializes a SignalPilot workspace and launches JupyterLab.
</p>

---

## Table of Contents

- [Overview](#overview)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Command Reference](#command-reference)
  - [sp init](#sp-init)
  - [sp lab](#sp-lab)
  - [sp status](#sp-status)
- [Workspace Structure](#workspace-structure)
- [Common Workflows](#common-workflows)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)
- [Development](#development)
- [License](#license)

---

## Overview

SignalPilot CLI (`sp`) provides a streamlined way to set up and manage your data analysis environment. With just two commands, you can go from zero to a fully configured JupyterLab environment with all the tools you need for data analysis.

**Key Features:**
- One-command installation via `curl | sh`
- Isolated Python environment powered by [uv](https://docs.astral.sh/uv/)
- Pre-configured JupyterLab with optimized settings
- Data science packages ready out of the box
- Beautiful, informative terminal output

---

## System Requirements

| Requirement | Details |
|-------------|---------|
| **OS** | macOS, Linux, or Windows (WSL) |
| **Shell** | bash or zsh |
| **Tools** | `curl` (pre-installed on most systems) |
| **Disk Space** | ~500MB for full installation |

> **Note:** Python is installed automatically via `uv`. You don't need Python pre-installed.

---

## Installation

### Quick Install (Recommended)

```bash
curl -sSf https://get.signalpilot.dev | sh
```

After installation, restart your terminal or run:

```bash
export PATH="${HOME}/.signalpilot/bin:${PATH}"
```

### What the Installer Does

1. Installs [uv](https://docs.astral.sh/uv/) (Python package manager) if not present
2. Creates an isolated environment at `~/.signalpilot/venv`
3. Installs the `signalpilot-cli` package
4. Adds `sp` command to your PATH

### Manual Installation

If you prefer to install manually or the quick install doesn't work:

```bash
# 1. Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Create environment and install
uv tool install signalpilot-cli
```

### Verify Installation

```bash
sp --help
```

You should see the SignalPilot CLI help message.

---

## Quick Start

Get up and running in 30 seconds:

```bash
# Step 1: Initialize your workspace
sp init

# Step 2: Launch JupyterLab
sp lab
```

That's it! JupyterLab will open in your browser at http://localhost:8888.

---

## Command Reference

### `sp init`

Initialize SignalPilot workspace and default environment.

```
Usage: sp init [OPTIONS]

Options:
  -p, --python TEXT    Python version to use [default: 3.12]
  --minimal            Install only core packages (skip data science extras)
  --skip-warmup        Skip Jupyter cache warmup
  --help               Show this message and exit
```

#### Examples

```bash
# Full installation with all packages
sp init

# Minimal installation (faster, smaller)
sp init --minimal

# Use a specific Python version
sp init --python 3.11

# Quick init for testing (skip warmup)
sp init --skip-warmup

# Combine options
sp init --minimal --python 3.11 --skip-warmup
```

#### What Gets Installed

**Core packages** (always installed):
| Package | Description |
|---------|-------------|
| `jupyterlab` | Interactive development environment |
| `ipykernel` | Jupyter kernel for Python |
| `pandas` | Data manipulation and analysis |
| `numpy` | Numerical computing |

**Data science packages** (unless `--minimal`):
| Package | Description |
|---------|-------------|
| `matplotlib` | Plotting and visualization |
| `seaborn` | Statistical data visualization |
| `scikit-learn` | Machine learning library |

**SignalPilot packages**:
| Package | Description |
|---------|-------------|
| `signalpilot-ai` | SignalPilot AI assistant |

#### Output Example

```
╭──────────────────────────────────────────────────────────────╮
│                                                              │
│   SignalPilot                                                │
│   Your Trusted CoPilot for Data Analysis                     │
│                                                              │
╰──────────────────────────────────────────────────────────────╯

→ Creating SignalPilot home at ~/SignalPilotHome
✓ Directory structure ready
✓ Python 3.12 ready
✓ Virtual environment created
✓ Installed 8 packages
✓ Registered kernel: signalpilot
✓ JupyterLab optimized
✓ Installation complete!

  Your workspace is at: ~/SignalPilotHome

╭─ Next steps ─────────────────────────────────────────────────╮
│   sp lab              Launch JupyterLab                      │
│   sp status           Check installation                     │
╰──────────────────────────────────────────────────────────────╯
```

---

### `sp lab`

Launch JupyterLab with the SignalPilot environment.

```
Usage: sp lab [OPTIONS]

Options:
  -p, --port INTEGER   Port number [default: 8888]
  -d, --dir PATH       Notebook directory
  --no-browser         Don't open browser automatically
  --help               Show this message and exit
```

#### Examples

```bash
# Launch with defaults (port 8888, opens browser)
sp lab

# Use a custom port
sp lab --port 9999

# Use a custom notebook directory
sp lab --dir ~/my-projects

# Don't open browser (useful for remote servers)
sp lab --no-browser

# Combine options
sp lab --port 9000 --dir ~/work --no-browser
```

#### Output Example

```
  ● Environment: default
  ● Notebooks:   ~/SignalPilotHome/notebooks
  ● URL:         http://localhost:8888

→ Starting JupyterLab... (Ctrl+C to stop)
```

#### Stopping JupyterLab

Press `Ctrl+C` in the terminal to stop JupyterLab.

---

### `sp status`

Show SignalPilot installation status.

```
Usage: sp status [OPTIONS]

Options:
  --help  Show this message and exit
```

#### Example

```bash
sp status
```

#### Output Example

```
╭──────────────────────────────────────────────────────────────╮
│                                                              │
│   SignalPilot                                                │
│   Your Trusted CoPilot for Data Analysis                     │
│                                                              │
╰──────────────────────────────────────────────────────────────╯
  Home          ✓   ~/SignalPilotHome
  Environment   ✓   default (Python 3.12)
  Kernels       ✓   signalpilot
  JupyterLab    ○   Not running
```

#### Status Icons

| Icon | Meaning |
|------|---------|
| ✓ | Installed/Ready |
| ✗ | Not installed/Error |
| ● | Running |
| ○ | Not running |

---

## Workspace Structure

After running `sp init`, your workspace is created at `~/SignalPilotHome`:

```
~/SignalPilotHome/
├── notebooks/          # Your Jupyter notebooks (default location)
├── skills/             # SignalPilot skills and templates
├── connections/        # Database and API connection configs
├── config/             # Jupyter and application configuration
└── system/
    ├── signal_pilot/   # Python virtual environment
    ├── jupyter/
    │   ├── runtime/    # Jupyter runtime files
    │   └── kernels/    # Registered Jupyter kernels
    ├── logs/           # Application logs
    └── cache/          # Cache files for faster startup
```

### Directory Purposes

| Directory | Purpose |
|-----------|---------|
| `notebooks/` | Store your Jupyter notebooks here. This is the default directory when launching JupyterLab. |
| `skills/` | SignalPilot skills for automated analysis workflows. |
| `connections/` | Store connection configurations for databases, APIs, etc. |
| `config/` | Jupyter configuration files and app settings. |
| `system/` | Internal system files. Generally, don't modify these manually. |

---

## Common Workflows

### Starting Fresh Each Day

```bash
# Check status
sp status

# Launch JupyterLab
sp lab
```

### Working on a Specific Project

```bash
# Launch JupyterLab in your project directory
sp lab --dir ~/projects/my-analysis
```

### Running on a Remote Server

```bash
# Initialize (only needed once)
sp init

# Launch without opening browser
sp lab --no-browser --port 8888

# Then SSH tunnel from your local machine:
# ssh -L 8888:localhost:8888 user@remote-server
```

### Reinstalling/Updating

```bash
# Re-run init to reinstall everything
sp init
```

### Minimal Installation for CI/Testing

```bash
# Fast installation with only essential packages
sp init --minimal --skip-warmup
```

---

## Configuration

### Environment Variables

SignalPilot sets these environment variables when running Jupyter:

| Variable | Value | Purpose |
|----------|-------|---------|
| `JUPYTER_CONFIG_DIR` | `~/SignalPilotHome/config` | Jupyter configuration |
| `JUPYTER_DATA_DIR` | `~/SignalPilotHome/system/jupyter` | Jupyter data files |
| `JUPYTER_RUNTIME_DIR` | `~/SignalPilotHome/system/jupyter/runtime` | Runtime files |

### Jupyter Kernel

SignalPilot registers a kernel named `signalpilot` with display name "SignalPilot (Python 3.12)". This kernel is automatically selected when you create new notebooks.

---

## Troubleshooting

### "command not found: sp"

Your PATH hasn't been updated. Run:

```bash
export PATH="${HOME}/.signalpilot/bin:${PATH}"
```

Then add this line to your `~/.bashrc` or `~/.zshrc` to make it permanent.

### "SignalPilot is not initialized"

Run `sp init` to set up your workspace:

```bash
sp init
```

### Port Already in Use

If port 8888 is busy, use a different port:

```bash
sp lab --port 9999
```

### Slow First Launch

The first time JupyterLab starts, it builds caches. Subsequent launches will be faster. You can also run `sp init` without `--skip-warmup` to pre-warm the cache.

### Installation Fails

1. **Check curl is installed:**
   ```bash
   curl --version
   ```

2. **Try manual installation:**
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   source ~/.local/bin/env  # or restart terminal
   uv tool install signalpilot-cli
   ```

3. **Check disk space:**
   Ensure you have at least 500MB free.

### Can't Connect to JupyterLab

1. Check if it's running:
   ```bash
   sp status
   ```

2. Check the URL in your browser matches the port:
   ```
   http://localhost:8888
   ```

3. Try disabling browser auto-open and accessing manually:
   ```bash
   sp lab --no-browser
   ```

---

## FAQ

### Where is my data stored?

All your notebooks and data are in `~/SignalPilotHome/notebooks/` by default. This directory is never deleted when you reinstall.

### Can I use my existing Python packages?

SignalPilot uses an isolated virtual environment. To add packages:

```bash
# Activate the SignalPilot environment
source ~/SignalPilotHome/system/signal_pilot/bin/activate

# Install packages
pip install your-package

# Deactivate when done
deactivate
```

### Can I use a different Python version?

Yes, specify it during init:

```bash
sp init --python 3.11
```

### How do I uninstall?

```bash
# Remove SignalPilot home (WARNING: deletes all notebooks!)
rm -rf ~/SignalPilotHome

# Remove CLI installation
rm -rf ~/.signalpilot

# Remove PATH entry from ~/.bashrc and ~/.zshrc
```

### Does this work on Windows?

SignalPilot CLI works on Windows through WSL (Windows Subsystem for Linux). Native Windows support is planned for a future release.

### Can I run multiple JupyterLab instances?

Yes, use different ports:

```bash
# Terminal 1
sp lab --port 8888

# Terminal 2
sp lab --port 9999 --dir ~/other-project
```

---

## Development

### Setting Up for Development

```bash
# Clone the repository
git clone <repo-url>
cd sp-cli

# Create venv and install in dev mode
uv venv .venv && uv pip install -e ".[dev]"

# Run CLI
.venv/bin/sp --help

# Run tests
.venv/bin/pytest tests/ -v

# Run single test
.venv/bin/pytest tests/test_cli.py::TestCLI::test_help -v
```

### Project Structure

```
sp-cli/
├── install.sh              # Shell installer (curl | sh)
├── pyproject.toml          # Package definition
├── tests/                  # Test suite
└── sp/
    ├── main.py             # CLI entry point
    ├── config.py           # Paths and constants
    ├── commands/           # CLI commands
    ├── core/               # Core functionality
    └── ui/                 # Terminal UI components
```

---

## License

Apache 2.0

---

<p align="center">
  <sub>Built with ❤️ for data analysts everywhere</sub>
</p>
