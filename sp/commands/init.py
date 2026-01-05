"""sp init - Initialize SignalPilot workspace."""

import typer

from sp import config
from sp.core import environment
from sp.ui import banner, error, info, next_steps, success


def init() -> None:
    """Initialize SignalPilot workspace at ~/SignalPilotHome/.

    Creates directory structure, installs Python, and sets up packages.

    This is idempotent - safe to run multiple times.
    """
    banner()

    # Check if already initialized
    if config.is_initialized():
        info("SignalPilot already initialized")
        info(f"Workspace: {config.SP_HOME}")
        print()
        next_steps([
            ("sp lab", "Launch Jupyter Lab is user workspacer"),
            ("sp lab --team", "Launch in team workspace"),
        ])
        return

    # ==========================================================================
    # Step 1: Create Directory Structure
    # ==========================================================================

    info(f"Creating workspace at {config.SP_HOME}")

    directories = [
        # Config
        config.SP_SIGNALPILOT / "defaults",

        # Skills & Rules
        config.SP_DEFAULT_SKILLS,
        config.SP_DEFAULT_RULES,

        # Connections
        config.SP_CONNECT,
        config.SP_CONNECT_FOLDERS,

        # System
        config.SP_LOGS,
        config.SP_MIGRATIONS,

        # Workspaces
        config.SP_USER_WORKSPACE_DEMO,
        config.SP_USER_WORKSPACE_SKILLS,
        config.SP_USER_WORKSPACE_RULES,
        config.SP_TEAM_WORKSPACE_NOTEBOOKS,
        config.SP_TEAM_WORKSPACE_SCRIPTS,
        config.SP_TEAM_WORKSPACE_SKILLS,
        config.SP_TEAM_WORKSPACE_RULES,
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

    success("Directory structure created")

    # ==========================================================================
    # Step 2: Python Environment
    # ==========================================================================

    # Check/install uv
    if not environment.ensure_uv():
        raise typer.Exit(1)

    # Install Python
    if not environment.install_python(config.DEFAULT_PYTHON_VERSION):
        raise typer.Exit(1)

    # Create venv
    if not environment.create_venv(config.SP_VENV, config.DEFAULT_PYTHON_VERSION):
        raise typer.Exit(1)

    # Install core packages
    if not environment.install_packages(config.CORE_PACKAGES, config.SP_VENV):
        raise typer.Exit(1)

    # ==========================================================================
    # Step 3: Create Config Files
    # ==========================================================================

    # Create empty skill registries
    for registry in [
        config.SP_USER_WORKSPACE_SKILL_REGISTRY,
        config.SP_TEAM_WORKSPACE_SKILL_REGISTRY,
    ]:
        if not registry.exists():
            registry.write_text("{}\n")

    success("Configuration files created")

    # ==========================================================================
    # Success!
    # ==========================================================================

    print()
    success("SignalPilot initialized!")
    print()
    info(f"Workspace: {config.SP_HOME}")
    print()

    next_steps([
        ("sp lab", "Launch Jupyter Lab"),
        ("sp lab --team", "Launch in team workspace"),
    ])