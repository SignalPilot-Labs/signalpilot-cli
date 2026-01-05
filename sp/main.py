"""SignalPilot CLI main entry point."""

import typer

from sp.commands.activate import activate
from sp.commands.init import init
from sp.commands.lab import lab

app = typer.Typer(
    name="sp",
    help="SignalPilot CLI - Your Trusted CoPilot for Data Analysis",
    no_args_is_help=True,
)

# Register commands
app.command()(activate)
app.command()(init)
app.command()(lab)


@app.callback()
def callback() -> None:
    """SignalPilot CLI - Your Trusted CoPilot for Data Analysis."""
    pass


if __name__ == "__main__":
    app()
