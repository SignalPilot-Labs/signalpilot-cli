"""Tests for SignalPilot CLI."""

import subprocess
import sys
from pathlib import Path

import pytest
from typer.testing import CliRunner

from sp import config
from sp.main import app
from sp.core import environment, jupyter
from sp.ui import console as ui_console


runner = CliRunner()


class TestConfig:
    """Test configuration module."""

    def test_paths_are_pathlib(self):
        """All path configs should be Path objects."""
        assert isinstance(config.SIGNALPILOT_HOME, Path)
        assert isinstance(config.DEFAULT_VENV_DIR, Path)
        assert isinstance(config.NOTEBOOKS_DIR, Path)

    def test_jupyter_env_vars(self):
        """Jupyter env vars should be set correctly."""
        env = config.get_jupyter_env()
        assert "JUPYTER_CONFIG_DIR" in env
        assert "JUPYTER_DATA_DIR" in env
        assert "JUPYTER_RUNTIME_DIR" in env

    def test_packages_defined(self):
        """Package lists should be non-empty."""
        assert len(config.CORE_PACKAGES) > 0
        assert "jupyterlab" in config.CORE_PACKAGES
        assert "ipykernel" in config.CORE_PACKAGES


class TestEnvironment:
    """Test environment module."""

    def test_check_uv(self):
        """uv should be available."""
        assert environment.check_uv() is True

    def test_get_uv_path(self):
        """Should return a valid uv path."""
        uv_path = environment.get_uv_path()
        assert uv_path is not None
        assert len(uv_path) > 0


class TestJupyter:
    """Test jupyter module."""

    def test_get_registered_kernels(self):
        """Should return list of kernels."""
        kernels = jupyter.get_registered_kernels()
        assert isinstance(kernels, list)

    def test_check_jupyter_running(self):
        """Should return boolean for jupyter status."""
        result = jupyter.check_jupyter_running(port=19998)  # Unlikely port
        assert result is False


class TestCLI:
    """Test CLI commands."""

    def test_help(self):
        """sp --help should work."""
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "SignalPilot" in result.stdout

    def test_init_help(self):
        """sp init --help should work."""
        result = runner.invoke(app, ["init", "--help"])
        assert result.exit_code == 0
        assert "--python" in result.stdout
        assert "--minimal" in result.stdout

    def test_lab_help(self):
        """sp lab --help should work."""
        result = runner.invoke(app, ["lab", "--help"])
        assert result.exit_code == 0
        assert "--port" in result.stdout
        assert "--no-browser" in result.stdout

    def test_status_runs(self):
        """sp status should run without error."""
        result = runner.invoke(app, ["status"])
        assert result.exit_code == 0
        assert "Home" in result.stdout
        assert "Environment" in result.stdout


class TestUI:
    """Test UI module."""

    def test_console_exists(self):
        """Console should be importable."""
        from sp.ui.console import console
        assert console is not None

    def test_brand_colors_defined(self):
        """Brand colors should be defined."""
        from sp.ui.console import (
            BRAND_PRIMARY,
            BRAND_SUCCESS,
            BRAND_ERROR,
        )
        assert BRAND_PRIMARY.startswith("#")
        assert BRAND_SUCCESS.startswith("#")
        assert BRAND_ERROR.startswith("#")
