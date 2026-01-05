"""sp activate - Self-bootstrap SignalPilot CLI installation."""

from pathlib import Path

import typer

from sp.core.environment import is_running_in_uvx
from sp.ui import error, info, next_steps, success


def activate() -> None:
    """Self-bootstrap SignalPilot CLI installation.

    This command installs the 'sp' command permanently on your system.

    Run via: uvx sp-cli activate

    What it does:
    1. Creates ~/.local/bin/sp wrapper script
    2. Adds ~/.local/bin to PATH in shell rc files

    After running, you'll have 'sp' available system-wide.
    """
    # Check if running in uvx (temp environment)
    if not is_running_in_uvx():
        error("This command should be run via: uvx sp-cli activate")
        info("Install uv first: brew install uv")
        raise typer.Exit(1)

    # Create ~/.local/bin if doesn't exist
    local_bin = Path.home() / ".local" / "bin"
    local_bin.mkdir(parents=True, exist_ok=True)

    # Create sp wrapper script
    sp_wrapper = local_bin / "sp"
    wrapper_content = """#!/bin/sh
# SignalPilot CLI wrapper
exec uvx sp-cli "$@"
"""
    sp_wrapper.write_text(wrapper_content)
    sp_wrapper.chmod(0o755)
    success(f"Created CLI wrapper: {sp_wrapper}")

    # Add to PATH in shell rc files
    path_line = f'export PATH="{local_bin}:$PATH"'
    shell_rcs = [
        Path.home() / ".bashrc",
        Path.home() / ".zshrc",
    ]

    updated_shells = []
    for rc_file in shell_rcs:
        if not rc_file.exists():
            continue

        rc_content = rc_file.read_text()

        # Check if PATH already contains ~/.local/bin
        if str(local_bin) in rc_content or ".local/bin" in rc_content:
            continue

        # Append PATH export
        with rc_file.open("a") as f:
            f.write(f"\n# SignalPilot CLI\n{path_line}\n")

        updated_shells.append(rc_file.name)

    if updated_shells:
        success(f"Added to PATH: {', '.join(updated_shells)}")
    else:
        info("PATH already configured")

    # Display next steps
    print()
    success("SignalPilot CLI installed!")
    print()
    next_steps([
        ("source ~/.zshrc", "Reload shell (or restart terminal)"),
        ("sp init", "Initialize workspace"),
    ])
