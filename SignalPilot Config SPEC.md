# RFC: SignalPilot Configuration & Directory Structure

**Status:** Draft v3  
**Author:** Tarik  
**Date:** January 2026  
**Reviewers:** Engineering Team

---

## 1. Overview

This RFC proposes a standardized directory structure and configuration format for SignalPilot. The goal is to establish clear separation between system configs, user workspace, team collaboration, and cached data—while maintaining compatibility with the MCP ecosystem.

### Design Principles

1. **Explicit over implicit** — Clear file purposes, no magic
2. **Local-first** — Works offline, syncs when connected
3. **Git-friendly** — Sensible defaults for what's tracked vs ignored
4. **MCP-compatible** — Native interop with Claude Desktop, Cursor, VS Code
5. **Override inheritance** — Global defaults → type defaults → instance overrides
6. **Agent containment** — LLM agent cannot access credentials by design

---

## 2. Directory Structure

### Main Directory (`~/SignalPilotHome/`)

```
~/SignalPilotHome/
│
├── config/                        # Configuration management
│   ├── defaults/                 # Shipped defaults (updated on upgrade)
│   │   ├── sp-core.toml
│   │   ├── jupyter_server_config.py
│   │   └── cli.toml
│   ├── user-sp-core.toml        # User overrides (visible, editable)
│   ├── user-jupyter_server_config.py
│   └── user-cli.toml
│
├── default-skills/                # Built-in agent skills (updated on upgrade)
│   └── sql-optimization/
│       └── SKILL.md
│
├── default-rules/                 # Built-in agent rules (updated on upgrade)
│   ├── analyze.md
│   ├── explain.md
│   └── investigate.md
│
├── connect/                       # Connection definitions (NEVER agent-accessible)
│   ├── db.toml                    # DB connections + credentials
│   ├── mcp.json                   # MCP server configs
│   ├── .env                       # Secrets
│   └── folders/
│       └── manifest.toml
│
├── system/                        # Installation metadata
│   ├── version.toml
│   ├── logs/
│   └── migrations/
│
├── .venv/                         # Shared Python environment
├── pyproject.toml                 # Shared dependencies
│
├── user-workspace/                # ═══ AGENT WORKSPACE ═══
│   │                              # Personal workspace (default agent CWD)
│   ├── demo-project/
│   │   ├── demo-quickstart.ipynb
│   │   └── optional-pyproject.toml
│   ├── skills/                    # User skills (override team-workspace/defaults)
│   │   └── skill-upload-registry.json
│   └── rules/                     # User rules (override team-workspace/defaults)
│
└── team-workspace/                # Team workspace (git-tracked)
    ├── README.md
    ├── notebooks/
    │   ├── monthly_metrics.ipynb
    │   └── monthly_metrics.chat.md
    ├── scripts/
    ├── skills/                    # Team skills
    │   └── skill-upload-registry.json
    └── rules/                     # Team rules
```

### System Application Data (OS-specific)

**macOS:** `~/Library/Application Support/SignalPilot/`
**Linux:** `~/.local/share/signalpilot/`
**Windows:** `%APPDATA%\SignalPilot\`

```
Application Support/SignalPilot/
│
├── cache/                         # Ephemeral, rebuildable
│   ├── schemas/
│   ├── mcp/
│   └── embeddings/
│
└── chat-history/                  # Conversation threads
    ├── threads/                   # Individual threads (JSONL)
    ├── index.json                 # Quick lookup metadata
    └── exports/                   # Exported for sharing
