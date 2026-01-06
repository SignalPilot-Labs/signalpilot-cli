"""sp install - Check status, repair, or reinstall SignalPilot."""

import shutil
from typing import Annotated

import typer

from sp import config
from sp.core import environment
from sp.ui import error, info, next_steps, spinner, success, warning


def get_version() -> str:
    """Get the current SignalPilot version.

    Returns:
        str: Version string or "unknown" if not found
    """
    if config.SP_SYSTEM_VERSION.exists():
        try:
            content = config.SP_SYSTEM_VERSION.read_text()
            # Simple TOML parsing for version line
            for line in content.split("\n"):
                if line.startswith("version"):
                    return line.split("=")[1].strip().strip('"')
        except Exception:
            pass
    return "unknown"


def show_status() -> None:
    """Display installation status and version information."""
    if not config.is_initialized():
        error("SignalPilot is not installed")
        info("Run: sp init")
        raise typer.Exit(1)

    version = get_version()
    success(f"SignalPilot is installed (version: {version})")
    print()
    info(f"Workspace: {config.SP_HOME}")
    info(f"Python environment: {config.SP_VENV}")
    info(f"Python: {config.get_venv_python()}")

    # Check venv health
    if not config.get_venv_python().exists():
        warning("Python environment is broken")
        print()
        next_steps([
            ("sp install --repair", "Repair the installation"),
        ])
    else:
        print()
        next_steps([
            ("sp lab", "Launch Jupyter Lab"),
            ("sp lab --team", "Launch in team workspace"),
        ])


def repair_installation() -> None:
    """Repair broken installation by reinstalling packages."""
    if not config.SP_HOME.exists():
        error("SignalPilot not initialized. Run: sp init")
        raise typer.Exit(1)

    info("Repairing SignalPilot installation...")
    print()

    # Check/install uv
    if not environment.ensure_uv():
        raise typer.Exit(1)

    # Recreate venv if missing
    if not config.SP_VENV.exists():
        with spinner("Recreating Python environment..."):
            if not environment.install_python(config.DEFAULT_PYTHON_VERSION):
                raise typer.Exit(1)
            if not environment.create_venv(config.SP_VENV, config.DEFAULT_PYTHON_VERSION):
                raise typer.Exit(1)
        success("Python environment recreated")

    # Reinstall core packages
    with spinner("Reinstalling core packages..."):
        if not environment.install_packages(config.CORE_PACKAGES, config.SP_VENV):
            error("Failed to reinstall packages")
            raise typer.Exit(1)

    success("Core packages reinstalled")
    print()
    success("Installation repaired!")
    print()
    next_steps([
        ("sp lab", "Launch Jupyter Lab"),
    ])


def force_reinstall() -> None:
    """Remove system directories and prompt to reinitialize."""
    if not config.SP_HOME.exists():
        info("SignalPilot not installed (nothing to remove)")
        info("Run: sp init")
        return

    # Directories to remove (system-only, preserves user data)
    dirs_to_remove = [
        config.SP_SIGNALPILOT,  # Config
        config.SP_VENV,         # Python environment
        config.SP_SYSTEM,       # System metadata
    ]

    # Confirm destructive action
    warning("This will remove system directories:")
    for dir_path in dirs_to_remove:
        if dir_path.exists():
            warning(f"  {dir_path}")
    warning("")
    warning("User notebooks, skills, and rules will be preserved.")
    print()

    confirm = typer.confirm("Continue?", default=False)
    if not confirm:
        info("Cancelled")
        return

    # Remove directories
    removed = []
    for dir_path in dirs_to_remove:
        if dir_path.exists():
            try:
                with spinner(f"Removing {dir_path.name}..."):
                    shutil.rmtree(dir_path)
                removed.append(dir_path.name)
            except Exception as e:
                error(f"Failed to remove {dir_path}: {e}")
                raise typer.Exit(1)

    if removed:
        success(f"Removed: {', '.join(removed)}")
    else:
        info("Nothing to remove")

    print()
    next_steps([
        ("sp init", "Reinitialize SignalPilot"),
    ])


def install(
    repair: Annotated[
        bool,
        typer.Option("--repair", help="Repair broken installation"),
    ] = False,
    force: Annotated[
        bool,
        typer.Option("--force", help="Remove system directories and prompt to reinstall"),
    ] = False,
) -> None:
    """Check installation status, repair, or reinstall.

    Default behavior:
        - Shows installation status and version if installed
        - Prompts to run 'sp init' if not installed

    Repair mode (--repair):
        - Recreates Python environment if missing
        - Reinstalls core packages
        - Fixes broken dependencies

    Force reinstall (--force):
        - Removes system directories (.signalpilot, .venv, system)
        - Preserves user notebooks, skills, and rules
        - Prompts user to run 'sp init' to reinitialize
        - Requires confirmation
    """
    if force:
        force_reinstall()
    elif repair:
        repair_installation()
    else:
        show_status()
