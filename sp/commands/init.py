"""sp init - Initialize SignalPilot workspace."""

from typing import Annotated

import typer

from sp import config
from sp.core import environment, jupyter
from sp.ui import banner, error, info, muted, next_steps, spinner, success


def init(
    python: Annotated[
        str,
        typer.Option("--python", "-p", help="Python version to use"),
    ] = config.DEFAULT_PYTHON_VERSION,
    minimal: Annotated[
        bool,
        typer.Option("--minimal", help="Install only core packages (skip data science extras)"),
    ] = False,
    skip_warmup: Annotated[
        bool,
        typer.Option("--skip-warmup", help="Skip Jupyter cache warmup"),
    ] = False,
) -> None:
    """Initialize SignalPilot workspace and default environment."""
    # Display banner
    banner()

    # Check/install uv
    if not environment.ensure_uv():
        raise typer.Exit(1)

    # Create directory structure
    info(f"Creating SignalPilot home at {config.SIGNALPILOT_HOME}")
    for directory in config.ALL_DIRS:
        directory.mkdir(parents=True, exist_ok=True)
    success("Directory structure ready")

    # Install Python
    if not environment.install_python(python):
        raise typer.Exit(1)

    # Create venv
    if not environment.create_venv(config.DEFAULT_VENV_DIR, python):
        raise typer.Exit(1)

    # Determine packages to install
    packages = config.CORE_PACKAGES.copy()
    if not minimal:
        packages.extend(config.DATASCIENCE_PACKAGES)
    packages.extend(config.SIGNALPILOT_PACKAGES)

    # Install packages
    if not environment.install_packages(packages):
        raise typer.Exit(1)

    # Register Jupyter kernel
    with spinner("Registering Jupyter kernel..."):
        display_name = f"SignalPilot (Python {python})"
        jupyter.create_kernel_spec(
            name=config.DEFAULT_KERNEL_NAME,
            display_name=display_name,
        )
    success(f"Registered kernel: {config.DEFAULT_KERNEL_NAME}")

    # Disable announcements
    with spinner("Optimizing JupyterLab..."):
        jupyter.disable_announcements()
    success("JupyterLab optimized")

    # Warmup (unless skipped)
    if not skip_warmup:
        with spinner("Warming up Jupyter (first launch will be faster)..."):
            jupyter.warmup_jupyter()
        success("Warmup complete")

    # Success message
    success("Installation complete!")
    print()
    muted(f"  Your workspace is at: {config.SIGNALPILOT_HOME}")
    print()

    # Next steps
    next_steps([
        ("sp lab", "Launch JupyterLab"),
        ("sp status", "Check installation"),
    ])