```

---

## 3. Agent Containment Model

### The Security Concern

When running `sp lab`, the LLM agent has filesystem access. Without containment:
- Agent could read `connect/db.toml` (credentials!)
- Agent could read `connect/.env` (secrets!)
- Agent could modify `config/` (break setup)
- Agent could read system app data (chat history, cache)

### Design Decision: Allowlist-Based Access Control

**Agent CWD is `~/SignalPilotHome/user-workspace/` (or `team-workspace/` in team mode)**

When `sp lab` starts:
1. CWD is set to `user-workspace/` (default) or `team-workspace/` (team mode)
2. Agent filesystem tools use allowlist for accessible paths
3. Blocked paths return permission denied errors

**What agent CAN access:**
```
user-workspace/      ✓ read/write (notebooks, scripts, projects)
team-workspace/      ✓ read/write (when in team mode)
.venv/              ✓ read-only (via Python interpreter)
pyproject.toml       ✓ read-only (dependency info)
```

**What agent CANNOT access:**
```
config/              ✗ blocked (user settings)
connect/             ✗ blocked (credentials!)
default-skills/      ✗ blocked (loaded via API only)
default-rules/       ✗ blocked (loaded via API only)
default-pyproject.toml ✗ blocked (template only)
system/              ✗ blocked (installation metadata)
~/Library/Application Support/SignalPilot/ ✗ blocked (system data)
```

**Skills and rules:** Agent can read these (they're instructions for it), but ONLY via dedicated skill/rule loading API, not raw filesystem access. This prevents tampering with defaults.

### Implementation

```python
# In agent tool registration
ALLOWED_PATHS = [
    SP_HOME / "user-workspace",
    SP_HOME / "team-workspace",
]

BLOCKED_PATHS = [
    SP_HOME / "connect",
    SP_HOME / "config",
    SP_HOME / "default-skills",
    SP_HOME / "default-rules",
    SP_HOME / "system",
    get_app_data_dir(),  # OS-specific system data
]

filesystem_tool = FileSystemTool(
    allowed_roots=ALLOWED_PATHS,
    blocked_paths=BLOCKED_PATHS,
    allow_parent_traversal=False
)
```

---

## 4. File Formats

| Directory | Format | Rationale |
|-----------|--------|-----------|
| `config/` | TOML | Human-editable, multiline, comments |
| `connect/db.toml` | TOML | Multiline SQL, override inheritance |
| `connect/mcp.json` | JSON | MCP ecosystem standard |
| `connect/.env` | dotenv | Standard secrets |
| `{app_data}/chat-history/threads/` | JSONL | Append-only, streaming |
| `{app_data}/cache/` | JSON files | Simple, inspectable |
| `default-rules/` | Markdown | Authoring experience, agent instructions |
| `default-skills/` | Markdown + frontmatter | Docs + metadata |
| `skill-upload-registry.json` | JSON | Track custom/uploaded skills |
| `pyproject.toml` | TOML | Python ecosystem standard |

---

## 5. Python Environment (`pyproject.toml`)

### Design Decision: Single Shared Environment (V1)

**Simple default:** One `.venv` and `pyproject.toml` at `~/SignalPilotHome/` root, shared by all work.

**Rationale:**
- Dependencies rarely differ between personal and team work (90% use case)
- Simpler mental model (one environment to manage)
- Faster setup, less disk space

**Optional project-specific deps:** Projects can have `optional-pyproject.toml` for unique dependencies.

### Main `pyproject.toml` (at root)

```toml
[project]
name = "signalpilot-workspace"
version = "0.1.0"
requires-python = ">=3.12"

dependencies = [
    "pandas>=2.0",
    "numpy>=1.24",
    "sqlalchemy>=2.0",
    "pyarrow>=14.0",
    "duckdb>=0.9",
]

[project.optional-dependencies]
snowflake = ["snowflake-connector-python>=3.0"]
bigquery = ["google-cloud-bigquery>=3.0"]
postgres = ["psycopg[binary]>=3.0"]
viz = ["plotly>=5.0", "altair>=5.0"]

[tool.signalpilot]
default_kernel = "python3"
auto_install_deps = true

