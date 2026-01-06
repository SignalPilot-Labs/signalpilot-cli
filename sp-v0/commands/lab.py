"""sp lab - Launch JupyterLab from workspace."""

from pathlib import Path
from typing import Annotated

import typer

from sp import config
from sp.core import jupyter
from sp.ui import error, info


def lab(
    ctx: typer.Context,
    team: Annotated[
        bool,
        typer.Option("--team", help="Launch in team workspace (default: user workspace)"),
    ] = False,
) -> None:
    """Launch Jupyter Lab from workspace.

    Detects and uses project-level config if present (.signalpilot/, .venv in current directory).
    Otherwise uses global workspace (~/SignalPilotHome/).

    For global mode, use --team to launch from team-workspace instead of user-workspace.

    Pass Jupyter Lab arguments directly, e.g.:
    sp lab --port=9999 --no-browser
    sp lab --team --port=8888 --ServerApp.token='mytoken'
    """
    # Capture all unknown arguments to pass to jupyter
    jupyter_args = ctx.args
    # Check for project-level initialization
    project_root = Path.cwd()
    local_signalpilot = project_root / ".signalpilot"
    local_venv = project_root / ".venv"

    # Project mode: use local .signalpilot and .venv
    if local_signalpilot.exists() and local_venv.exists():
        if team:
            info("--team flag ignored in project mode")

        print()
        info(f"Starting Jupyter Lab in project: {project_root.name}")
        info(f"Config: .signalpilot/")
        info(f"Environment: .venv/")
        print()

        # Launch with project config
        exit_code = jupyter.launch_jupyterlab(
            workspace=project_root,
            config_dir=local_signalpilot,
            venv_path=local_venv,
            extra_args=jupyter_args,
        )
        raise typer.Exit(exit_code)

    # Global mode: use ~/SignalPilotHome/
    if not config.is_initialized():
        error("SignalPilot not initialized")
        info("Run: sp init (global) or sp init --local (project)")
        raise typer.Exit(1)

    # Determine workspace
    workspace = config.SP_TEAM_WORKSPACE if team else config.SP_USER_WORKSPACE
    workspace_name = "team-workspace" if team else "user-workspace"

    # Display info
    print()
    info(f"Starting Jupyter Lab in ~/SignalPilotHome/{workspace_name}")
    info(f"Using environment: ~/SignalPilotHome/.venv")
    print()

    # Launch JupyterLab (blocks until user exits)
    exit_code = jupyter.launch_jupyterlab(
        workspace=workspace,
        extra_args=jupyter_args,
    )

    raise typer.Exit(exit_code)
