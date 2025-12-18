"""SignalPilot CLI configuration - paths and constants."""

from pathlib import Path

# SignalPilot Home directory
SIGNALPILOT_HOME = Path.home() / "SignalPilotHome"

# User directories
NOTEBOOKS_DIR = SIGNALPILOT_HOME / "notebooks"
SKILLS_DIR = SIGNALPILOT_HOME / "skills"
CONNECTIONS_DIR = SIGNALPILOT_HOME / "connections"
CONFIG_DIR = SIGNALPILOT_HOME / "config"

# System directories
SYSTEM_DIR = SIGNALPILOT_HOME / "system"
DEFAULT_VENV_DIR = SYSTEM_DIR / "signal_pilot"
LOGS_DIR = SYSTEM_DIR / "logs"
CACHE_DIR = SYSTEM_DIR / "cache"

# Jupyter directories
JUPYTER_DIR = SYSTEM_DIR / "jupyter"
JUPYTER_RUNTIME_DIR = JUPYTER_DIR / "runtime"
JUPYTER_KERNELS_DIR = JUPYTER_DIR / "kernels"

# Default Python version
DEFAULT_PYTHON_VERSION = "3.12"

# Default kernel name
DEFAULT_KERNEL_NAME = "signalpilot"
DEFAULT_KERNEL_DISPLAY_NAME = f"SignalPilot (Python {DEFAULT_PYTHON_VERSION})"

# Core packages (always installed)
CORE_PACKAGES = [
    "jupyterlab",
    "ipykernel",
    "pandas",
    "numpy",
]

# Data science packages (installed unless --minimal)
DATASCIENCE_PACKAGES = [
    "matplotlib",
    "seaborn",
    "scikit-learn",
]

# SignalPilot packages
SIGNALPILOT_PACKAGES = [
    "signalpilot-ai",
]

# All directories to create during init
ALL_DIRS = [
    NOTEBOOKS_DIR,
    SKILLS_DIR,
    CONNECTIONS_DIR,
    CONFIG_DIR,
    LOGS_DIR,
    CACHE_DIR,
    JUPYTER_DIR,
    JUPYTER_RUNTIME_DIR,
    JUPYTER_KERNELS_DIR,
]


def get_jupyter_env() -> dict[str, str]:
    """Get environment variables for Jupyter."""
    return {
        "JUPYTER_CONFIG_DIR": str(CONFIG_DIR),
        "JUPYTER_DATA_DIR": str(JUPYTER_DIR),
        "JUPYTER_RUNTIME_DIR": str(JUPYTER_RUNTIME_DIR),
    }


def is_initialized() -> bool:
    """Check if SignalPilot has been initialized."""
    return (
        SIGNALPILOT_HOME.exists()
        and DEFAULT_VENV_DIR.exists()
        and (DEFAULT_VENV_DIR / "bin" / "python").exists()
    )


def get_venv_python() -> Path:
    """Get the path to the venv Python executable."""
    return DEFAULT_VENV_DIR / "bin" / "python"


def get_venv_bin(name: str) -> Path:
    """Get the path to a binary in the venv."""
    return DEFAULT_VENV_DIR / "bin" / name
