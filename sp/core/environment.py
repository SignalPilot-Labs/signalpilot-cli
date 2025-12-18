"""Environment management using uv."""

import shutil
import subprocess
from pathlib import Path

from sp import config
from sp.ui import error, info, success, spinner


def check_uv() -> bool:
    """Check if uv is installed and available."""
    return shutil.which("uv") is not None


def install_uv() -> bool:
    """Install uv using the official installer.

    Returns:
        True if installation succeeded, False otherwise.
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
    """Get the path to uv executable."""
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
        True if uv is available, False otherwise.
    """
    if check_uv():
        return True

    info("uv not found, installing...")
    if not install_uv():
        error("Could not install uv automatically.")
        error("Please install uv manually: https://docs.astral.sh/uv/getting-started/installation/")
        return False

    return True


def install_python(version: str = config.DEFAULT_PYTHON_VERSION) -> bool:
    """Install Python using uv.

    Args:
        version: Python version to install.

    Returns:
        True if installation succeeded, False otherwise.
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
    path: Path = config.DEFAULT_VENV_DIR,
    python_version: str = config.DEFAULT_PYTHON_VERSION,
) -> bool:
    """Create a virtual environment using uv.

    Args:
        path: Path where the venv will be created.
        python_version: Python version to use.

    Returns:
        True if creation succeeded, False otherwise.
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
    venv_path: Path = config.DEFAULT_VENV_DIR,
) -> bool:
    """Install packages into a virtual environment using uv.

    Args:
        packages: List of packages to install.
        venv_path: Path to the virtual environment.

    Returns:
        True if installation succeeded, False otherwise.
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


def get_installed_packages(venv_path: Path = config.DEFAULT_VENV_DIR) -> list[str]:
    """Get list of installed packages in a venv.

    Args:
        venv_path: Path to the virtual environment.

    Returns:
        List of installed package names.
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


def get_python_version(venv_path: Path = config.DEFAULT_VENV_DIR) -> str | None:
    """Get the Python version of a venv.

    Args:
        venv_path: Path to the virtual environment.

    Returns:
        Python version string or None if not found.
    """
    python = venv_path / "bin" / "python"
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
