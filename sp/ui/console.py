"""Rich console utilities with SignalPilot branding."""

from contextlib import contextmanager
from typing import Generator

from rich.console import Console
from rich.panel import Panel
from rich.style import Style
from rich.text import Text
from rich.status import Status

# Brand colors
BRAND_PRIMARY = "#8B5CF6"    # Soft violet
BRAND_SECONDARY = "#A78BFA"  # Light violet
BRAND_SUCCESS = "#10B981"    # Green
BRAND_WARNING = "#F59E0B"    # Amber
BRAND_ERROR = "#EF4444"      # Red
BRAND_MUTED = "#6B7280"      # Gray

# Rich styles
style_primary = Style(color=BRAND_PRIMARY)
style_secondary = Style(color=BRAND_SECONDARY)
style_success = Style(color=BRAND_SUCCESS)
style_warning = Style(color=BRAND_WARNING)
style_error = Style(color=BRAND_ERROR)
style_muted = Style(color=BRAND_MUTED)

# Global console instance
console = Console()


def success(message: str) -> None:
    """Print a success message with checkmark."""
    console.print(f"[{BRAND_SUCCESS}]✓[/] {message}")


def error(message: str) -> None:
    """Print an error message with X."""
    console.print(f"[{BRAND_ERROR}]✗[/] {message}")


def info(message: str) -> None:
    """Print an info message with arrow."""
    console.print(f"[{BRAND_MUTED}]→[/] {message}")


def warning(message: str) -> None:
    """Print a warning message."""
    console.print(f"[{BRAND_WARNING}]![/] {message}")


def muted(message: str) -> None:
    """Print muted/dim text."""
    console.print(f"[{BRAND_MUTED}]{message}[/]")


def banner() -> None:
    """Display the SignalPilot branded banner."""
    banner_text = Text()
    banner_text.append("\n")
    banner_text.append("  SignalPilot\n", style=f"bold {BRAND_PRIMARY}")
    banner_text.append("  Your Trusted CoPilot for Data Analysis\n", style=BRAND_MUTED)
    banner_text.append("\n")

    panel = Panel(
        banner_text,
        border_style=BRAND_PRIMARY,
        padding=(0, 2),
    )
    console.print(panel)


def next_steps(steps: list[tuple[str, str]]) -> None:
    """Display a panel with next steps.

    Args:
        steps: List of (command, description) tuples.
    """
    content = Text()
    for cmd, desc in steps:
        content.append(f"  {cmd:<18}", style="bold")
        content.append(f"{desc}\n", style=BRAND_MUTED)

    panel = Panel(
        content,
        title="[bold]Next steps[/]",
        title_align="left",
        border_style=BRAND_MUTED,
        padding=(0, 1),
    )
    console.print(panel)


@contextmanager
def spinner(message: str) -> Generator[Status, None, None]:
    """Show a spinner while an operation is in progress.

    Usage:
        with spinner("Installing packages..."):
            # do work
    """
    with console.status(f"[{BRAND_MUTED}]{message}[/]", spinner="dots") as status:
        yield status
