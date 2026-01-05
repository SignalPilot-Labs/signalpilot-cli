"""SignalPilot CLI main entry point."""

import typer

from sp.commands.init import init
from sp.commands.lab import lab

# TODO: Add new commands in Phase 3
# from sp.commands.activate import activate
# from sp.commands.install import install
# from sp.commands.upgrade import upgrade

app = typer.Typer(
    name="sp",
    help="SignalPilot CLI - Your Trusted CoPilot for Data Analysis",
    no_args_is_help=True,
)

# Register commands
# TODO: Uncomment when commands are implemented in Phase 3
# app.command()(activate)
app.command()(init)
app.command()(lab)
# app.command()(install)
# app.command()(upgrade)


@app.callback()
def callback() -> None:
    """SignalPilot CLI - Your Trusted CoPilot for Data Analysis."""
    pass


if __name__ == "__main__":
    app()
