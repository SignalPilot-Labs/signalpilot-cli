"""Jupyter Lab launch utilities.

Simple module for launching Jupyter Lab from SignalPilot workspaces.
"""

import signal
import subprocess
from pathlib import Path

from sp import config
from sp.ui import error


def launch_jupyterlab(
    workspace: Path,
    config_dir: Path | None = None,
    venv_path: Path | None = None,
    extra_args: list[str] | None = None,
) -> int:
    """Launch Jupyter Lab from specified workspace.

    Args:
        workspace: Workspace directory to launch from
        config_dir: Optional custom config directory (for project mode)
        venv_path: Optional custom venv path (for project mode)
        extra_args: Additional arguments to pass to jupyter lab

    Returns:
        int: Exit code from Jupyter process
    """
    if extra_args is None:
        extra_args = []
    # Get jupyter binary (from custom venv or global SignalPilotHome venv)
    if venv_path:
        # Project mode: use local .venv
        jupyter = venv_path / "bin" / "jupyter"
    else:
        # Global mode: use SignalPilotHome .venv
        jupyter = config.get_venv_bin("jupyter")

    if not jupyter.exists():
        error("JupyterLab not found. Run 'sp init' first.")
        return 1

    # Ensure workspace exists
    if not workspace.exists():
        error(f"Workspace not found: {workspace}")
        error("Run 'sp init' to create the workspace.")
        return 1

    # Build command
    cmd = [
        str(jupyter),
        "lab",
        f"--notebook-dir={workspace}",
    ]

    # Add any extra arguments passed by user
    cmd.extend(extra_args)

    # Set Jupyter environment
    import os
    env = os.environ.copy()

    # Always use ~/SignalPilotHome/.signalpilot/ for global installs
    # Follow Jupyter config precedence: JUPYTER_CONFIG_PATH (defaults), then JUPYTER_CONFIG_DIR (user overrides)
    if config_dir:
        # Project mode: use local .signalpilot/
        env["JUPYTER_CONFIG_DIR"] = str(config_dir)
    else:
        # Global mode: use ~/SignalPilotHome/.signalpilot/
        env.update(config.get_jupyter_env())

    # Handle signals gracefully
    def signal_handler(signum: int, frame: object) -> None:
        # Let the subprocess handle the signal
        pass

    original_sigint = signal.signal(signal.SIGINT, signal_handler)
    original_sigterm = signal.signal(signal.SIGTERM, signal_handler)

    try:
        process = subprocess.Popen(cmd, env=env)
        return process.wait()
    finally:
        signal.signal(signal.SIGINT, original_sigint)
        signal.signal(signal.SIGTERM, original_sigterm)
