"""sp upgrade - Upgrade SignalPilot CLI and AI library."""

import subprocess
from pathlib import Path

import typer

from sp import config
from sp.ui import error, info, spinner, success, warning


def get_signalpilot_library() -> str:
    """Get the SignalPilot AI library name from config.

    Returns:
        str: Library name (signalpilot-ai or signalpilot-ai-internal)
    """
    # Check user CLI config
    if config.SP_USER_CLI_CONFIG.exists():
        try:
            content = config.SP_USER_CLI_CONFIG.read_text()
            for line in content.split("\n"):
                if line.strip().startswith("library"):
                    # Parse: library = "signalpilot-ai"
                    lib = line.split("=")[1].strip().strip('"').strip("'")
                    return lib
        except Exception:
            pass

    # Default to public library
    return "signalpilot-ai"


def get_current_cli_version() -> str:
    """Get current CLI version.

    Returns:
        str: Version string or "unknown"
    """
    try:
        result = subprocess.run(
            ["uvx", "sp-cli", "--version"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            # Parse output like "sp-cli version 0.1.0"
            output = result.stdout.strip()
            if "version" in output:
                return output.split("version")[-1].strip()
        return "unknown"
    except Exception:
        return "unknown"


def get_latest_pypi_version(package: str) -> str | None:
    """Get latest version of a package from PyPI.

    Args:
        package: Package name

    Returns:
        str | None: Latest version or None if lookup fails
    """
    try:
        import json
        import urllib.request

        url = f"https://pypi.org/pypi/{package}/json"
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.loads(response.read())
            return data["info"]["version"]
    except Exception:
        return None


def upgrade_cli() -> bool:
    """Upgrade the SignalPilot CLI to latest version.

    Returns:
        bool: True if upgrade succeeded, False otherwise
    """
    with spinner("Checking for CLI updates..."):
        latest = get_latest_pypi_version("signalpilot-cli")

    if not latest:
        warning("Could not check for updates")
        return False

    current = get_current_cli_version()
    info(f"Current: {current}")
    info(f"Latest:  {latest}")

    if latest == current:
        success("CLI is up to date")
        return True

    # Upgrade via uvx
    with spinner(f"Upgrading CLI to {latest}..."):
        try:
            result = subprocess.run(
                ["uvx", "--upgrade", "sp-cli"],
                capture_output=True,
                text=True,
                timeout=60,
            )
            if result.returncode != 0:
                error("Failed to upgrade CLI")
                error(result.stderr)
                return False
        except Exception as e:
            error(f"Failed to upgrade CLI: {e}")
            return False

    success(f"CLI upgraded to {latest}")
    return True


def upgrade_library() -> bool:
    """Upgrade the SignalPilot AI library to latest version.

    Returns:
        bool: True if upgrade succeeded, False otherwise
    """
    # Check if global workspace is initialized
    if not config.is_initialized():
        error("SignalPilot not initialized. Run: sp init")
        return False

    library = get_signalpilot_library()

    with spinner(f"Checking for {library} updates..."):
        latest = get_latest_pypi_version(library)

    if not latest:
        info(f"{library} not found on PyPI (may not be published yet)")
        return True  # Not an error

    info(f"Upgrading {library} to {latest}...")

    # Upgrade in the global venv
    with spinner(f"Upgrading {library}..."):
        try:
            result = subprocess.run(
                [
                    "uv",
                    "pip",
                    "install",
                    "--upgrade",
                    f"{library}=={latest}",
                    "--python",
                    str(config.get_venv_python()),
                ],
                capture_output=True,
                text=True,
                timeout=120,
            )
            if result.returncode != 0:
                error(f"Failed to upgrade {library}")
                error(result.stderr)
                return False
        except Exception as e:
            error(f"Failed to upgrade {library}: {e}")
            return False

    success(f"{library} upgraded to {latest}")
    return True


def upgrade() -> None:
    """Upgrade SignalPilot CLI and AI library to latest versions.

    Upgrades:
    1. SignalPilot CLI (this tool) via uvx
    2. SignalPilot AI library (signalpilot-ai or signalpilot-ai-internal)

    The library name is read from ~/SignalPilotHome/.signalpilot/user-cli.toml
    """
    print()
    info("Upgrading SignalPilot...")
    print()

    # Upgrade CLI
    cli_ok = upgrade_cli()

    print()

    # Upgrade library (if initialized)
    lib_ok = upgrade_library()

    print()

    if cli_ok and lib_ok:
        success("Upgrade complete!")
    elif cli_ok:
        info("CLI upgraded, but library upgrade had issues")
        raise typer.Exit(1)
    elif lib_ok:
        info("Library upgraded, but CLI upgrade had issues")
        raise typer.Exit(1)
    else:
        error("Upgrade failed")
        raise typer.Exit(1)
