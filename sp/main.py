"""SignalPilot CLI - Simple init command"""

import subprocess
import sys
import urllib.request
from pathlib import Path

import typer
from rich.console import Console
from rich.tree import Tree

app = typer.Typer(
    name="sp",
    help="SignalPilot CLI - Bootstrap your data analysis workspace",
    no_args_is_help=True,
)

console = Console()

LOGO = """   ┌───┐
   │ ↗ │  ╔═╗┬┌─┐┌┐┌┌─┐┬  ╔═╗┬┬  ┌─┐┌┬┐
   │▓▓▓│  ╚═╗││ ┬│││├─┤│  ╠═╝││  │ │ │
   │▓░░│  ╚═╝┴└─┘┘└┘┴ ┴┴─┘╩  ┴┴─┘└─┘ ┴
   └───┘"""


def check_uv() -> bool:
    """Check if uv is installed"""
    try:
        subprocess.run(
            ["uv", "--version"],
            check=True,
            capture_output=True,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def download_file(url: str, dest_path: Path):
    """Download a file from URL to destination path. Exits on failure."""
    try:
        console.print(f"  → Downloading {dest_path.name}...", style="dim")
        urllib.request.urlretrieve(url, dest_path)
    except Exception as e:
        console.print(f"  ✗ Failed to download {dest_path.name}: {e}", style="bold red")
        sys.exit(1)


def print_directory_tree(base_path: Path):
    """Print a nice directory structure"""
    tree = Tree(
        f"[bold cyan]{base_path.name}/[/bold cyan]",
        guide_style="dim"
    )

    # Add subdirectories
    tree.add("[cyan]user-skills/[/cyan]")
    tree.add("[cyan]user-rules/[/cyan]")
    tree.add("[cyan]team-workspace/[/cyan]")
    tree.add("[cyan]demo-project/[/cyan]")

    console.print(tree)


def optimize_jupyter_cache(home_dir: Path):
    """Warm up Jupyter to initialize caches for faster startup"""
    console.print("\n→ Optimizing Jupyter for fast startup...", style="bold cyan")
    console.print("  (This may take 20-30 seconds)\n", style="dim")

    try:
        venv_jupyter = home_dir / ".venv" / "bin" / "jupyter"

        # Disable announcements extension
        subprocess.run(
            [str(venv_jupyter), "labextension", "disable", "@jupyterlab/apputils-extension:announcements"],
            cwd=home_dir,
            capture_output=True,
            check=False,  # Don't fail if already disabled
        )

        # Lock announcements extension
        subprocess.run(
            [str(venv_jupyter), "labextension", "lock", "@jupyterlab/apputils-extension:announcements"],
            cwd=home_dir,
            capture_output=True,
            check=False,  # Don't fail if already locked
        )

        # Warm-up run: start Jupyter to initialize caches
        jupyter_process = subprocess.Popen(
            [str(venv_jupyter), "lab", "--no-browser", "--allow-root", "--port=19999"],
            cwd=home_dir,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        # Wait for Jupyter to be ready (up to 30 seconds)
        import time
        max_wait = 20
        jupyter_ready = False

        for i in range(max_wait):
            # Check if process is still running
            if jupyter_process.poll() is not None:
                console.print("  → Jupyter process exited early", style="yellow")
                break

            try:
                import urllib.request
                urllib.request.urlopen("http://localhost:19999/api", timeout=1)
                jupyter_ready = True
                console.print("  ✓ Jupyter cache initialized (100%)", style="green")
                break
            except Exception:
                progress = int((i + 1) / max_wait * 100)
                console.print(f"  → Warming up... {progress}%", style="dim", end="\r")
                time.sleep(1)

        if not jupyter_ready:
            console.print("  → Skipping optimization (timeout)     ", style="yellow")

        # Shutdown Jupyter
        try:
            jupyter_process.terminate()
            jupyter_process.wait(timeout=5)
        except Exception:
            jupyter_process.kill()

    except Exception as e:
        console.print(f"  → Skipping optimization: {e}", style="yellow")
        # Don't fail the entire process if optimization fails


@app.command()
def init():
    """Initialize SignalPilot workspace at ~/SignalPilotHome"""

    # Check for uv
    console.print("→ Checking for uv...", style="dim")
    if not check_uv():
        console.print("✗ uv is not installed", style="bold red")
        console.print("\nPlease install uv first:", style="yellow")
        console.print("  macOS/Linux: curl -LsSf https://astral.sh/uv/install.sh | sh")
        console.print("  Windows:     powershell -c \"irm https://astral.sh/uv/install.ps1 | iex\"")
        console.print("  Or via package manager: brew install uv")
        sys.exit(1)

    console.print("✓ uv found", style="green")

    # Create directory structure
    home_dir = Path.home() / "SignalPilotHome"
    console.print(f"\n→ Setting up workspace at [bold]{home_dir}[/bold]", style="dim")

    # Create main directory and subdirectories
    home_dir.mkdir(exist_ok=True)
    (home_dir / "user-skills").mkdir(exist_ok=True)
    (home_dir / "user-rules").mkdir(exist_ok=True)
    (home_dir / "team-workspace").mkdir(exist_ok=True)
    (home_dir / "demo-project").mkdir(exist_ok=True)

    console.print("\n✓ Directory structure created:", style="green")
    print_directory_tree(home_dir)

    # Check for existing pyproject.toml
    pyproject_path = home_dir / "pyproject.toml"
    download_pyproject = True

    if pyproject_path.exists():
        response = typer.prompt(
            "\npyproject.toml already exists. Overwrite? y/n",
            default="y",
            show_default=True,
        )
        download_pyproject = response.lower() in ["y", "yes"]

    # Download files from GitHub
    base_url = "https://raw.githubusercontent.com/SignalPilot-Labs/sp-cli/refs/heads/sp-cli-v1/defaultSignalPilotHome/"

    console.print("\n→ Downloading workspace files...", style="dim")

    # Always download start-here.ipynb
    download_file(base_url + "start-here.ipynb", home_dir / "start-here.ipynb")

    # Download pyproject.toml if approved
    if download_pyproject:
        download_file(base_url + "pyproject.toml", pyproject_path)
    else:
        console.print("  → Keeping existing pyproject.toml", style="yellow")

    console.print("\n✓ Files downloaded successfully", style="green")

    # Create venv with specific Python version
    console.print("\n→ Creating Python virtual environment...", style="bold cyan")
    console.print("  (Using Python 3.12)\n", style="dim")

    try:
        subprocess.run(
            ["uv", "venv", "--clear", "--seed", "--python", "3.12"],
            cwd=home_dir,
            check=True,
        )
        console.print("\n✓ Virtual environment created", style="green")
    except subprocess.CalledProcessError as e:
        console.print(f"\n✗ uv venv failed with exit code {e.returncode}", style="bold red")
        console.print("\nTry running manually:", style="yellow")
        console.print(f"  cd {home_dir}")
        console.print("  uv venv --seed --python 3.12")
        sys.exit(1)

    # Install dependencies using uv pip install
    console.print("\n→ Installing dependencies...", style="bold cyan")
    console.print("  (This may take a minute)\n", style="dim")

    try:
        # Don't capture output - show everything to the user
        subprocess.run(
            ["uv", "pip", "install", "-r", "pyproject.toml"],
            cwd=home_dir,
            check=True,
        )
        console.print("\n✓ Dependencies installed successfully", style="bold green")
    except subprocess.CalledProcessError as e:
        console.print(f"\n✗ uv pip install failed with exit code {e.returncode}", style="bold red")
        console.print("\nTry running manually:", style="yellow")
        console.print(f"  cd {home_dir}")
        console.print("  uv pip install -r pyproject.toml")
        sys.exit(1)

    # Optimize Jupyter cache
    optimize_jupyter_cache(home_dir)

    # Get version information from the venv
    python_version = "unknown"
    try:
        result = subprocess.run(
            [str(home_dir / ".venv" / "bin" / "python"), "--version"],
            capture_output=True,
            text=True,
            check=True,
        )
        # Output is like "Python 3.12.7"
        python_version = result.stdout.strip().split()[1]
    except Exception:
        pass

    # Get SignalPilot version from installed packages
    sp_version = "unknown"
    try:
        result = subprocess.run(
            [str(home_dir / ".venv" / "bin" / "pip"), "show", "signalpilot-ai"],
            capture_output=True,
            text=True,
            check=True,
        )
        for line in result.stdout.split("\n"):
            if line.startswith("Version:"):
                sp_version = line.split(":", 1)[1].strip()
                break
    except Exception:
        pass

    # Success message with logo and versions
    console.print("\n" + "="*60, style="white")
    console.print(LOGO, style="cyan")
    console.print("\n✓ SignalPilotHome created successfully!", style="bold green")
    console.print(f"  SignalPilot: v{sp_version} | Python: {python_version}", style="dim")
    console.print("="*60, style="white")

    console.print("\n[bold red]NEXT STEPS[/bold red]")
    console.print(f"[green]Step 1: cd {home_dir} && source .venv/bin/activate[/green]")
    console.print("[green]STep 2: jupyter lab[/green]")
    console.print("\n" + "="*60 + "\n", style="white")


if __name__ == "__main__":
    app()
