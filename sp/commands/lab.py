"""sp lab - Launch JupyterLab from workspace."""

from typing import Annotated

import typer

from sp import config
from sp.core import jupyter
from sp.ui import error, info


def lab(
    team: Annotated[
        bool,
        typer.Option("--team", help="Launch in team workspace (default: user workspace)"),
    ] = False,
    port: Annotated[
        int,
        typer.Option("--port", help="Port number"),
    ] = 8888,
    no_browser: Annotated[
        bool,
        typer.Option("--no-browser", help="Don't open browser automatically"),
    ] = False,
) -> None:
    """Launch Jupyter Lab from user workspace or team workspace.

    By default, launches from user-workspace (personal work).
    Use --team to launch from team-workspace (collaborative work).
    """
    # Check if initialized
    if not config.is_initialized():
        error("SignalPilot not initialized. Run: uvx sp-cli activate")
        raise typer.Exit(1)

    # Determine workspace
    workspace = config.SP_TEAM_WORKSPACE if team else config.SP_USER_WORKSPACE
    workspace_name = "team-workspace" if team else "user-workspace"

    # Display info
    print()
    info(f"Starting Jupyter Lab in ~/SignalPilotHome/{workspace_name}")
    info(f"Using environment: ~/SignalPilotHome/.venv")
    info(f"Access at: http://localhost:{port}")
    print()

    # Launch JupyterLab (blocks until user exits)
    exit_code = jupyter.launch_jupyterlab(
        workspace=workspace,
        port=port,
        no_browser=no_browser,
    )

    raise typer.Exit(exit_code)
