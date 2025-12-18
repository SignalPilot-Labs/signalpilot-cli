"""SignalPilot CLI main entry point."""

import typer

from sp.commands.init import init
from sp.commands.lab import lab
from sp.commands.status import status

app = typer.Typer(
    name="sp",
    help="SignalPilot CLI - Your Trusted CoPilot for Data Analysis",
    no_args_is_help=True,
)

# Register commands
app.command()(init)
app.command()(lab)
app.command()(status)


@app.callback()
def callback() -> None:
    """SignalPilot CLI - Your Trusted CoPilot for Data Analysis."""
    pass


if __name__ == "__main__":
    app()
