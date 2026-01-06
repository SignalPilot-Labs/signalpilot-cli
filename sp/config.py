"""SignalPilot CLI configuration - Config SPEC architecture.

This module defines all directory paths and constants according to the
SignalPilot Config SPEC, which uses a global workspace at ~/SignalPilotHome/
with separate user and team workspaces.

Note: Windows support is commented out for now. Use WSL on Windows.
"""

import platform
from pathlib import Path

# =============================================================================
# Main Directory
# =============================================================================

SP_HOME = Path.home() / "SignalPilotHome"

# =============================================================================
# Configuration
# =============================================================================

SP_SIGNALPILOT = SP_HOME / ".signalpilot"
SP_CONFIG_DEFAULTS = SP_SIGNALPILOT / "defaults"

# Default config files (shipped with CLI, updated on upgrade)
SP_DEFAULT_CORE_CONFIG = SP_CONFIG_DEFAULTS / "sp-core.toml"
SP_DEFAULT_JUPYTER_CONFIG = SP_CONFIG_DEFAULTS / "jupyter_server_config.py"
SP_DEFAULT_CLI_CONFIG = SP_CONFIG_DEFAULTS / "cli.toml"

# User override config files
SP_USER_CORE_CONFIG = SP_SIGNALPILOT / "user-sp-core.toml"
SP_USER_JUPYTER_CONFIG = SP_SIGNALPILOT / "user-jupyter_server_config.py"
SP_USER_CLI_CONFIG = SP_SIGNALPILOT / "user-cli.toml"

# =============================================================================
# Skills & Rules
# =============================================================================

SP_DEFAULT_SKILLS = SP_HOME / "default-skills"
SP_DEFAULT_RULES = SP_HOME / "default-rules"

# =============================================================================
# Connections (Credentials - NEVER agent-accessible)
# =============================================================================

SP_CONNECT = SP_HOME / "connect"
SP_CONNECT_DB = SP_CONNECT / "db.toml"
SP_CONNECT_MCP = SP_CONNECT / "mcp.json"
SP_CONNECT_ENV = SP_CONNECT / ".env"
SP_CONNECT_FOLDERS = SP_CONNECT / "folders"
SP_CONNECT_FOLDERS_MANIFEST = SP_CONNECT_FOLDERS / "manifest.toml"

# =============================================================================
# System
# =============================================================================

SP_SYSTEM = SP_HOME / "system"
SP_SYSTEM_VERSION = SP_SYSTEM / "version.toml"
SP_LOGS = SP_SYSTEM / "logs"
SP_MIGRATIONS = SP_SYSTEM / "migrations"

# =============================================================================
# Python Environment
# =============================================================================

SP_VENV = SP_HOME / ".venv"
SP_PYPROJECT = SP_HOME / "pyproject.toml"

# =============================================================================
# Workspaces (Agent-Accessible)
# =============================================================================

# User Workspace (personal, not version-controlled by default)
SP_USER_WORKSPACE = SP_HOME / "user-workspace"
SP_USER_WORKSPACE_DEMO = SP_USER_WORKSPACE / "demo-project"
SP_USER_WORKSPACE_SKILLS = SP_USER_WORKSPACE / "skills"
SP_USER_WORKSPACE_RULES = SP_USER_WORKSPACE / "rules"
SP_USER_WORKSPACE_SKILL_REGISTRY = SP_USER_WORKSPACE_SKILLS / "skill-upload-registry.json"

# Team Workspace (collaborative, git-tracked)
SP_TEAM_WORKSPACE = SP_HOME / "team-workspace"
SP_TEAM_WORKSPACE_NOTEBOOKS = SP_TEAM_WORKSPACE / "notebooks"
SP_TEAM_WORKSPACE_SCRIPTS = SP_TEAM_WORKSPACE / "scripts"
SP_TEAM_WORKSPACE_SKILLS = SP_TEAM_WORKSPACE / "skills"
SP_TEAM_WORKSPACE_RULES = SP_TEAM_WORKSPACE / "rules"
SP_TEAM_WORKSPACE_SKILL_REGISTRY = SP_TEAM_WORKSPACE_SKILLS / "skill-upload-registry.json"

# =============================================================================
# Python & Package Configuration
# =============================================================================

DEFAULT_PYTHON_VERSION = "3.12"

# Core packages (always installed)
CORE_PACKAGES = [
    "jupyterlab",
    "ipykernel",
    "pandas",
    "numpy",
]

# =============================================================================
# Agent Containment
# =============================================================================

# Agent-accessible directories (allowlist)
AGENT_ACCESSIBLE_DIRS = [
    SP_USER_WORKSPACE,
    SP_TEAM_WORKSPACE,
]

# Agent-accessible directories (read-only)
AGENT_READONLY_DIRS = [
    SP_DEFAULT_SKILLS,
    SP_DEFAULT_RULES,
]

# Agent-inaccessible directories (blocklist)
AGENT_INACCESSIBLE_DIRS = [
    SP_CONNECT,       # Credentials
    SP_SIGNALPILOT,   # System configuration
    SP_SYSTEM,        # Installation metadata
    SP_VENV,          # Python environment
]

# =============================================================================
# Helper Functions
# =============================================================================


def get_venv_python() -> Path:
    """Get the path to the venv Python executable.

    Returns:
        Path: Path to python executable in the shared .venv
    """
    # if platform.system() == "Windows":
    #     return SP_VENV / "Scripts" / "python.exe"
    return SP_VENV / "bin" / "python"


def get_venv_bin(name: str) -> Path:
    """Get the path to a binary in the venv.

    Args:
        name: Name of the binary (e.g., 'jupyter', 'pip')

    Returns:
        Path: Path to the binary in the shared .venv
    """
    # if platform.system() == "Windows":
    #     return SP_VENV / "Scripts" / name
    return SP_VENV / "bin" / name


def get_jupyter_env() -> dict[str, str]:
    """Get environment variables for Jupyter.

    Sets up Jupyter config path following standard Jupyter convention:
    - JUPYTER_CONFIG_PATH: defaults directory (loaded first)
    - JUPYTER_CONFIG_DIR: main .signalpilot directory (loaded last, user overrides)

    Other Jupyter directories (data, runtime, kernels) use defaults in .venv.

    Returns:
        dict: Environment variables to set when launching Jupyter
    """
    return {
        "JUPYTER_CONFIG_PATH": str(SP_CONFIG_DEFAULTS),
        "JUPYTER_CONFIG_DIR": str(SP_SIGNALPILOT),
    }


def is_initialized() -> bool:
    """Check if SignalPilot has been initialized.

    Returns:
        bool: True if ~/SignalPilotHome exists with required structure
    """
    return (
        SP_HOME.exists()
        and SP_VENV.exists()
        and get_venv_python().exists()
    )
