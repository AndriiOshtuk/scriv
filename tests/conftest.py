"""Fixture definitions."""

import pathlib
import traceback
from typing import Tuple

import pytest
from click.testing import CliRunner

from scriv.cli import cli as scriv_cli


class RunCommandFaker:
    """
    A fake implementation of run_command.

    Add results for commands with `add_fake`.
    """

    def __init__(self):
        """Make the faker."""
        self.in_out = {}

    def add_fake(self, cmd: str, result: Tuple[bool, str]) -> None:
        """If `cmd` is executed, return `result`."""
        self.in_out[cmd] = result

    def __call__(self, cmd: str) -> Tuple[bool, str]:
        """Do the faking!."""
        return self.in_out.get(cmd, (False, ""))


@pytest.fixture()
def fake_run_command(mocker):
    """Replace gitinfo.run_command with a fake."""
    frc = RunCommandFaker()
    mocker.patch("scriv.gitinfo.run_command", frc)
    return frc


@pytest.fixture()
def temp_dir(tmpdir) -> pathlib.Path:
    """Make and change into the tmpdir directory, as a Path."""
    tmpdir.chdir()
    return pathlib.Path(str(tmpdir))


@pytest.fixture()
def cli_invoke(temp_dir):
    """
    Produce a function to invoke the Scriv cli with click.CliRunner.

    The test will run in a temp directory.
    """

    def invoke(command, expect_ok=True):
        runner = CliRunner()
        result = runner.invoke(scriv_cli, command)
        print(result.output)
        if result.exception:
            traceback.print_exception(None, result.exception, result.exception.__traceback__)
        if expect_ok:
            assert result.exception is None
            assert result.exit_code == 0
        return result

    return invoke


@pytest.fixture()
def changelog_d(temp_dir) -> pathlib.Path:
    """Make a changelog.d directory, and return a Path() to it."""
    the_changelog_d = temp_dir / "changelog.d"
    the_changelog_d.mkdir()
    return the_changelog_d
