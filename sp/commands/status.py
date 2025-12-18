"""sp status - Show SignalPilot installation status."""

from sp import config
from sp.core import environment, jupyter
from sp.ui import banner
from sp.ui.console import console, BRAND_SUCCESS, BRAND_ERROR, BRAND_MUTED


def status() -> None:
    """Show SignalPilot installation status."""
    # Display banner
    banner()

    # Home directory status
    home_ok = config.SIGNALPILOT_HOME.exists()
    _print_status_line(
        "Home",
        home_ok,
        str(config.SIGNALPILOT_HOME) if home_ok else "Not found",
    )

    # Environment status
    env_ok = config.is_initialized()
    if env_ok:
        python_version = environment.get_python_version()
        env_detail = f"default (Python {python_version})" if python_version else "default"
    else:
        env_detail = "Not initialized - run 'sp init'"
    _print_status_line("Environment", env_ok, env_detail)

    # Kernels status
    kernels = jupyter.get_registered_kernels()
    kernels_ok = len(kernels) > 0
    if kernels_ok:
        kernels_detail = ", ".join(kernels)
    else:
        kernels_detail = "None - run 'sp init'"
    _print_status_line("Kernels", kernels_ok, kernels_detail)

    # JupyterLab running status
    jupyter_running = jupyter.check_jupyter_running()
    _print_status_line(
        "JupyterLab",
        jupyter_running,
        "Running on port 8888" if jupyter_running else "Not running",
        show_circle=True,
    )


def _print_status_line(
    label: str,
    ok: bool,
    detail: str,
    show_circle: bool = False,
) -> None:
    """Print a formatted status line.

    Args:
        label: Status label (left column).
        ok: Whether the status is good/OK.
        detail: Detail text to show.
        show_circle: Use circle instead of checkmark (for running status).
    """
    if show_circle:
        icon = "●" if ok else "○"
    else:
        icon = "✓" if ok else "✗"

    color = BRAND_SUCCESS if ok else BRAND_ERROR if not show_circle else BRAND_MUTED

    console.print(f"  {label:<14}[{color}]{icon}[/]   {detail}")
