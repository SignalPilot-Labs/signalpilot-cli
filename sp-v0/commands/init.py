"""sp init - Initialize SignalPilot workspace."""

from pathlib import Path
from typing import Annotated

import typer

from sp import config
from sp.core import environment
from sp.ui import banner, error, info, next_steps, success


def init_local() -> None:
    """Initialize project-level SignalPilot workspace in current directory."""
    project_root = Path.cwd()
    local_signalpilot = project_root / ".signalpilot"
    local_venv = project_root / ".venv"
    local_skills = project_root / "skills"
    local_rules = project_root / "rules"

    info(f"Creating project workspace in {project_root}")

    # Check if already initialized
    if local_signalpilot.exists() and local_venv.exists():
        info("Project already initialized")
        info(f"Config: {local_signalpilot}")
        info(f"Environment: {local_venv}")
        print()
        next_steps([
            ("sp lab", "Launch Jupyter Lab in this project"),
        ])
        return

    # Ensure global SignalPilot is initialized (for Python)
    if not config.is_initialized():
        error("Global SignalPilot not initialized")
        info("Run: sp init")
        info("Then retry: sp init --local")
        raise typer.Exit(1)

    # Create directories
    local_signalpilot.mkdir(exist_ok=True)
    local_skills.mkdir(exist_ok=True)
    local_rules.mkdir(exist_ok=True)

    success("Directory structure created")

    # Create local venv using Python from global SignalPilotHome
    # This reuses the Python already installed in ~/SignalPilotHome/.venv
    if not environment.create_venv(local_venv, config.DEFAULT_PYTHON_VERSION):
        raise typer.Exit(1)

    # Install core packages in local venv
    if not environment.install_packages(config.CORE_PACKAGES, local_venv):
        raise typer.Exit(1)

    # Create skill registry
    skill_registry = local_skills / "skill-upload-registry.json"
    if not skill_registry.exists():
        skill_registry.write_text("{}\n")

    # Create pyproject.toml
    pyproject = project_root / "pyproject.toml"
    if not pyproject.exists():
        pyproject.write_text("""[project]
name = "signalpilot-project"
version = "0.1.0"
description = "SignalPilot project"
requires-python = ">=3.12"
dependencies = [
    "jupyterlab",
    "ipykernel",
    "pandas",
    "numpy",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
""")

    success("Configuration files created")

    print()
    success("Project initialized!")
    print()
    info(f"Workspace: {project_root}")
    info(f"Config: {local_signalpilot}")
    info(f"Environment: {local_venv}")
    print()

    next_steps([
        ("sp lab", "Launch Jupyter Lab in this project"),
    ])


def init(
    local: Annotated[
        bool,
        typer.Option("--local", help="Initialize project-level workspace in current directory"),
    ] = False,
) -> None:
    """Initialize SignalPilot workspace.

    Default: Creates global workspace at ~/SignalPilotHome/
    --local: Creates project workspace in current directory (.signalpilot/, .venv, skills/, rules/)

    Both modes create directory structure, install Python, and set up packages.
    This is idempotent - safe to run multiple times.
    """
    if local:
        init_local()
        return

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