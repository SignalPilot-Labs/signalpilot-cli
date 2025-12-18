# SignalPilot CLI - R Language Support Specification

## Overview

Add R language support to the SignalPilot CLI for academic users who work with R and RMarkdown. This is a separate feature module that can be built after the MVP.

**Prerequisite**: MVP CLI must be complete (`sp init`, `sp lab`, `sp status`).

## User Journey

```
sp r status                    # Check R installation
sp r install                   # Install IRkernel for Jupyter
sp r convert analysis.Rmd      # Convert RMarkdown to notebook
sp lab                         # Launch Jupyter with R kernel available
```

## Commands to Implement

### 1. `sp r status`

**Purpose**: Check R installation and kernel status.

**Output when R is fully set up**:
```
  R              ✓ Installed    version 4.3.1
  IRkernel       ✓ Installed
  Jupyter kernel ✓ Registered
```

**Output when R needs setup**:
```
  R              ✓ Installed    version 4.3.1
  IRkernel       ✗ Not installed    Run 'sp r install'
  Jupyter kernel ✗ Not registered   Run 'sp r install'
```

**Output when R not found**:
```
  R              ✗ Not found    Install from cran.r-project.org
  IRkernel       —
  Jupyter kernel —
```

**Implementation**:
```python
def check_r() -> bool:
    """Check if R is installed and in PATH."""
    try:
        result = subprocess.run(["R", "--version"], capture_output=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def get_r_version() -> str | None:
    """Get R version string."""
    result = subprocess.run(["R", "--version"], capture_output=True, text=True)
    # Parse "R version 4.3.1 (2023-06-16)" from first line
    ...

def check_irkernel() -> bool:
    """Check if IRkernel R package is installed."""
    result = subprocess.run(
        ["R", "-e", "requireNamespace('IRkernel', quietly=TRUE)"],
        capture_output=True, text=True
    )
    return "TRUE" in result.stdout
```

---

### 2. `sp r install`

**Purpose**: Install IRkernel and register it with Jupyter.

**Options**:
```
--name, -n       Kernel name (default: "r")
--display-name   Display name in Jupyter (default: "R (version)")
```

**Steps**:
1. Check R is installed (exit with error if not)
2. Install IRkernel R package from CRAN
3. Create kernel spec in SignalPilot's Jupyter directory
4. Print success message

**Install IRkernel**:
```python
subprocess.run([
    "R", "-e",
    "if (!requireNamespace('IRkernel', quietly=TRUE)) "
    "install.packages('IRkernel', repos='https://cloud.r-project.org')"
])
```

**Create kernel spec** at `~/SignalPilotHome/system/jupyter/kernels/r/kernel.json`:
```json
{
  "argv": [
    "R",
    "--slave",
    "-e", "IRkernel::main()",
    "--args", "{connection_file}"
  ],
  "display_name": "R (4.3.1)",
  "language": "R",
  "metadata": {
    "signalpilot": true
  }
}
```

**Note**: We create the kernel spec manually rather than using `IRkernel::installspec()` to ensure it goes into SignalPilot's Jupyter directory, not the system location.

**Output on success**:
```
→ Found R 4.3.1
✓ IRkernel package installed
✓ Registered R kernel as 'r'
  Display name: R (4.3.1)
```

**Output when R not found**:
```
✗ R is not installed or not in PATH
  Install R from https://cran.r-project.org/ or use your package manager:
    macOS:  brew install r
    Ubuntu: sudo apt install r-base
    Fedora: sudo dnf install R
```

---

### 3. `sp r convert`

**Purpose**: Convert RMarkdown (.Rmd) files to Jupyter notebooks (.ipynb).

**Usage**:
```
sp r convert <files...> [--output DIR] [--overwrite]
```

**Options**:
```
files            One or more .Rmd files to convert
--output, -o     Output directory (default: same as input file)
--overwrite, -f  Overwrite existing .ipynb files
```

**Implementation**:
Uses `jupytext` which handles Rmd → ipynb conversion perfectly.

**Steps**:
1. Check if `jupytext` is installed in SignalPilot env; install if not
2. For each input file:
   - Validate it's an .Rmd file
   - Determine output path
   - Check if output exists (error unless --overwrite)
   - Run jupytext conversion
   - Print success/error

