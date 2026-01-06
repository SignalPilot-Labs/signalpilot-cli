# SignalPilot Home Directory

This directory is the template for `~/SignalPilotHome/` created by `sp init`.

## Directory Structure

```
SignalPilotHome/
├── .signalpilot/              # Configuration management
│   ├── defaults/              # Shipped defaults (updated on upgrade)
│   │   ├── sp-core.toml
│   │   ├── jupyter_server_config.py
│   │   └── cli.toml
│   ├── user-sp-core.toml     # User overrides
│   ├── user-jupyter_server_config.py
│   └── user-cli.toml
│
├── default-skills/            # Built-in agent skills (updated on upgrade)
│   └── data-visualization/
│       └── SKILL.md
│
├── default-rules/             # Built-in agent rules (updated on upgrade)
│   ├── analyze.md
│   ├── explain.md
│   └── investigate.md
│
├── connect/                   # Connection definitions (NEVER agent-accessible)
│   ├── db.toml               # Database connections + credentials
│   ├── mcp.json              # MCP server configs
│   ├── .env.example          # Environment variables template
│   └── folders/
│       └── manifest.toml     # External folder access
│
├── system/                    # Installation metadata
│   ├── version.toml
│   ├── logs/
│   └── migrations/
│
├── .venv/                     # Shared Python environment (created by sp init)
├── pyproject.toml             # Shared dependencies
│
├── user-workspace/            # ═══ AGENT WORKSPACE (personal) ═══
│   ├── demo-project/
│   │   └── demo-quickstart.ipynb
│   ├── skills/
│   │   └── skill-upload-registry.json
│   └── rules/
│
└── team-workspace/            # ═══ AGENT WORKSPACE (team) ═══
    ├── README.md
    ├── notebooks/
    ├── scripts/
    ├── skills/
    │   └── skill-upload-registry.json
    └── rules/
```

## Key Concepts

### Agent Containment

The LLM agent has **allowlist-based** access:

**Agent CAN access:**
- ✅ `user-workspace/` (full read/write)
- ✅ `team-workspace/` (full read/write)
- ✅ `.venv/` (read-only, via Python interpreter)
- ✅ `pyproject.toml` (read-only)

**Agent CANNOT access:**
- ❌ `connect/` (credentials!)
- ❌ `.signalpilot/` (system configuration)
- ❌ `default-skills/` (loaded via API only)
- ❌ `default-rules/` (loaded via API only)
- ❌ `system/` (installation metadata)

### Skills & Rules Resolution Order

Skills and rules follow an override hierarchy:

```
default-skills/           # Built-in (lowest priority)
    ↓
team-workspace/skills/    # Team overrides
    ↓
user-workspace/skills/    # Personal overrides (highest)
```

Same for rules.

### Configuration Override

Config files follow a similar pattern:

```
.signalpilot/defaults/    # Shipped defaults
    ↓
.signalpilot/user-*.toml  # User overrides
```

User config values override defaults; unspecified values use defaults.

## Usage

This directory serves as the template shipped with the `sp-cli` package. During `sp init`, these files are copied to `~/SignalPilotHome/`.

## Files to Customize

**After running `sp init`, users should customize:**

1. `.signalpilot/user-sp-core.toml` - Override default settings
2. `.signalpilot/user-jupyter_server_config.py` - Jupyter customizations
3. `.signalpilot/user-cli.toml` - CLI behavior
4. `connect/db.toml` - Database connections
5. `connect/mcp.json` - MCP servers
6. `connect/.env` - Environment variables (copy from `.env.example`)
7. `pyproject.toml` - Add project dependencies

**Never edit files in:**
- `.signalpilot/defaults/` (overwritten on upgrades)
- `default-skills/` (overwritten on upgrades)
- `default-rules/` (overwritten on upgrades)

## Security

- `connect/.env` contains secrets - **NEVER commit to git**
- `connect/db.toml` may contain credentials - gitignored by default
- Agent cannot access `connect/` directory by design
- All credentials should use environment variables: `${VAR_NAME}`

## Installation

This template is packaged with `sp-cli` and deployed during:
- `sp activate` (creates global SignalPilot installation)
- `sp init` (creates/updates workspace in current directory)

## Version

Template version: 0.1.0
Last updated: 2026-01-05
