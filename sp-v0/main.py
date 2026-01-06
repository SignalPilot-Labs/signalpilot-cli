"""SignalPilot CLI main entry point."""

import typer

from sp.commands.activate import activate
from sp.commands.init import init
from sp.commands.install import install
from sp.commands.lab import lab
from sp.commands.upgrade import upgrade

app = typer.Typer(
    name="sp",
    help="SignalPilot CLI - Your Trusted CoPilot for Data Analysis",
    no_args_is_help=True,
)

# Register commands
app.command()(activate)
app.command()(init)
app.command()(install)
app.command(
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True}
)(lab)
app.command()(upgrade)


@app.callback()
def callback() -> None:
    """SignalPilot CLI - Your Trusted CoPilot for Data Analysis."""
    pass


if __name__ == "__main__":
    app()