**Core conversion**:
```python
# Install jupytext if needed
env_path = config.get_env_path("default")
jupytext_path = env_path / "bin" / "jupytext"

if not jupytext_path.exists():
    subprocess.run([
        "uv", "pip", "install", 
        "--python", str(env_path), 
        "jupytext"
    ])

# Convert
subprocess.run([
    str(jupytext_path),
    "--to", "notebook",
    "--output", str(output_file),
    str(input_file)
])
```

**Output**:
```
→ Converting analysis.Rmd...
✓ Converted: analysis.ipynb

→ Converting report.Rmd...
✓ Converted: output/report.ipynb
```

**Error cases**:
```
✗ File not found: missing.Rmd

✗ Not an Rmd file: data.csv

✗ Output exists (use --overwrite): analysis.ipynb
```

---

## File Structure

Add to existing CLI:

```
sp/
├── commands/
│   ├── ...
│   └── r.py            # NEW: sp r commands
└── core/
    ├── ...
    └── r.py            # NEW: R helper functions (optional, can inline)
```

---

## Full Command Implementation

```python
# sp/commands/r.py
"""sp r - R language support."""
import typer
import subprocess
from pathlib import Path
from typing import Optional, List
from sp import config
from sp.ui import success, error, info, muted, spinner
from sp.ui.console import console

app = typer.Typer(help="R language support")


def check_r() -> bool:
    """Check if R is installed."""
    try:
        result = subprocess.run(["R", "--version"], capture_output=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False


def get_r_version() -> Optional[str]:
    """Get installed R version."""
    try:
        result = subprocess.run(["R", "--version"], capture_output=True, text=True)
        first_line = result.stdout.split("\n")[0]
        if "R version" in first_line:
            return first_line.split()[2]
    except Exception:
        pass
    return None


def check_irkernel() -> bool:
    """Check if IRkernel is installed."""
    result = subprocess.run(
        ["R", "-e", "requireNamespace('IRkernel', quietly=TRUE)"],
        capture_output=True, text=True
    )
    return result.returncode == 0 and "TRUE" in result.stdout


@app.command("status")
def status():
    """Check R installation status."""
    from rich.table import Table
    from sp.ui.console import BRAND_SUCCESS, BRAND_ERROR, BRAND_MUTED
    
    table = Table(show_header=False, box=None)
    table.add_column("Component", style="bold")
    table.add_column("Status")
    table.add_column("Details")
    
    # R installation
    if check_r():
        version = get_r_version()
        table.add_row("R", f"[{BRAND_SUCCESS}]✓ Installed[/]", f"version {version}")
        
        # IRkernel
        if check_irkernel():
            table.add_row("IRkernel", f"[{BRAND_SUCCESS}]✓ Installed[/]", "")
        else:
            table.add_row("IRkernel", f"[{BRAND_ERROR}]✗ Not installed[/]", "Run 'sp r install'")
        
        # Jupyter kernel
        r_kernel = config.JUPYTER_KERNELS_DIR / "r"
        if r_kernel.exists():
            table.add_row("Jupyter kernel", f"[{BRAND_SUCCESS}]✓ Registered[/]", "")
        else:
            table.add_row("Jupyter kernel", f"[{BRAND_ERROR}]✗ Not registered[/]", "Run 'sp r install'")
    else:
        table.add_row("R", f"[{BRAND_ERROR}]✗ Not found[/]", "Install from cran.r-project.org")
        table.add_row("IRkernel", f"[{BRAND_MUTED}]—[/]", "")
        table.add_row("Jupyter kernel", f"[{BRAND_MUTED}]—[/]", "")
    
    console.print(table)


@app.command("install")
def install_kernel(
    name: str = typer.Option("r", "--name", "-n", help="Kernel name"),
    display_name: Optional[str] = typer.Option(None, "--display-name", help="Display name"),
):
    """Install IRkernel for Jupyter."""
    import json
    
    if not check_r():
        error("R is not installed or not in PATH")
        info("Install R from https://cran.r-project.org/ or:")
        muted("  macOS:  brew install r")
        muted("  Ubuntu: sudo apt install r-base")
        raise typer.Exit(1)
    
    version = get_r_version()
    info(f"Found R {version}")
    
    if display_name is None:
        display_name = f"R ({version})" if version else "R"
    
    # Install IRkernel
    with spinner("Installing IRkernel package..."):
        result = subprocess.run(
            ["R", "-e",
             "if (!requireNamespace('IRkernel', quietly=TRUE)) "
             "install.packages('IRkernel', repos='https://cloud.r-project.org')"],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            error("Failed to install IRkernel")
            console.print(result.stderr)
            raise typer.Exit(1)
    
    success("IRkernel package installed")
    
    # Create kernel spec
    kernel_dir = config.JUPYTER_KERNELS_DIR / name
    kernel_dir.mkdir(parents=True, exist_ok=True)
    
    kernel_spec = {
        "argv": ["R", "--slave", "-e", "IRkernel::main()", "--args", "{connection_file}"],
        "display_name": display_name,
        "language": "R",
        "metadata": {"signalpilot": True}
    }
    
    (kernel_dir / "kernel.json").write_text(json.dumps(kernel_spec, indent=2))
    
    success(f"Registered R kernel as '{name}'")
    muted(f"Display name: {display_name}")


@app.command("convert")
def convert_rmd(
    files: List[Path] = typer.Argument(..., help="Rmd files to convert"),
    output_dir: Optional[Path] = typer.Option(None, "--output", "-o", help="Output directory"),
    overwrite: bool = typer.Option(False, "--overwrite", "-f", help="Overwrite existing"),
):
    """Convert RMarkdown files to Jupyter notebooks."""
    import shutil
    
    # Ensure jupytext is installed
    env_path = config.DEFAULT_VENV_DIR
    jupytext_path = env_path / "bin" / "jupytext"
    
    if not jupytext_path.exists():
        with spinner("Installing jupytext..."):
            subprocess.run(
                ["uv", "pip", "install", "--python", str(env_path), "jupytext"],
                capture_output=True
            )
    
    for rmd_file in files:
        if not rmd_file.exists():
            error(f"File not found: {rmd_file}")
            continue
        
        if rmd_file.suffix.lower() not in [".rmd", ".rmarkdown"]:
            error(f"Not an Rmd file: {rmd_file}")
            continue
        
        # Determine output path
        if output_dir:
            output_dir.mkdir(parents=True, exist_ok=True)
            output_file = output_dir / rmd_file.with_suffix(".ipynb").name
        else:
            output_file = rmd_file.with_suffix(".ipynb")
        
        if output_file.exists() and not overwrite:
            error(f"Output exists (use --overwrite): {output_file}")
            continue
        
        with spinner(f"Converting {rmd_file.name}..."):
            result = subprocess.run(
                [str(jupytext_path), "--to", "notebook", "--output", str(output_file), str(rmd_file)],
                capture_output=True, text=True
            )
            
            if result.returncode != 0:
                error(f"Failed to convert {rmd_file.name}")
                continue
        
        success(f"Converted: {output_file}")
```