[tool.ruff]
line-length = 100
select = ["E", "F", "I"]
```

### Optional Project Dependencies

Projects can specify additional dependencies in `optional-pyproject.toml`:

```toml
# user-workspace/ml-experiments/optional-pyproject.toml
[project]
dependencies = [
    "scikit-learn>=1.3",
    "statsmodels>=0.14",
    "xgboost>=2.0",
]
```

When working in this project, SignalPilot detects `optional-pyproject.toml` and ensures these packages are installed in the shared `.venv`.

### Advanced Mode (V2): Separate Environments

For the 10% who need isolated environments:

```bash
sp init --mode=user    # Creates user-workspace/.venv
sp init --mode=team    # Creates team-workspace/.venv
```

Each workspace gets its own `pyproject.toml` and `.venv`.

### Resolution (V1)

```python
def resolve_dependencies(project_path: Path) -> list[str]:
    # Load main dependencies
    main = load_toml(SP_HOME / "pyproject.toml")
    deps = main["project"]["dependencies"]

    # Add project-specific deps if they exist
    optional = project_path / "optional-pyproject.toml"
    if optional.exists():
        project_deps = load_toml(optional)["project"]["dependencies"]
        deps.extend(project_deps)

    return deps
```

---

## 6. Chat History Design

### Design Decision: Local by Default, Explicit Export

**Chat threads are local** (stored in system app data). Never committed automatically.

**Storage location:** OS-appropriate app data folder
- macOS: `~/Library/Application Support/SignalPilot/chat-history/`
- Linux: `~/.local/share/signalpilot/chat-history/`
- Windows: `%APPDATA%\SignalPilot\chat-history\`

**Sharing is explicit:**
```
/attach-chat monthly_metrics.ipynb
```

Exports to:
```
team-workspace/notebooks/monthly_metrics.chat.md
```

### Storage Format

**Thread (`{app_data}/chat-history/threads/{uuid}.jsonl`):**
```jsonl
{"ts":"2026-01-05T10:00:00Z","role":"user","content":"Why did revenue drop?"}
{"ts":"2026-01-05T10:00:05Z","role":"assistant","content":"Let me investigate..."}
```

**Index (`{app_data}/chat-history/index.json`):**
```json
{
  "threads": [
    {
      "id": "abc-123",
      "title": "Revenue investigation",
      "created": "2026-01-05T10:00:00Z",
      "updated": "2026-01-05T10:45:00Z",
      "workspace": "team-workspace",
      "notebook": "monthly_metrics.ipynb"
    }
  ]
}
```

**Export (`*.chat.md`):**
```markdown
# Chat: Revenue Investigation

**Thread ID:** abc-123
**Attached to:** monthly_metrics.ipynb
**Date:** January 5, 2026

---

## User
Why did revenue drop last week?

## Assistant
Let me investigate...
```

---

## 7. Collaboration & Locking

### V1: Advisory (No Hard Locks)

On file open, track git state locally. On save, warn if file changed since open.

No lock file in git (causes its own merge conflicts).

### V2: Presence Service (Future)

Optional SignalPilot API for real-time awareness:
- "tarik is viewing monthly_metrics.ipynb"
- Soft locks with timeout

---

## 8. Configuration Schema

### 8.1 Core Config

**Default (`config/defaults/sp-core.toml`):**
```toml
[signalpilot]
version = "0.1.0"
home = "~/SignalPilotHome"

[jupyter]
lab_port = 8888
token_auth = true

[agent]
model = "claude-sonnet-4-20250514"
temperature = 0.0
max_tool_calls = 20
confirm_mutations = true
# Agent filesystem access (allowlist-based)
allowed_paths = ["user-local", "team-shared"]

[logging]
level = "info"
file = "./system/logs/signalpilot.log"
```

**User Override (`config/user-sp-core.toml`):**
```toml
# User overrides (optional, merges with defaults)

[jupyter]
lab_port = 8889  # Override: use different port

[agent]
temperature = 0.1  # Override: slightly more creative

[logging]
level = "debug"  # Override: more verbose logging
```

**Resolution:** User config values override defaults, unspecified values use defaults.

### 8.2 Database Connections (`connect/db.toml`)

```toml
#:schema https://signalpilot.dev/schemas/db.json

[defaults]
timeout = 30
max_rows = 10000

[defaults.snowflake]
warehouse = "COMPUTE_WH"
role = "ANALYST"

[[connections]]
name = "prod_snowflake"
type = "snowflake"
account = "xy12345"
database = "ANALYTICS"

