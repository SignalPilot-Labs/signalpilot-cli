# SignalPilot CLI

<p align="center">
  <strong>Your Trusted CoPilot for Data Analysis</strong>
</p>

<p align="center">
  A self-bootstrapping CLI that creates a global workspace for Jupyter-powered data analysis with built-in AI agent support.
</p>

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
  - [Global Workspace Design](#global-workspace-design)
  - [Agent Containment](#agent-containment)
  - [System App Data](#system-app-data)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Command Reference](#command-reference)
  - [sp activate](#sp-activate)
  - [sp init](#sp-init)
  - [sp lab](#sp-lab)
  - [sp install](#sp-install)
  - [sp upgrade](#sp-upgrade)
- [Directory Structure](#directory-structure)
- [Workflows](#workflows)
  - [User Workspace vs Team Workspace](#user-workspace-vs-team-workspace)
  - [Working with Skills and Rules](#working-with-skills-and-rules)
  - [Managing Connections](#managing-connections)
- [Docker Testing](#docker-testing)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)
- [Development](#development)
- [License](#license)

---

## Overview

SignalPilot CLI (`sp`) is a modern, self-bootstrapping command-line tool that sets up a comprehensive data analysis environment with:

- **Global Workspace**: Single `~/SignalPilotHome/` directory for all projects
- **User & Team Workspaces**: Separate spaces for personal and collaborative work
- **AI Agent Ready**: Built-in containment for safe agent execution
- **Self-Contained**: Shared Python environment with all dependencies
- **Beautiful UX**: Informative terminal output powered by Rich

**Key Features:**
- Self-bootstrapping installation via `uvx sp-cli activate`
- Isolated Python environment powered by [uv](https://docs.astral.sh/uv/)
- Pre-configured JupyterLab with optimized settings
- Agent containment with allowlist-based filesystem access
- Credential isolation (never agent-accessible)
- OS-appropriate system app data locations

---

## Architecture

### Global Workspace Design

SignalPilot uses a **single global workspace** at `~/SignalPilotHome/` instead of per-project installations. This provides:

- **Shared environment**: One `.venv` with all dependencies
- **Centralized configuration**: Single source of truth for settings
- **Workspace separation**: User workspace for personal work, team workspace for collaboration
- **Security boundaries**: Clear agent containment model

```
~/SignalPilotHome/
├── .signalpilot/               # Configuration files
├── default-skills/             # Built-in agent skills
├── default-rules/              # Built-in agent rules
├── connect/                    # Credentials (NEVER agent-accessible)
├── system/                     # Installation metadata
├── .venv/                      # Shared Python environment
├── pyproject.toml              # Shared dependencies
├── user-workspace/             # ═══ AGENT WORKSPACE (personal) ═══
│   ├── demo-project/
│   ├── skills/
│   └── rules/
└── team-workspace/             # ═══ AGENT WORKSPACE (team) ═══
    ├── notebooks/
    ├── scripts/
    ├── skills/
    └── rules/
```

### Agent Containment

SignalPilot implements **allowlist-based** agent containment for security:

**Agent-Accessible Directories:**
- ✅ `~/SignalPilotHome/user-workspace/` (personal work)
- ✅ `~/SignalPilotHome/team-workspace/` (collaborative work)

**Agent-Inaccessible Directories:**
- ❌ `~/SignalPilotHome/connect/` (credentials, API keys, connection strings)
- ❌ `~/SignalPilotHome/.signalpilot/` (system configuration)
- ❌ `~/SignalPilotHome/system/` (installation metadata)

This ensures agents can work with notebooks, scripts, and data files while keeping credentials and system files secure.

### System App Data

Following OS conventions, cache and chat history are stored in platform-specific locations:

| Platform | Location |
|----------|----------|
| **macOS** | `~/Library/Application Support/SignalPilot/` |
| **Linux** | `~/.local/share/signalpilot/` |
| **Windows** | `%APPDATA%\SignalPilot\` |

**Contents (OUT of SCOPE for this System):**
```
Application Support/SignalPilot/
├── cache/
│   ├── schemas/            # Database schema cache
│   ├── mcp/                # MCP server cache
│   └── embeddings/         # Embeddings cache
└── chat-history/
    ├── threads/            # JSONL format chat threads
    ├── index.json          # Thread index
    └── exports/            # Exported conversations
```

---

## Installation

SignalPilot uses a **self-bootstrapping** installation model for maximum trust and simplicity.

### Step 1: Install uv

First, install [uv](https://docs.astral.sh/uv/) via your system's trusted package manager:

**macOS (Homebrew):**
```bash
brew install uv
```

**Linux (cargo):**
```bash
cargo install uv
```

**Windows (winget):**
```powershell
winget install --id=astral-sh.uv -e
```

**Alternative (shell script):**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Step 2: Self-Bootstrap SignalPilot

Run the activation command via `uvx` (no permanent installation yet):

```bash
uvx sp-cli activate
```

This creates a wrapper script at `~/.local/bin/sp` and adds it to your PATH.

### Step 3: Restart Your Shell

```bash
# Restart your terminal or reload shell config
source ~/.zshrc  # or ~/.bashrc
```

### Verify Installation

```bash
sp --help
```

You should see the SignalPilot CLI help message.

---

## Quick Start

Get up and running in 60 seconds:

```bash
# Step 1: Self-bootstrap (one-time setup)
uvx sp-cli activate

# Step 2: Initialize workspace
sp init

# Step 3: Launch JupyterLab
sp lab
```

JupyterLab opens at `http://localhost:8888` in your user workspace.

---

## Command Reference

### `sp activate`

**Self-bootstrap SignalPilot CLI installation.**

This command should be run via `uvx sp-cli activate` (not as `sp activate`). It:
1. Creates `~/.local/bin/sp` wrapper script
2. Adds `~/.local/bin` to PATH in shell rc files
3. Displays next steps

```bash
uvx sp-cli activate
```

**What it does:**
- ✅ Creates wrapper script that calls `uvx sp-cli`
- ✅ Updates `~/.zshrc` and `~/.bashrc` with PATH
- ✅ No sudo required
- ✅ No curl | sh trust issues

**Example output:**
```
✓ SignalPilot CLI installed!
→ Restart your shell or run: source ~/.zshrc
→ Then run: sp init
```

---

### `sp init`

**Initialize SignalPilot workspace at ~/SignalPilotHome/.**

Creates the complete directory structure, config files, Python environment, and demo notebook.

```
Usage: sp init [OPTIONS]

Options:
  --help  Show this message and exit
```

**What it creates:**
- ✅ Full `~/SignalPilotHome/` directory structure (see [Directory Structure](#directory-structure))
- ✅ Default configuration files
- ✅ Python 3.12 virtual environment
- ✅ Core packages: `jupyterlab`, `ipykernel`, `pandas`, `numpy`
- ✅ System app data directories (OS-specific)
- ✅ Demo notebook in `user-workspace/demo-project/`
- ✅ Skill and rule registries

**Example:**
```bash
sp init
```

**Example output:**
```
╭──────────────────────────────────────────────────────────────╮
│                                                              │
│   SignalPilot                                                │
│   Your Trusted CoPilot for Data Analysis                     │
│                                                              │
╰──────────────────────────────────────────────────────────────╯

→ Creating SignalPilot workspace...
✓ Directory structure ready
✓ Configuration files created
✓ Python 3.12 installed
✓ Virtual environment created
✓ Installed 4 core packages
✓ Demo notebook created
✓ SignalPilot initialized!

  Your workspace is at: ~/SignalPilotHome

╭─ Next steps ─────────────────────────────────────────────────╮
│   sp lab              Launch Jupyter Lab                     │
│   sp lab --help       See all options                        │
╰──────────────────────────────────────────────────────────────╯
```

**Idempotence:**
Running `sp init` multiple times is safe. It will:
- Skip existing directories
- Ensure all required directories exist
- Repair missing configuration files

---

### `sp lab`

**Launch Jupyter Lab from user-workspace or team-workspace.**

```
Usage: sp lab [OPTIONS]

Options:
  --team               Launch in team workspace (default: user workspace)
  --port INTEGER       Port number [default: 8888]
  --no-browser         Don't open browser automatically
  --help               Show this message and exit
```

**Examples:**

```bash
# Launch in user workspace (default)
sp lab

# Launch in team workspace
sp lab --team

# Use custom port
sp lab --port 9999

# Don't open browser (useful for remote servers)
sp lab --no-browser

# Combine options
sp lab --team --port 9999 --no-browser
```

**Example output:**
```
→ Starting Jupyter Lab in ~/SignalPilotHome/user-workspace
→ Using environment: ~/SignalPilotHome/.venv
→ Access at: http://localhost:8888
```

**Stopping JupyterLab:**
Press `Ctrl+C` in the terminal.

---

### `sp install`

**Repair or reinstall SignalPilot.**

Useful for fixing broken installations or starting completely fresh.

```
Usage: sp install [OPTIONS]

Options:
  --force  Remove all data and reinstall from scratch
  --help   Show this message and exit
```

**Examples:**

```bash
# Repair installation (reinstall packages)
sp install

# Nuclear option: remove everything and start fresh
sp install --force
```

**Repair mode** (no `--force`):
- Verifies Python environment exists
- Reinstalls core packages
- Fixes broken dependencies

**Force mode** (`--force`):
- ⚠️ **WARNING**: Deletes `~/SignalPilotHome/` (including all notebooks!)
- Requires confirmation
- Use only when repair mode doesn't work

**Example output (repair):**
```
→ Repairing installation...
✓ Environment verified
✓ Core packages reinstalled
✓ Installation repaired
```

**Example output (force):**
```
⚠ This will remove ALL SignalPilot data and settings!
Continue? [y/N]: y
✓ Removed ~/SignalPilotHome
→ Run 'sp init' to reinitialize
```

---

### `sp upgrade`

**Upgrade SignalPilot CLI to the latest version.**

Checks PyPI for updates and upgrades via `uv`.

```
Usage: sp upgrade [OPTIONS]

Options:
  --help  Show this message and exit
```

**Example:**
```bash
sp upgrade
```

**Example output (update available):**
```
→ Checking for updates...
→ Current: 0.1.0
→ Latest:  0.2.0
Upgrade? [Y/n]: y
→ Upgrading to 0.2.0...
✓ Upgraded to 0.2.0
```

**Example output (already up-to-date):**
```
→ Checking for updates...
✓ Already on latest version: 0.2.0
```

---

## Directory Structure

Complete `~/SignalPilotHome/` structure created by `sp init`:

```
~/SignalPilotHome/
├── .signalpilot/
│   ├── defaults/                       # Shipped defaults (updated on upgrade)
│   │   ├── sp-core.toml                # Core SignalPilot config
│   │   ├── jupyter_server_config.py    # Jupyter server config
│   │   └── cli.toml                    # CLI defaults
│   ├── user-sp-core.toml               # User overrides for core config
│   ├── user-jupyter_server_config.py   # User Jupyter overrides
│   └── user-cli.toml                   # User CLI overrides
├── default-skills/                     # Built-in agent skills
│   └── sql-optimization/
│       └── SKILL.md
├── default-rules/                      # Built-in agent rules
│   ├── analyze.md
│   ├── explain.md
│   └── investigate.md
├── connect/                            # ⚠️ Credentials (NEVER agent-accessible)
│   ├── db.toml                         # Database connections
│   ├── mcp.json                        # MCP server configs
│   ├── .env                            # Environment variables
│   └── folders/
│       └── manifest.toml               # Folder access permissions
├── system/                             # Installation metadata
│   ├── version.toml                    # Installed version info
│   ├── logs/                           # Application logs
│   └── migrations/                     # Version migration scripts
├── .venv/                              # Shared Python environment
├── pyproject.toml                      # Shared dependencies
├── user-workspace/                     # ═══ AGENT WORKSPACE (personal) ═══
│   ├── demo-project/
│   │   ├── demo-quickstart.ipynb       # Demo notebook
│   │   └── optional-pyproject.toml     # Project-specific dependencies
│   ├── skills/
│   │   └── skill-upload-registry.json  # User skill registry
│   └── rules/                          # User-specific rules
└── team-workspace/                     # ═══ AGENT WORKSPACE (team) ═══
    ├── README.md                       # Team workspace docs
    ├── notebooks/                      # Team notebooks
    ├── scripts/                        # Team scripts
    ├── skills/
    │   └── skill-upload-registry.json  # Team skill registry
    └── rules/                          # Team-specific rules
```

### Directory Purposes

| Directory | Purpose | Agent Access |
|-----------|---------|--------------|
| `.signalpilot/` | Configuration files, defaults, and user overrides | ❌ No |
| `default-skills/` | Built-in agent skills (updated on upgrade) | ✅ Read-only |
| `default-rules/` | Built-in agent rules (analyze, explain, etc.) | ✅ Read-only |
| `connect/` | **Credentials, API keys, connection strings** | ❌ **NEVER** |
| `system/` | Version info, logs, migration scripts | ❌ No |
| `.venv/` | Shared Python virtual environment | ❌ No |
| `user-workspace/` | **Personal notebooks, scripts, data** | ✅ **Full access** |
| `team-workspace/` | **Team notebooks, scripts, data (git-tracked)** | ✅ **Full access** |

---

## Workflows

### User Workspace vs Team Workspace

**User Workspace** (`user-workspace/`):
- Personal, experimental work
- Not version-controlled by default
- Private notebooks and scripts
- Your own custom skills and rules

**Team Workspace** (`team-workspace/`):
- Collaborative work
- **Git-tracked** (initialize with `git init` inside `team-workspace/`)
- Shared notebooks and analysis
- Team-wide skills and rules
- Can be cloned from a team repository

**Example workflow:**

```bash
# Personal work (default)
sp lab

# Team collaboration
sp lab --team
cd ~/SignalPilotHome/team-workspace
git init
git remote add origin git@github.com:yourteam/analytics.git
git pull origin main
```

### Working with Skills and Rules

**Skills** are agent capabilities (e.g., "SQL optimization", "data cleaning").

**Rules** are agent instructions (e.g., "always explain analysis steps").

**Resolution order** (highest priority first):
1. `team-workspace/skills/` or `team-workspace/rules/` (team-specific)
2. `user-workspace/skills/` or `user-workspace/rules/` (user-specific)
3. `default-skills/` or `default-rules/` (built-in)

**Example:**
If `user-workspace/rules/analyze.md` exists, it overrides `default-rules/analyze.md`.

### Managing Connections

Store database and API credentials in `~/SignalPilotHome/connect/`:

**Database connections** (`db.toml`):
```toml
[postgresql.production]
host = "db.example.com"
port = 5432
database = "analytics"
user = "analyst"
password = "secret"

[mysql.staging]
host = "staging-db.example.com"
database = "staging"
user = "dev"
```

**Environment variables** (`.env`):
```bash
OPENAI_API_KEY=sk-...
AWS_ACCESS_KEY_ID=AKIA...
```

**Folder access** (`folders/manifest.toml`):
```toml
[folders.data]
path = "/mnt/data/analytics"
readonly = true
```

**Security:** The `connect/` directory is **NEVER accessible** to agents. Credentials are loaded by trusted code only.

---

## Docker Testing

SignalPilot includes a Docker environment for isolated testing.

### Quick Start

```bash
# Build and start container
./docker-test.sh

# Inside container
sp --help
sp init
sp lab --port 9999 --no-browser
```

### Access Jupyter Lab

Port 9999 is forwarded to your host:
```
http://localhost:9999
```

### Docker Files

- **Dockerfile**: Python 3.12 + uv + sp-cli in dev mode
- **docker-compose.yml**: Port forwarding, volume mounts
- **docker-test.sh**: One-command setup script

### Manual Docker Commands

```bash
# Build
docker compose build

# Start
docker compose up -d

# Shell
docker compose exec sp-cli-dev /bin/bash

# Stop
docker compose down

# Clean up
docker compose down -v
```

### What's Mounted

| Host | Container | Purpose |
|------|-----------|---------|
| `.` | `/app/sp-cli` | Live source code editing |
| `sp-home` | `/root/SignalPilotHome` | Persist workspace |
| `workspace` | `/workspace` | Persist test projects |

---

## Troubleshooting

### "command not found: sp"

Your PATH hasn't been updated. Run:

```bash
source ~/.zshrc  # or ~/.bashrc
```

Or manually add to your shell rc:
```bash
export PATH="${HOME}/.local/bin:${PATH}"
```

### "SignalPilot not initialized. Run: sp init"

You need to run `sp init` first:

```bash
sp init
```

### Port Already in Use

Use a different port:

```bash
sp lab --port 9999
```

Or find what's using port 8888:

```bash
lsof -ti:8888  # Get PID
kill -9 <PID>  # Kill it
```

### Installation Fails

1. **Ensure uv is installed:**
   ```bash
   uv --version
   ```
   If not, install via [uv installation guide](https://docs.astral.sh/uv/).

2. **Check disk space:**
   Ensure you have at least 500MB free.

3. **Try repair mode:**
   ```bash
   sp install
   ```

4. **Nuclear option:**
   ```bash
   sp install --force
   sp init
   ```

### Can't Connect to JupyterLab

1. Check if Jupyter is running (look for the terminal where you ran `sp lab`)

2. Verify the URL matches:
   ```
   http://localhost:8888  # default
   http://localhost:9999  # if you used --port 9999
   ```

3. Check for firewall blocking localhost connections

4. Try accessing without browser auto-open:
   ```bash
   sp lab --no-browser
   ```

### Docker Container Issues

**Container won't start:**
```bash
docker compose down
docker compose build --no-cache
docker compose up -d
```

**Can't access port 9999:**
Check if port is already in use:
```bash
lsof -ti:9999
```

**Source code changes not reflected:**
Rebuild the image:
```bash
docker compose down
docker compose build
docker compose up -d
```

---

## FAQ

### Where is my data stored?

- **Notebooks/Scripts**: `~/SignalPilotHome/user-workspace/` or `team-workspace/`
- **Credentials**: `~/SignalPilotHome/connect/`
- **Cache**: `~/Library/Application Support/SignalPilot/cache/` (macOS)
- **Chat History**: `~/Library/Application Support/SignalPilot/chat-history/` (macOS)

### Can I install additional packages?

Yes, activate the shared environment:

```bash
source ~/SignalPilotHome/.venv/bin/activate
pip install your-package
deactivate
```

Or add to `~/SignalPilotHome/pyproject.toml` for persistence.

### How do I uninstall?

```bash
# Remove workspace (⚠️ WARNING: deletes all notebooks!)
rm -rf ~/SignalPilotHome

# Remove system app data
rm -rf ~/Library/Application\ Support/SignalPilot  # macOS
rm -rf ~/.local/share/signalpilot                   # Linux

# Remove wrapper script
rm ~/.local/bin/sp

# Remove PATH entry from ~/.zshrc or ~/.bashrc
```

### Does this work on Windows?

SignalPilot works on Windows through WSL (Windows Subsystem for Linux). Native Windows support is under development.

### Can I use a different Python version?

Currently, SignalPilot uses Python 3.12. Multi-version support is planned for v1.1.

### Can I run multiple JupyterLab instances?

Yes, use different ports:

```bash
# Terminal 1: User workspace
sp lab --port 8888

# Terminal 2: Team workspace
sp lab --team --port 9999
```

### What's the difference between user and team workspace?

- **User workspace**: Personal, not version-controlled, private
- **Team workspace**: Collaborative, git-tracked, shared with team

Both are agent-accessible for AI-powered analysis.

### How does agent containment work?

Agents can **ONLY** access:
- `user-workspace/`
- `team-workspace/`
- `default-skills/` (read-only)
- `default-rules/` (read-only)

Agents **CANNOT** access:
- `connect/` (credentials)
- `.signalpilot/` (system config)
- `system/` (metadata)

This is enforced at the agent runtime level via allowlist-based filesystem access control.

### Can I share my team workspace via Git?

Yes! Team workspace is designed for Git:

```bash
cd ~/SignalPilotHome/team-workspace
git init
git remote add origin git@github.com:yourteam/analytics.git
git add .
git commit -m "Initial commit"
git push -u origin main
```

Team members can clone and collaborate:

```bash
sp init
cd ~/SignalPilotHome/team-workspace
rm -rf *  # Clear demo files
git clone git@github.com:yourteam/analytics.git .
sp lab --team
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

### Running Tests

```bash
# All tests
pytest tests/ -v

# Specific test file
pytest tests/test_init.py -v

# Specific test
pytest tests/test_cli.py::TestCLI::test_help -v

# With coverage
pytest tests/ --cov=sp --cov-report=html
```

### Docker Development Workflow

```bash
# Start Docker environment
./docker-test.sh

# Inside container, test commands
sp init
sp lab --port 9999 --no-browser

# Exit container
exit

# Rebuild after code changes
docker compose down
docker compose build
```

### Code Style

- **CLI Framework**: [Typer](https://typer.tiangolo.com/)
- **Terminal UI**: [Rich](https://rich.readthedocs.io/)
- **Testing**: [pytest](https://pytest.org/)
- **Formatting**: Follow existing Rich console patterns in `sp/ui/console.py`

### Contributing

1. Fork the repository
2. Create a feature branch
3. Write tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

---

## License

Apache 2.0

---

<p align="center">
  <sub>Built with ❤️ for data analysts everywhere</sub>
</p>
