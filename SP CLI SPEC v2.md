---
tags:
  - project
  - signalpilot
  - cli
type: Project
status: In Progress
---

> **Modified**: `=dateformat(this.file.mtime, "DDDD, HH:mm:ss")`
> **Created**: `=dateformat(this.file.ctime, "DDDD, HH:mm")`

## 🎯 Executive Summary

**What Changed**: SignalPilot CLI is NOT a full-featured CLI tool like dbt/dagster. It's a **minimal, self-bootstrapping helper** for workspace setup and Jupyter Lab launching. Configuration happens in the VS Code extension UI, not through CLI commands.

**Core Philosophy**: "mise" level of simplicity - self-installing on first run.

**Key Decisions**:
- CLI name: `sp` (not `signalpilot`)
- 5 core commands: `sp activate`, `sp init`, `sp lab`, `sp install`, `sp upgrade`
- **Installation**: `uvx sp-cli activate` (self-bootstrapping, no curl|sh needed)
- **Project init**: `sp init` creates project-level `.signalpilot/` with venv and configs
- **Smart lab**: `sp lab` detects `.signalpilot/` and prints working directory
- Advanced features (skills, prompts, chat, MCP, DB config) managed via VS Code UI
- Python environment: `.venv` at project level (created by `sp init`)
- Project-level `config.toml` for local configuration
- Fast activation: <30s target
- Config format: TOML (multiline support, comments, ecosystem standard)
- No interactive prompts (use flags or VS Code UI)
- Document uv, don't wrap it

See [[CLAUDE.md]] for complete architecture decisions.

---

## 🎯 Goals

- [ ] Ship minimal CLI (`sp`) with self-bootstrapping installation (<30s)
- [ ] Implement `uvx sp-cli activate` for one-command setup
- [ ] Implement `sp init` for project-level initialization
- [ ] Implement smart `sp lab` with project detection
- [ ] Create installation guide (uvx-first approach, no curl|sh)
- [ ] Document VS Code extension integration (MCP, DB config, skills/prompts via UI)
- [ ] Implement smart upgrade mechanism with version compatibility checking

## 📦 Deliverables (Intermediate Packets)

### CLI Implementation
- [ ] Working `sp` CLI with 5 core commands
- [ ] `sp activate` - Self-bootstrapping system setup (run via `uvx sp-cli activate`)
- [ ] `sp init` - Project-level initialization (creates `.signalpilot/`, `.venv`, folders)
- [ ] `sp lab` - Smart Jupyter Lab launcher with project detection (supports `--port`)
- [ ] `sp install` - Repair/reinstall (with `--force` flag for full reset)
- [ ] `sp upgrade` - Upgrade CLI to latest version