[[connections]]
name = "dev_snowflake"
type = "snowflake"
account = "xy12345"
warehouse = "DEV_XS"
timeout = 60
```

### 8.3 MCP Connections (`connect/mcp.json`)

```json
{
  "$schema": "https://signalpilot.dev/schemas/mcp.json",
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

---

## 9. Skills & Rules Resolution

### Override Order

```
default-skills/            # Built-in (lowest priority)
    ↓
team-workspace/skills/     # Team overrides
    ↓
user-workspace/skills/     # Personal overrides (highest)
```

Same for rules.

### Skill Upload Registry

Each skills folder contains `skill-upload-registry.json` to track custom/uploaded skills:

```json
{
  "skills": [
    {
      "name": "custom-etl-validator",
      "anthropic_skill_id": "skill_abc123",
      "version": "1.0.0",
      "uploaded": "2026-01-05T10:00:00Z",
      "author": "tarik",
      "source": "uploaded"
    }
  ]
}
```

**Field descriptions:**
- `name`: Local skill name (filesystem folder name)
- `anthropic_skill_id`: Official Anthropic skill ID (if from marketplace)
- `version`: Skill version
- `uploaded`: Timestamp when added
- `author`: Who uploaded/created it
- `source`: `"uploaded"`, `"marketplace"`, `"custom"`, `"team"`

### Example

**Rules resolution:**
```
default-rules/investigate.md             # Built-in
team-workspace/rules/investigate.md      # Team version (wins if exists)
user-workspace/rules/investigate.md      # Personal version (wins if exists)
```

**Resolution:**
```python
def resolve_rule(name: str, workspace: str = "user-workspace") -> Path:
    candidates = [
        SP_HOME / f"{workspace}/rules/{name}.md",
        SP_HOME / "team-workspace/rules/{name}.md",  # if workspace is user-workspace
        SP_HOME / f"default-rules/{name}.md",
    ]
    for path in candidates:
        if path.exists():
            return path
    raise RuleNotFound(name)

def resolve_skill(name: str, workspace: str = "user-workspace") -> Path:
    candidates = [
        SP_HOME / f"{workspace}/skills/{name}",
        SP_HOME / "team-workspace/skills/{name}",
        SP_HOME / f"default-skills/{name}",
    ]
    for path in candidates:
        if path.exists():
            return path
    raise SkillNotFound(name)
```

---

## 10. Git & Sync Strategy

| Directory | Git | Agent Access | Rationale |
|-----------|-----|--------------|-----------|
| `config/` | ✗ | ✗ | Local machine settings |
| `connect/` | ✗ Never | ✗ | Credentials |
| `{app_data}/chat-history/` | ✗ | ✗ (API only) | Local threads, system data |
| `{app_data}/cache/` | ✗ | ✗ (API only) | Ephemeral, system data |
| `system/` | ✗ | ✗ | Installation state |
| `default-skills/` | ✗ | ✗ (API only) | Ships with SignalPilot |
| `default-rules/` | ✗ | ✗ (API only) | Ships with SignalPilot |
| `pyproject.toml` (root) | ✗ | ✓ read-only | Shared dependencies |
| `.venv/` | ✗ | ✓ read-only | Python interpreter access |
| `user-workspace/` | User choice | ✓ read/write | Personal workspace |
| `team-workspace/` | ✓ Team repo | ✓ read/write | Collaborative workspace |

---

## 11. Open Questions

### 11.1 Multiple Team Workspaces
- One `team-workspace/` or support multiple? (`team-analytics/`, `team-ml/`)
- If multiple, how to switch context?

### 11.2 Workspace Templates
- `sp init --template=dbt` to scaffold with dbt structure?
- Community templates?

### 11.3 Agent Boundary Enforcement ✅ RESOLVED
- **Decision:** Allowlist-based (user-workspace/, team-workspace/)
- Blocked paths enforced at filesystem tool level
- Skills/rules loaded via API only, not raw filesystem

### 11.4 pyproject.toml Management ✅ RESOLVED
- **V1:** Single shared pyproject.toml at root
- **Optional:** Projects can have optional-pyproject.toml
- **V2:** Advanced mode with separate environments per workspace

### 11.5 Chat Retention
- Auto-cleanup after N days?
- Storage limits?
- Migration from local chat-history/ to system app data on upgrade?

---

## 12. Implementation Plan

### Phase 1: Core Structure
- [ ] `sp init` — scaffold `~/SignalPilotHome/` and system app data
- [ ] Agent containment (allowlist-based: user-workspace/, team-workspace/)
- [ ] Config loading with defaults/user override merge
- [ ] System app data directory creation (OS-specific)

### Phase 2: Python Environment
- [ ] Create shared .venv at ~/SignalPilotHome/ root
- [ ] Generate pyproject.toml with core dependencies
- [ ] Detect and install optional-pyproject.toml deps
- [ ] Register Jupyter kernel pointing to shared .venv

### Phase 3: Chat History (System App Data)
- [ ] JSONL thread storage in {app_data}/chat-history/
- [ ] Index management in {app_data}/chat-history/index.json
- [ ] `/attach-chat` export to team-workspace/
- [ ] Cache management in {app_data}/cache/

### Phase 4: Skills & Rules
- [ ] Resolution order (user-workspace > team-workspace > default)
- [ ] Skill loader with skill-upload-registry.json
- [ ] Rule loader (renamed from prompts)
- [ ] Slash command parser

### Phase 5: Collaboration
- [ ] Git SHA tracking in team-workspace/
- [ ] Conflict warnings
- [ ] V2 presence service (optional)

---

## 13. Decision Log

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Workspace location | `user-workspace/` and `team-workspace/` at root | Flatter structure, consistent naming |
| Agent containment | Allowlist-based access control | More flexible than chroot, explicit permissions |
| System data location | OS-specific app data folders | Follows platform conventions, cleaner home dir |
| Config naming | `config/user-*.toml` + `config/defaults/` | Clear user vs shipped defaults |
| Rules naming | `rules/` not `prompts/` | More accurate, prompts are UI concept |
| pyproject.toml | Single shared at root (V1) | Simpler for 90% use case |
| Config format | TOML | Multiline, comments, no indent issues |
| MCP format | JSON | Ecosystem requirement |
| Chat/cache location | System app data, not SignalPilotHome | OS conventions, avoid clutter |
| Chat sharing | Explicit export to team-workspace/ | Avoids merge conflicts |
| Skill tracking | skill-upload-registry.json | Track custom skills, anthropic_skill_id |

---

## 14. Appendix: Init Scaffold

`sp init` creates:

### Main Directory (`~/SignalPilotHome/`)

```
~/SignalPilotHome/
├── config/
│   ├── defaults/
│   │   ├── sp-core.toml
│   │   ├── jupyter_server_config.py
│   │   └── cli.toml
│   ├── user-sp-core.toml
│   ├── user-jupyter_server_config.py
│   └── user-cli.toml
├── default-skills/
│   └── sql-optimization/
│       └── SKILL.md
├── default-rules/
│   ├── analyze.md
│   ├── explain.md
│   └── investigate.md
├── pyproject.toml
├── connect/
│   ├── db.toml
│   ├── mcp.json
│   ├── .env.example
│   └── folders/
│       └── manifest.toml
├── system/
│   ├── version.toml
│   ├── logs/
│   └── migrations/
├── .venv/                       # Created by uv
├── user-workspace/
│   ├── demo-project/
│   │   ├── demo-quickstart.ipynb
│   │   └── optional-pyproject.toml
│   ├── skills/
│   │   └── skill-upload-registry.json
│   └── rules/
└── team-workspace/
    ├── README.md
    ├── notebooks/
    ├── scripts/
    ├── skills/
    │   └── skill-upload-registry.json
    └── rules/
```

### System App Data (OS-specific)

**macOS:** `~/Library/Application Support/SignalPilot/`

```
Application Support/SignalPilot/
├── cache/
│   ├── schemas/
│   ├── mcp/
│   └── embeddings/
└── chat-history/
    ├── threads/
    ├── index.json
    └── exports/
```

---

**Feedback requested on:**
1. Agent boundary enforcement approach
2. Multiple shared workspaces (Section 11.1)
3. pyproject.toml inheritance mechanism
4. Anything missing?