---

## Register with Main CLI

In `sp/main.py`, add:

```python
from sp.commands import r

app.add_typer(r.app, name="r", help="R language support")
```

---

## Testing Checklist

- [ ] `sp r status` works when R is not installed
- [ ] `sp r status` works when R is installed but IRkernel is not
- [ ] `sp r status` works when fully configured
- [ ] `sp r install` installs IRkernel from CRAN
- [ ] `sp r install` creates kernel spec in correct location
- [ ] `sp r install` fails gracefully when R not found
- [ ] `sp r convert` converts single .Rmd file
- [ ] `sp r convert` converts multiple files
- [ ] `sp r convert --output` puts files in specified directory
- [ ] `sp r convert` respects --overwrite flag
- [ ] R kernel appears in JupyterLab after `sp r install`
- [ ] R notebooks work correctly in JupyterLab

---

## Dependencies

No additional dependencies in `pyproject.toml`. Uses:
- `jupytext` (installed into SignalPilot env on first use)
- System R installation (user's responsibility)

---

## User Documentation

Add to README:

```markdown
## R Support

SignalPilot supports R for academic users working with RMarkdown.

### Prerequisites

Install R from [CRAN](https://cran.r-project.org/) or your package manager:

```bash
# macOS
brew install r

# Ubuntu/Debian
sudo apt install r-base

# Fedora
sudo dnf install R
```

### Setup

```bash
# Check R installation
sp r status

# Install R kernel for Jupyter
sp r install
```

### Converting RMarkdown

```bash
# Convert single file
sp r convert analysis.Rmd

# Convert multiple files
sp r convert *.Rmd

# Convert to specific directory
sp r convert notebook.Rmd --output converted/
```

After conversion, open the `.ipynb` file in JupyterLab with `sp lab`.
```
