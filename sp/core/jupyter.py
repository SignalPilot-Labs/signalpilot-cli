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
    port: int = 8888,
    no_browser: bool = False,
) -> int:
    """Launch Jupyter Lab from specified workspace.

    Args:
        workspace: Workspace directory to launch from (user-workspace or team-workspace)
        port: Port to run on (default: 8888)
        no_browser: If True, don't open browser automatically (default: False)

    Returns:
        int: Exit code from Jupyter process
    """
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
        f"--port={port}",
        f"--notebook-dir={workspace}",
    ]

    if no_browser:
        cmd.append("--no-browser")

    # Set Jupyter environment (only JUPYTER_CONFIG_DIR)
    import os
    env = os.environ.copy()
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
