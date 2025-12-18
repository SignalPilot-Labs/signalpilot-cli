"""sp lab - Launch JupyterLab."""

from pathlib import Path
from typing import Annotated

import typer

from sp import config
from sp.core import jupyter
from sp.ui import console, error, info, muted


def lab(
    port: Annotated[
        int,
        typer.Option("--port", "-p", help="Port number"),
    ] = 8888,
    dir: Annotated[
        Path | None,
        typer.Option("--dir", "-d", help="Notebook directory"),
    ] = None,
    no_browser: Annotated[
        bool,
        typer.Option("--no-browser", help="Don't open browser automatically"),
    ] = False,
) -> None:
    """Launch JupyterLab with the SignalPilot environment."""
    # Check if initialized
    if not config.is_initialized():
        error("SignalPilot is not initialized.")
        info("Run 'sp init' first to set up your workspace.")
        raise typer.Exit(1)

    # Default to SignalPilot notebooks directory
    notebook_dir = dir if dir else config.NOTEBOOKS_DIR

    # Check if port is already in use
    if jupyter.check_jupyter_running(port):
        error(f"Port {port} is already in use.")
        info(f"Try a different port: sp lab --port {port + 1}")
        raise typer.Exit(1)

    # Display connection info
    print()
    console.print(f"  [bold]●[/] Environment: default")
    console.print(f"  [bold]●[/] Notebooks:   {notebook_dir}")
    console.print(f"  [bold]●[/] URL:         http://localhost:{port}")
    print()
    info("Starting JupyterLab... (Ctrl+C to stop)")
    print()

    # Launch JupyterLab (blocks until user exits)
    exit_code = jupyter.launch_jupyterlab(
        port=port,
        notebook_dir=notebook_dir,
        no_browser=no_browser,
    )

    raise typer.Exit(exit_code)
