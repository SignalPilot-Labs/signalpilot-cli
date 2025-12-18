"""Jupyter kernel registration and launch utilities."""

import json
import os
import signal
import subprocess
import sys
from pathlib import Path

from sp import config
from sp.ui import error, info, success, spinner


def create_kernel_spec(
    name: str = config.DEFAULT_KERNEL_NAME,
    display_name: str = config.DEFAULT_KERNEL_DISPLAY_NAME,
    python_path: Path | None = None,
) -> bool:
    """Create a Jupyter kernel spec for SignalPilot.

    Args:
        name: Kernel name (used internally by Jupyter).
        display_name: Display name shown in Jupyter UI.
        python_path: Path to Python executable. Defaults to venv Python.

    Returns:
        True if creation succeeded, False otherwise.
    """
    if python_path is None:
        python_path = config.get_venv_python()

    kernel_dir = config.JUPYTER_KERNELS_DIR / name
    kernel_dir.mkdir(parents=True, exist_ok=True)

    kernel_spec = {
        "argv": [
            str(python_path),
            "-Xfrozen_modules=off",
            "-m",
            "ipykernel_launcher",
            "-f",
            "{connection_file}",
        ],
        "display_name": display_name,
        "language": "python",
        "metadata": {"debugger": True},
    }

    kernel_json = kernel_dir / "kernel.json"
    kernel_json.write_text(json.dumps(kernel_spec, indent=2))

    # Copy logo files from default python3 kernel if available
    python3_kernel = config.DEFAULT_VENV_DIR / "share" / "jupyter" / "kernels" / "python3"
    if python3_kernel.exists():
        import shutil

        for logo in python3_kernel.glob("logo-*.png"):
            shutil.copy(logo, kernel_dir)

    return True


def get_registered_kernels() -> list[str]:
    """Get list of registered kernel names.

    Returns:
        List of kernel names.
    """
    if not config.JUPYTER_KERNELS_DIR.exists():
        return []

    kernels = []
    for kernel_dir in config.JUPYTER_KERNELS_DIR.iterdir():
        if kernel_dir.is_dir() and (kernel_dir / "kernel.json").exists():
            kernels.append(kernel_dir.name)
    return kernels


def is_kernel_registered(name: str = config.DEFAULT_KERNEL_NAME) -> bool:
    """Check if a kernel is registered.

    Args:
        name: Kernel name to check.

    Returns:
        True if kernel is registered, False otherwise.
    """
    kernel_json = config.JUPYTER_KERNELS_DIR / name / "kernel.json"
    return kernel_json.exists()


def disable_announcements() -> bool:
    """Disable JupyterLab announcements extension.

    Returns:
        True if successful, False otherwise.
    """
    jupyter = config.get_venv_bin("jupyter")
    if not jupyter.exists():
        return False

    env = os.environ.copy()
    env.update(config.get_jupyter_env())

    # Disable and lock the announcements extension
    for action in ["disable", "lock"]:
        result = subprocess.run(
            [str(jupyter), "labextension", action, "@jupyterlab/apputils-extension:announcements"],
            capture_output=True,
            text=True,
            env=env,
        )
        if result.returncode != 0:
            return False

    return True


def warmup_jupyter(port: int = 19999) -> bool:
    """Warm up Jupyter to initialize caches.

    Starts Jupyter briefly to populate caches for faster subsequent starts.

    Args:
        port: Port to use for warmup (should be unused).

    Returns:
        True if warmup succeeded, False otherwise.
    """
    import time

    jupyter = config.get_venv_bin("jupyter")
    if not jupyter.exists():
        return False

    env = os.environ.copy()
    env.update(config.get_jupyter_env())

    # Start Jupyter in background
    process = subprocess.Popen(
        [
            str(jupyter),
            "lab",
            "--no-browser",
            "--allow-root",
            f"--port={port}",
            f"--notebook-dir={config.NOTEBOOKS_DIR}",
        ],
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    # Wait for Jupyter to be ready (up to 30 seconds)
    import urllib.request

    for _ in range(30):
        try:
            urllib.request.urlopen(f"http://localhost:{port}/api/status", timeout=1)
            break
        except Exception:
            time.sleep(1)

    # Kill Jupyter
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()

    return True


def launch_jupyterlab(
    port: int = 8888,
    notebook_dir: Path | None = None,
    no_browser: bool = False,
) -> int:
    """Launch JupyterLab.

    Args:
        port: Port to run on.
        notebook_dir: Directory for notebooks. Defaults to SignalPilot notebooks dir.
        no_browser: If True, don't open browser automatically.

    Returns:
        Exit code from Jupyter process.
    """
    if notebook_dir is None:
        notebook_dir = config.NOTEBOOKS_DIR

    jupyter = config.get_venv_bin("jupyter")
    if not jupyter.exists():
        error("JupyterLab not found. Run 'sp init' first.")
        return 1

    env = os.environ.copy()
    env.update(config.get_jupyter_env())

    cmd = [
        str(jupyter),
        "lab",
        f"--port={port}",
        f"--notebook-dir={notebook_dir}",
    ]

    if no_browser:
        cmd.append("--no-browser")

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


def check_jupyter_running(port: int = 8888) -> bool:
    """Check if JupyterLab is running on a port.

    Args:
        port: Port to check.

    Returns:
        True if Jupyter is running, False otherwise.
    """
    import urllib.request

    try:
        urllib.request.urlopen(f"http://localhost:{port}/api/status", timeout=2)
        return True
    except Exception:
        return False
