"""Environment management using uv.

This module handles Python environment setup using uv:
- Checking and installing uv
- Installing Python versions
- Creating virtual environments
- Installing packages
"""

import os
import shutil
import subprocess
from pathlib import Path

from sp import config
from sp.ui import error, info, success, spinner


def check_uv() -> bool:
    """Check if uv is installed and available.

    Returns:
        bool: True if uv is in PATH, False otherwise
    """
    return shutil.which("uv") is not None


def install_uv() -> bool:
    """Install uv using the official installer.

    Returns:
        bool: True if installation succeeded, False otherwise
    """
    info("Installing uv (Python package manager)...")
    try:
        result = subprocess.run(
            ["sh", "-c", "curl -LsSf https://astral.sh/uv/install.sh | sh"],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            error("Failed to install uv")
            error(result.stderr)
            return False
        success("uv installed")
        return True
    except Exception as e:
        error(f"Failed to install uv: {e}")
        return False


def get_uv_path() -> str:
    """Get the path to uv executable.

    Returns:
        str: Path to uv executable
    """
    # Check common locations
    uv = shutil.which("uv")
    if uv:
        return uv

    # Check ~/.local/bin (common after fresh install)
    local_uv = Path.home() / ".local" / "bin" / "uv"
    if local_uv.exists():
        return str(local_uv)

    # Check ~/.cargo/bin (older install method)
    cargo_uv = Path.home() / ".cargo" / "bin" / "uv"
    if cargo_uv.exists():
        return str(cargo_uv)

    return "uv"  # Hope it's in PATH


def ensure_uv() -> bool:
    """Ensure uv is available, installing if necessary.

    Returns:
        bool: True if uv is available, False otherwise
    """
    if check_uv():
        return True

    info("uv not found, installing...")
    if not install_uv():
        error("Could not install uv automatically.")
        error("Please install uv manually: https://docs.astral.sh/uv/getting-started/installation/")
        return False

    return True


def is_running_in_uvx() -> bool:
    """Detect if we're running in a uvx temporary environment.

    uvx creates temporary environments and sets UV_PROJECT_ENVIRONMENT.
    This is used to detect if 'sp activate' is being run via 'uvx sp-cli activate'.

    Returns:
        bool: True if running in uvx, False otherwise
    """
    # Check for UV_PROJECT_ENVIRONMENT (set by uvx)
    if "UV_PROJECT_ENVIRONMENT" in os.environ:
        return True

    # Fallback: check if we're in a .cache/uv path (uvx temp location)
    try:
        venv_path = Path(os.environ.get("VIRTUAL_ENV", ""))
        if ".cache/uv" in str(venv_path):
            return True
    except Exception:
        pass

    return False


def install_python(version: str = config.DEFAULT_PYTHON_VERSION) -> bool:
    """Install Python using uv.

    Args:
        version: Python version to install (default: from config)

    Returns:
        bool: True if installation succeeded, False otherwise
    """
    uv = get_uv_path()
    with spinner(f"Installing Python {version}..."):
        result = subprocess.run(
            [uv, "python", "install", version],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            error(f"Failed to install Python {version}")
            error(result.stderr)
            return False
    success(f"Python {version} ready")
    return True


def create_venv(
    path: Path = config.SP_VENV,
    python_version: str = config.DEFAULT_PYTHON_VERSION,
) -> bool:
    """Create a virtual environment using uv.

    Args:
        path: Path where the venv will be created (default: ~/SignalPilotHome/.venv)
        python_version: Python version to use (default: from config)

    Returns:
        bool: True if creation succeeded, False otherwise
    """
    uv = get_uv_path()
    with spinner("Creating virtual environment..."):
        result = subprocess.run(
            [uv, "venv", str(path), "--python", python_version],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            error("Failed to create virtual environment")
            error(result.stderr)
            return False
    success("Virtual environment created")
    return True


def install_packages(
    packages: list[str],
    venv_path: Path = config.SP_VENV,
) -> bool:
    """Install packages into a virtual environment using uv.

    Args:
        packages: List of packages to install
        venv_path: Path to the virtual environment (default: ~/SignalPilotHome/.venv)

    Returns:
        bool: True if installation succeeded, False otherwise
    """
    if not packages:
        return True

    uv = get_uv_path()
    with spinner(f"Installing {len(packages)} packages..."):
        result = subprocess.run(
            [uv, "pip", "install", "--python", str(venv_path), *packages],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            error("Failed to install packages")
            error(result.stderr)
            return False
    success(f"Installed {len(packages)} packages")
    return True


def get_installed_packages(venv_path: Path = config.SP_VENV) -> list[str]:
    """Get list of installed packages in a venv.

    Args:
        venv_path: Path to the virtual environment (default: ~/SignalPilotHome/.venv)

    Returns:
        list[str]: List of installed package names
    """
    uv = get_uv_path()
    result = subprocess.run(
        [uv, "pip", "list", "--python", str(venv_path), "--format", "freeze"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return []

    packages = []
    for line in result.stdout.strip().split("\n"):
        if "==" in line:
            packages.append(line.split("==")[0])
    return packages


def get_python_version(venv_path: Path = config.SP_VENV) -> str | None:
    """Get the Python version of a venv.

    Args:
        venv_path: Path to the virtual environment (default: ~/SignalPilotHome/.venv)

    Returns:
        str | None: Python version string (e.g., "3.12.0") or None if not found
    """
    python = config.get_venv_python()
    if not python.exists():
        return None

    result = subprocess.run(
        [str(python), "--version"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None

    # Parse "Python 3.12.0" -> "3.12.0"
    output = result.stdout.strip()
    if output.startswith("Python "):
        return output[7:]
    return output