### Package & Environment
- [ ] Project-level `.venv/` (created by `sp init`)
- [ ] uv integration (document usage, don't wrap)
- [ ] Custom Jupyter kernel registration pointing to project .venv
- [ ] Global `~/SignalPilotHome/` for CLI installation and global config

### Documentation
- [ ] Installation guide (uvx-first approach)
- [ ] Quickstart: `uvx sp-cli activate` → `sp init` → `sp lab` in <3 minutes
- [ ] Command reference (activate, init, lab, install, upgrade)
- [ ] uv package management guide (how to add/remove libraries)
- [ ] VS Code extension integration guide
- [ ] Project structure guide (`.signalpilot/`, custom folders)
- [ ] Troubleshooting guide

### Example Content
- [ ] Working example notebook: `sp-workspaces/user-workspace/demo-project/demo-quickstart.ipynb`
- [ ] Demo `optional-pyproject.toml` showing project-specific dependencies (if needed)
- [ ] Sample analysis that runs immediately after init with attached chat
- [ ] Quick reference for common operations
- [ ] Demo showing how to create new project folders in `sp-workspaces/user-workspace/`
- [ ] Documentation explaining simple default (shared .venv) vs advanced mode (separate envs)
- [ ] Example of exported `.chat.md` file showing conversation history

## ✅ Outcomes

- [ ] Users install SignalPilot in <2 minutes (any method)
- [ ] `sp init` completes in <30s
- [ ] Users run first analysis in <5 minutes total
- [ ] Clear upgrade path with version compatibility warnings
- [ ] Zero manual config editing required (all via VS Code UI)
- [ ] V1.5: Chat history auto-attaches to notebooks, viewable in VS Code
- [ ] V2: Users can explicitly attach/export chat for team sharing

---

## 🚀 Installation & Usage Flow

### For End Users

**Step 1: Install uv** (one-time, via trusted method)
```bash
# macOS/Linux
brew install uv

# Windows
winget install astral-sh.uv

# Or see: https://docs.astral.sh/uv/getting-started/installation/
```

**Step 2: Activate SignalPilot** (one-time, self-bootstrapping)
```bash
uvx sp-cli activate

# Output:
✓ Created ~/SignalPilotHome/
✓ Installed Python 3.12
✓ Installed SignalPilot CLI
✓ Added 'sp' command to PATH

Restart your shell or run:
  source ~/.zshrc
```

**Step 3: Initialize your project**
```bash
cd ~/my-analysis
sp init

# Output:
✓ Created .venv/
✓ Created .signalpilot/config.toml
✓ Created custom-skills/
✓ Created custom-rules/

Ready! Run 'sp lab' to start.
```

**Step 4: Launch Jupyter Lab**
```bash
sp lab

# Output:
→ Starting Jupyter Lab in /Users/you/my-analysis
→ Using environment: .venv
[Jupyter Lab opens in browser]
```

**Total time: <3 minutes** ⚡

---

## 🔁 Tasks and Breakdown

### Phase 1: Research & Design (✅ MOSTLY COMPLETE)
- [x] Research CLI patterns from industry tools (dbt, dagster, poetry, uv, etc.)
- [x] Decision: Use Typer framework (type-hint based, built on Click)
- [x] Decision: Single workspace environment at sp-workspaces/ root (simpler, shared)
- [x] Decision: Document uv usage (don't wrap with `sp install`)
- [x] Decision: Configs via VS Code UI (not CLI commands)
- [x] Design upgrade mechanism with version compatibility
- [ ] Complete uv best practices research (lazy imports, dependency tiers)
- [ ] Define example notebook content (what to demonstrate?)
- [x] Finalize `sp init` scaffolding structure (aligned with Config SPEC)

### Phase 2: CLI Core Implementation
- [ ] Set up project with Typer + Rich
- [ ] Implement `sp activate`:
  - [ ] Check if running via uvx (detect temp environment)
  - [ ] Create `~/SignalPilotHome/` directory
  - [ ] Create `~/SignalPilotHome/.venv/` with Python 3.12+
  - [ ] Install sp-cli into the venv
  - [ ] Create wrapper script at `~/SignalPilotHome/bin/sp`
  - [ ] Add `~/SignalPilotHome/bin` to PATH (.bashrc, .zshrc, .profile)
  - [ ] Create `~/SignalPilotHome/.signalpilot/config.toml`
  - [ ] Print next steps (restart shell / source rc file)
- [ ] Implement `sp init`:
  - [ ] Create `.venv/` in current directory if doesn't exist (Python 3.12+)
  - [ ] Create `.signalpilot/` directory
  - [ ] Create `.signalpilot/config.toml` (blank template)
  - [ ] Create `custom-skills/` directory with `.keep` file
  - [ ] Create `custom-rules/` directory with `.keep` file
  - [ ] Update/create `.gitignore` with appropriate rules
  - [ ] Print success message and next steps
  - [ ] Idempotent - safe to run multiple times
- [ ] Implement `sp lab`:
  - [ ] Walk up directory tree to find `.signalpilot/`
  - [ ] Print working directory being used
  - [ ] Print Python environment being used (`.venv` or system)
  - [ ] Support `--port` flag for custom port
  - [ ] Support `--no-browser` flag
  - [ ] Launch Jupyter Lab with project context
  - [ ] Non-blocking update check (24hr cache)
- [ ] Implement `sp install`:
  - [ ] Verify `~/SignalPilotHome/` installation
  - [ ] Reinstall CLI dependencies
  - [ ] Support `--force` flag with confirmation prompt
  - [ ] Full reset: remove `~/SignalPilotHome/` and reinstall
- [ ] Implement `sp upgrade`:
  - [ ] Fetch latest version from PyPI
  - [ ] Show changelog
  - [ ] Prompt for confirmation
  - [ ] Install new version via uv
  - [ ] Verify installation

### Phase 3: Chat History & Notebook Association (V1.5 & V2)
- [ ] V1: Basic chat storage (JSONL format)
  - [ ] Thread storage in `chat-history/threads/{uuid}.jsonl`
  - [ ] Index management in `chat-history/index.json`
  - [ ] Chat persists between sessions
- [ ] V1.5: Auto-attach to notebooks
  - [ ] Detect active notebook in VS Code extension
  - [ ] Auto-link chat thread to notebook in index
  - [ ] VS Code UI: Show chat history panel for active notebook
  - [ ] Export chat to markdown for sharing
  - [ ] Copy `.chat.md` to `sp-workspaces/team-workspace/` on export
- [ ] V2: Manual attach with explicit control
  - [ ] `/attach-chat <name>` command in notebook
  - [ ] Detach/reattach chats to different notebooks
  - [ ] Merge multiple chat threads
  - [ ] Chat history browser in VS Code UI

### Phase 4: Upgrade Mechanism
- [ ] Version checking logic (non-blocking, 24hr cache)
- [ ] Tiered notifications (minor/major/security/too-old)
- [ ] CLI ↔ Extension compatibility matrix
- [ ] Rollback mechanism (`sp rollback` command)
- [ ] Auto-upgrade opt-in (config flag)
- [ ] Update channels (stable/beta/nightly)
- [ ] Breaking change migration assistant

### Phase 5: Installation Methods
- [ ] Package for PyPI (`pip install signalpilot`)
- [ ] Test uvx installation (`uvx signalpilot init`)
- [ ] Create curl install script (`curl -sSL https://signalpilot.dev/install.sh | sh`)
  - [ ] Detect OS (macOS/Linux/Windows)
  - [ ] Install uv if missing
  - [ ] Install signalpilot
  - [ ] Run `sp init`
- [ ] Test all installation methods on clean systems

### Phase 6: Documentation
- [ ] Installation guide:
  - [ ] Prerequisites (Python 3.12+, uv)
  - [ ] Three install methods (uvx/pip/curl)
  - [ ] Platform-specific instructions
  - [ ] Troubleshooting common issues
- [ ] Quickstart tutorial:
  - [ ] Install → Init → Launch Lab (with timing)
  - [ ] Run example notebook
  - [ ] Add your first library (`uv pip install pandas`)
  - [ ] Create your first analysis
- [ ] CLI Reference:
  - [ ] `sp init` - options, output, what it creates
  - [ ] `sp lab` - options, Jupyter Lab integration
  - [ ] `sp doctor` - health check outputs
  - [ ] `sp upgrade` - upgrade flow, rollback
- [ ] uv Package Management Guide:
  - [ ] Where dependencies live: `sp-workspaces/pyproject.toml` (single file, shared)
  - [ ] Adding packages: `cd sp-workspaces && uv pip install <package>`
  - [ ] Removing packages: `uv pip uninstall <package>`
  - [ ] Updating packages: `uv pip install --upgrade <package>`
  - [ ] Syncing pyproject.toml: `uv add <package>` (updates pyproject + installs)
  - [ ] Optional project-level deps: Use `optional-pyproject.toml` in project folders
  - [ ] Advanced: `sp init --mode=user` for separate user-workspace environment
  - [ ] Link to uv docs for advanced usage
- [ ] VS Code Extension Integration:
  - [ ] How CLI and extension work together
  - [ ] Where to configure data sources (Extension UI → `connect/db.toml`)
  - [ ] Where to configure MCP servers (Extension UI → `connect/mcp.json`)
  - [ ] Version compatibility requirements
- [ ] Security Model Guide:
  - [ ] Why agent is chrooted to `sp-workspaces/`
  - [ ] What agent can/cannot access
  - [ ] How to safely add credentials via VS Code UI (never in notebooks!)
  - [ ] Skills/prompts resolution (user-workspace > team-workspace > defaults)
  - [ ] Config resolution (user config > defaults/config)
  - [ ] Why config lives at root (machine-specific, not workspace-specific)
- [ ] Skills & Prompts Guide:
  - [ ] Override hierarchy (user-workspace > team-workspace > defaults)
  - [ ] Creating custom skills (`sp-workspaces/user-workspace/skills/`)
  - [ ] Team skills in shared workspace (`sp-workspaces/team-workspace/skills/`)
  - [ ] Built-in skills/prompts in `defaults/` (DO NOT EDIT)
  - [ ] Slash command usage (`/analyze`, `/investigate`, etc.)
  - [ ] How VS Code UI helps browse/edit skills
- [ ] Chat History Guide:
  - [ ] Where threads are stored (`chat-history/threads/`)
  - [ ] How chat attaches to notebooks (V1.5: auto, V2: manual)
  - [ ] Viewing attached chat history in VS Code UI
  - [ ] How to export for team sharing (→ `sp-workspaces/team-workspace/`)
  - [ ] Index management (`chat-history/index.json`)
  - [ ] Retention policies and cleanup

### Phase 7: Testing & Validation
- [ ] Test `sp init` on clean macOS system
- [ ] Test `sp init` on clean Linux system
- [ ] Test `sp init` on clean Windows system (if supported)
- [ ] Test all installation methods (uvx/pip/curl)
- [ ] Test upgrade path (0.1.0 → 0.1.1 → 0.2.0)
- [ ] Test rollback mechanism
- [ ] Test without uv installed (guide user to install)
- [ ] Test without Python 3.12 (guide user to install)
- [ ] Error handling testing (invalid inputs, network failures, permission issues)
- [ ] Beta testing with 2-3 users

---

## 📚 Research Documents

Created research docs for detailed exploration:

1. **[[Research - CLI Patterns (dbt, great_expectations, etc)]]** ✅ COMPLETE
   - Status: Comprehensive research completed
   - Finding: Must separate project config from credentials
   - Finding: Scaffold working examples (not empty projects)
   - Finding: Provide validate command for health checks
   - Note: Most patterns don't apply (we're minimal helper, not full CLI)

2. **[[Research - uv Best Practices]]** 🟡 IN PROGRESS
   - Status: Structure created, needs detailed research
   - Focus: Installation detection, dependency tiers, lazy imports
   - Relevance: HIGH (critical for `sp init` implementation)

3. **[[Research - CLI Command Hierarchy]]** ⚠️ MOSTLY NOT APPLICABLE
   - Status: Structure created but superseded by minimal scope
   - Note: Most content not relevant (no interactive prompts, no config commands)

4. **[[Research - Init Command Design]]** 🟡 RELEVANT
   - Status: Structure created, needs completion
   - Focus: What `sp init` should create and how
   - Relevance: HIGH (core implementation guide)

---

## ⚡ What We're NOT Building

**Critical scope cuts** (based on architectural decisions):

### **Never Building:**
- ❌ `sp analyze` command (analysis happens in notebook, not CLI)
- ❌ `sp configure` command (config editing happens manually or via VS Code UI)
- ❌ `sp install <package>` wrapper (just document uv/pip directly)
- ❌ Recipe-based init (no templates, one simple setup)
- ❌ Interactive prompts for config
- ❌ Complex command hierarchy (5 commands max)
- ❌ Global workspace management (each project is independent)

### **Not in V1 (Coming Later):**
- ⏳ **V1.5**: Auto-attach chat to notebooks
- ⏳ **V1.5**: Chat history viewer in VS Code UI
- ⏳ **V1.5**: Export chat to markdown for team sharing
- ⏳ **V2**: Manual `/attach-chat` command
- ⏳ **V2**: `sp doctor` command for health checks

See [[CLAUDE.md]] Section "What CLI Does NOT Do" for complete list.

---

## 🎨 CLI Design Principles

**From research findings** (see [[Research - CLI Patterns]]):

1. **Self-Bootstrapping**: Like `mise`, `rustup` - installs itself on first run
2. **Fast by Default**: `sp activate` <30s, `sp lab` startup <1s
3. **Minimal Prompts**: Zero interactive prompts (use flags if needed)
4. **Helpful Errors**: Error + Why + What to do next
5. **Progress Indicators**: Show what's happening during long operations
6. **Smart Defaults**: Works out of box, customize via flags if needed
7. **Scaffolding**: Always create working example, never empty project
8. **Non-blocking**: Background operations (version checks) never block user

---

## 📋 Command Reference

### System-Level Commands (One-Time Setup)

#### `sp activate` (via `uvx sp-cli activate`)
**Purpose**: Self-bootstrapping system installation

```bash
# First-time installation
uvx sp-cli activate

# What it does:
✓ Created ~/SignalPilotHome/
✓ Installed Python 3.12
✓ Installed SignalPilot CLI
✓ Added 'sp' command to PATH (~/.zshrc)

Restart your shell or run:
  source ~/.zshrc
```

**Features**:
- Installs `sp` command globally to `~/SignalPilotHome/bin/sp`
- Creates global config at `~/SignalPilotHome/.signalpilot/config.toml`
- Adds PATH to shell rc files (.bashrc, .zshrc, .profile)
- Uses uv for Python environment management

---

#### `sp install`
**Purpose**: Repair/reinstall system setup

```bash
# Repair installation
sp install
  ✓ Verified Python environment
  ✓ Reinstalled dependencies

# Nuclear option (with confirmation)
sp install --force
  ⚠ This will reset ALL SignalPilot settings
  Continue? [y/N]: y
  ✓ Removed ~/SignalPilotHome/
  ✓ Reinstalled everything
```

---

#### `sp upgrade`
**Purpose**: Upgrade CLI to latest version

```bash
sp upgrade
  ✓ Upgraded sp-cli: 0.1.0 → 0.2.0
  ✓ Updated global configuration
```

---

### Project-Level Commands

#### `sp init`
**Purpose**: Initialize current directory as SignalPilot project

```bash
cd ~/my-analysis-project
sp init

# What it creates:
✓ Created .venv/ (Python virtual environment)
✓ Created .signalpilot/config.toml
✓ Created custom-skills/
✓ Created custom-rules/
✓ Added .gitignore rules

Ready! Run 'sp lab' to start Jupyter Lab.
```

**Features**:
- Creates `.venv` if it doesn't exist (using Python 3.12+)
- Creates `.signalpilot/` folder with blank `config.toml`
- Creates `custom-skills/` and `custom-rules/` folders (with `.keep` files)
- Idempotent - safe to run multiple times

**Directory structure after `sp init`**:
```
my-project/
├── .venv/                    # Python environment
├── .signalpilot/
│   └── config.toml          # Project configuration (blank)
├── custom-skills/
│   └── .keep
├── custom-rules/
│   └── .keep
└── .gitignore               # Updated
```

---

### Workspace Commands

#### `sp lab`
**Purpose**: Launch Jupyter Lab with smart project detection

```bash
# Smart detection (uses .signalpilot if exists)
sp lab
  → Starting Jupyter Lab in /Users/tarik/my-project
  → Using environment: .venv
  [Jupyter Lab opens]

# Custom port
sp lab --port 8889
  → Starting Jupyter Lab in /Users/tarik/my-project
  → Server running at http://localhost:8889
```

**Behavior**:
- **Smart detection**:
  - If `.signalpilot/` exists in current or parent directories → use that project
  - Otherwise → use current directory
- **Always prints** the working directory it's using
- **Uses project `.venv`** if available
- Falls back to system Python if no `.venv`

**Flags**:
- `--port <number>` - Custom port (default: 8888)
- `--no-browser` - Don't open browser automatically

---

## 📁 Directory Structure

### Global Installation (`~/SignalPilotHome/`)

**Created by `uvx sp-cli activate`:**

```
~/SignalPilotHome/
├── bin/
│   └── sp                      # CLI wrapper script
├── .venv/                      # CLI's own Python environment
├── .signalpilot/
│   └── config.toml            # Global CLI configuration
└── cache/                      # CLI cache and metadata
```

**Purpose**: Global CLI installation directory
- Added to PATH automatically
- Contains the `sp` command
- Follows same pattern as project directories (`.signalpilot/` for config)

---

### Project Structure (Created by `sp init`)

**Each project is self-contained:**

```
my-project/                     # Any directory you run 'sp init' in
├── .venv/                      # Project Python environment
├── .signalpilot/
│   └── config.toml            # Project configuration (blank template)
├── custom-skills/             # Project-specific skills
│   └── .keep
├── custom-rules/              # Project-specific rules
│   └── .keep
├── notebooks/                 # Your Jupyter notebooks (optional)
├── data/                      # Your data files (optional)
└── .gitignore                 # Updated with .venv, .signalpilot rules
```

**Example multi-project setup:**

```
~/work/
├── sales-analytics/           # Project 1
│   ├── .venv/
│   ├── .signalpilot/
│   ├── custom-skills/
│   ├── custom-rules/
│   └── revenue.ipynb
│
├── product-metrics/          # Project 2
│   ├── .venv/
│   ├── .signalpilot/
│   ├── custom-skills/
│   ├── custom-rules/
│   └── cohorts.ipynb
│
└── ml-experiments/           # Project 3
    ├── .venv/
    ├── .signalpilot/
    ├── custom-skills/
    ├── custom-rules/
    └── model-training.ipynb
```

**Benefits of project-level structure:**
- ✅ Each project has its own dependencies (`.venv`)
- ✅ Each project has its own configuration
- ✅ Projects are portable (just move the folder)
- ✅ Easy to git-track entire project
- ✅ No shared state between projects
- ✅ Works with any directory structure

---

## 🔧 Technology Stack

**Finalized decisions:**

- **CLI Framework**: Typer (type-hint based, built on Click)
- **UI/Progress**: Rich (spinners, progress bars, colors)
- **Package Manager**: uv (Rust-based, fast Python tooling)
- **Python Version**: 3.12+ required
- **Jupyter Integration**: Custom kernel registration
- **Config Format**: TOML (multiline support, comments, no indent issues)
  - `config/*.toml` for app/CLI settings
  - `connect/db.toml` for database connections
  - `connect/mcp.json` for MCP servers (ecosystem requirement)

**Why Typer over Click?**
- Less boilerplate (type hints do the work)
- Auto-generated help text
- Better IDE support
- Rich integration built-in
- Can drop down to Click if needed
- See decision in conversation history

---

## 🔒 Security Considerations

With the project-based structure, security is simplified:

**Agent Workspace:**
- The LLM agent in `sp lab` operates within the project directory
- Agent has access to project files, notebooks, and data
- Agent uses the project's `.venv` for Python execution

**Credentials Management:**
- Database credentials and API keys should be stored in `.env` files
- Add `.env` to `.gitignore` (done automatically by `sp init`)
- Use environment variables in notebooks: `os.getenv("DB_PASSWORD")`
- **Never hardcode credentials** in notebooks or config files

**Best Practices:**
- ✅ Store secrets in `.env` files (gitignored)
- ✅ Use `.signalpilot/config.toml` for non-sensitive project config
- ✅ Keep `.venv` out of version control
- ✅ Review `.gitignore` after `sp init`
- ❌ Don't commit `.env` files
- ❌ Don't hardcode passwords/tokens

**Skills & Rules:**
- Custom skills live in `custom-skills/` (project-specific)
- Custom rules live in `custom-rules/` (project-specific)
- Both directories are version-controllable (no secrets)

**Config Files:**
- `.signalpilot/config.toml` - Project configuration (safe to commit)
- `~/SignalPilotHome/.signalpilot/config.toml` - Global CLI configuration (machine-specific)

---

## 💬 Chat History & Notebook Association

**The Problem**: Analysis often happens through conversations with the agent. When sharing notebooks, the chat context is lost.

**Our Solution**: Associate chat threads with notebooks for full context sharing.

### **V1.5: Auto-Attach (Simple)**

When working in a notebook, chat is automatically linked:
- Agent knows which notebook is active
- Chat thread stored in `chat-history/threads/{uuid}.jsonl`
- Index tracks: `{"notebook": "user-workspace/sales-analytics/revenue.ipynb", "thread_id": "abc-123"}`
- VS Code UI shows chat history panel for active notebook

**User Experience:**
1. Open `revenue.ipynb`
2. Chat with agent: "Why did revenue drop?"
3. Chat auto-saves to `chat-history/` linked to this notebook
4. Reopen notebook later → Chat history available in UI

### **V2: Manual Attach (Explicit Control)**

For power users who want explicit control:

```python
# In notebook or VS Code command palette
/attach-chat revenue_investigation
```

Creates explicit link + exports to shareable format:
```
sp-workspaces/team-workspace/notebooks/revenue.ipynb
sp-workspaces/team-workspace/notebooks/revenue.chat.md
```

**Export Format** (`.chat.md`):
```markdown
# Chat: Revenue Investigation

**Thread ID:** abc-123
**Notebook:** revenue.ipynb
**Date:** January 5, 2026

---

## User
Why did revenue drop last week?

## Assistant
Let me investigate...
[Code execution results...]
```

### **Benefits**

✅ **Reproducibility**: See the thought process behind analysis
✅ **Collaboration**: Team members understand the "why" not just "what"
✅ **Onboarding**: New team members can read conversation history
✅ **Knowledge capture**: Insights preserved, not lost in chat

### **Implementation Phases**

| Feature | V1 | V1.5 | V2 |
|---------|----|----|-----|
| Chat storage (JSONL) | ✅ | ✅ | ✅ |
| Auto-attach to notebook | ❌ | ✅ | ✅ |
| VS Code UI: View history | ❌ | ✅ | ✅ |
| Manual `/attach-chat` | ❌ | ❌ | ✅ |
| Export to markdown | ❌ | ✅ | ✅ |
| Team sharing integration | ❌ | ✅ | ✅ |

---

## 📊 Success Metrics

**Installation flow:**
- ✅ <3 minutes from `uvx sp-cli activate` to running analysis
- ✅ `sp activate` completes in <30s
- ✅ `sp init` completes in <5s
- ✅ Zero manual config file editing required

**User experience:**
- ✅ Self-bootstrapping works reliably
- ✅ Clear next steps at each stage
- ✅ Smart project detection in `sp lab`
- ✅ Helpful error messages with solutions
- ✅ Projects are portable (move folder = move everything)

**System health:**
- ✅ Works on macOS, Linux (Windows TBD)
- ✅ `uvx` installation method tested
- ✅ Beta users can complete quickstart
- ✅ No support questions about installation
- ✅ PATH setup works across shells (bash/zsh)

---

## 🔗 References

### Internal Docs
- [[CLAUDE.md]] - Architecture decisions and locked-in choices
- [[SignalPilot Development]] - Parent project
- [[What is SignalPilot]] - Product overview

### Research Docs
- [[Research - CLI Patterns (dbt, great_expectations, etc)]]
- [[Research - uv Best Practices]]
- [[Research - CLI Command Hierarchy]]
- [[Research - Init Command Design]]

### External Resources
- [Typer Documentation](https://typer.tiangolo.com/)
- [Rich Documentation](https://rich.readthedocs.io/)
- [uv Documentation](https://docs.astral.sh/uv/)
- [CLI UX Guidelines](https://clig.dev/)

---

## ✅ Completed

- [x] Research CLI patterns from 6 industry tools
- [x] Create research documentation structure
- [x] Decide on Typer framework
- [x] Lock in minimal CLI scope (4 commands)
- [x] Design upgrade mechanism
- [x] Document architecture in CLAUDE.md

---

**Last Updated**: 2026-01-05
**Next Focus**: Complete uv best practices research, implement `sp init` prototype with security boundaries
