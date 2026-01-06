# SignalPilot CLI (`sp-cli`)

Your Trusted CoPilot for Data Analysis - A simple CLI tool to bootstrap Jupyter-powered data science workspaces with AI agent support.

## Features

- 🚀 **One-command setup** - Get from zero to Jupyter Lab in under 3 minutes
- 🐍 **Python 3.12** - Uses the latest Python with uv for fast package management
- 📊 **Pre-configured workspace** - Includes pandas, numpy, matplotlib, seaborn, plotly
- 🤖 **AI-ready** - Built-in SignalPilot AI agent support
- ⚡ **Fast** - Optimized Jupyter cache for quick startups
- 🎨 **Beautiful CLI** - Clean, colorful terminal output

## Installation

```bash
# Install uv (if you don't have it)
brew install uv  # macOS
# OR
curl -LsSf https://astral.sh/uv/install.sh | sh  # Linux/macOS

# Run SignalPilot init
uvx sp-cli
```

That's it! The tool will:
1. Create `~/SignalPilotHome` directory structure
2. Download starter notebook and dependencies
3. Set up Python 3.12 virtual environment
4. Install Jupyter Lab and data science packages
5. Optimize for fast startup

## Usage

After running `uvx sp-cli`, follow the next steps:

```bash
cd ~/SignalPilotHome && source .venv/bin/activate
jupyter lab
```

## What Gets Installed

**Python Packages:**
- `signalpilot-ai` - AI agent integration
- `jupyterlab` - Modern Jupyter interface
- `pandas`, `numpy` - Data manipulation
- `matplotlib`, `seaborn`, `plotly` - Visualization
- `python-dotenv`, `tomli` - Configuration utilities

**Directory Structure:**
```
~/SignalPilotHome/
├── user-skills/       # Custom agent skills
├── user-rules/        # Custom agent rules
├── team-workspace/    # Shared team notebooks
├── demo-project/      # Example notebooks
├── start-here.ipynb   # Quick start guide
└── .venv/             # Python environment
```

## Requirements

- Python 3.10 or higher
- [uv](https://docs.astral.sh/uv/) package manager

## License

MIT License - See LICENSE file for details

## Links

- [Homepage](https://signalpilot.ai)
- [Documentation](https://docs.signalpilot.ai)
- [GitHub](https://github.com/SignalPilot-Labs/sp-cli)