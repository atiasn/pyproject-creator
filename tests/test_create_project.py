import os
import subprocess

import click
import pytest
from click.testing import CliRunner

from pyproject_creator.cli import run_command, create_project, check_poetry_installed


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def mock_poetry_installed(monkeypatch):
    def mock_run(*args, **kwargs):
        if args[0][:2] == ["poetry", "--version"]:
            return subprocess.CompletedProcess(args, 0, stdout="Poetry 1.1.0\n")
        return subprocess.run(*args, **kwargs)

    monkeypatch.setattr(subprocess, "run", mock_run)


def test_validate_project_name():
    from pyproject_creator.cli import validate_project_name

    assert validate_project_name("valid_project_name") == "valid_project_name"
    assert validate_project_name("valid-project-name") == "valid-project-name"
    assert validate_project_name("validProjectName1234") == "validProjectName1234"

    with pytest.raises(click.BadParameter):
        validate_project_name("invalid project name")

    with pytest.raises(click.BadParameter):
        validate_project_name("-invalid-project-name")

    with pytest.raises(click.BadParameter):
        validate_project_name("_invalid_project_name")

    with pytest.raises(click.BadParameter):
        validate_project_name("invalid_project_name-")

    with pytest.raises(click.BadParameter):
        validate_project_name("invalid_project_name_")


def test_check_poetry_installed(mocker):
    mock_run = mocker.patch("subprocess.run")

    # Test Poetry installed
    mock_run.return_value.returncode = 0
    check_poetry_installed()
    mock_run.assert_called_once_with(
        ["poetry", "--version"],
        check=True,
        capture_output=True,
    )

    # Test Poetry not installed
    mock_run.side_effect = subprocess.CalledProcessError(1, "poetry")
    with pytest.raises(SystemExit):
        check_poetry_installed()


def test_run_command(mocker):
    mock_run = mocker.patch("subprocess.run")
    command = "echo test"

    # Test successful command execution
    mock_run.return_value.stdout = "test output"
    run_command(command)
    mock_run.assert_called_once_with(
        command,
        shell=True,
        check=True,
        capture_output=True,
        text=True,
    )

    # Test command failure
    mock_run.side_effect = subprocess.CalledProcessError(1, command)
    with pytest.raises(SystemExit):
        run_command(command)


def test_create_project(runner, mock_poetry_installed, monkeypatch, rootdir, project_names):
    os.chdir(rootdir)
    project_name = project_names[0]
    project_path = rootdir / project_name
    src_path = project_path / project_name.replace("-", "_")

    inputs = (
        "\n".join(
            [
                project_name,  # Project name
                "A tool to create Python project templates",  # Project description
                "Test Author <test@example.com>",  # Author name
                "3.11",  # Python version
                "",  # Project license
                "Y",  # Create logs package
                "Y",  # Create tests directory
                "Y",  # Create github actions
            ]
        )
        + "\n"
    )

    result = runner.invoke(create_project, input=inputs, color=True)
    if result.exit_code != 0:
        print("Output:\n", result.output)
        print("Exception:", result.exception)
    assert result.exit_code == 0
    print("Output:\n", result.output)

    # Verify directory structure
    assert project_path.exists()
    assert (src_path / "__init__.py").exists()
    assert (project_path / ".gitignore").exists()
    assert (project_path / ".pre-commit-config.yaml").exists()
    assert (project_path / ".cz.toml").exists()
    assert (src_path / "logs").exists()
    assert (project_path / "tests").exists()
    assert (project_path / "tests" / "test_sample.py").exists()
    assert (project_path / "README.md").exists()
    assert (project_path / ".github").exists()

    # Verify content of pyproject.toml
    assert (project_path / "pyproject.toml").exists()
    with open(project_path / "pyproject.toml") as f:
        content = f.read()
        assert "[tool.poetry]" in content
        assert f'name = "{project_name}"' in content
        assert 'description = "A tool to create Python project templates"' in content
        assert 'authors = ["Test Author <test@example.com>"]' in content
        assert 'python = "^3.11"' in content
        assert "[tool.poetry.dependencies]" in content
        assert "[tool.poetry.group.dev.dependencies]" in content
        assert "[tool.poetry.scripts]" not in content

    # Verify content of test_sample.py
    with open(project_path / "tests" / "test_sample.py") as f:
        content = f.read()
        assert "def test_sample()" in content


def test_create_project_without_tests_logs(runner, mock_poetry_installed, monkeypatch, rootdir, project_names):
    os.chdir(rootdir)
    project_name = project_names[1]
    project_path = rootdir / project_name
    src_path = project_path / project_name.replace("-", "_")

    inputs = (
        "\n".join(
            [
                project_name,  # Project name
                "A tool to create Python project templates",  # Project description
                "Test Author <test@example.com>",  # Author name
                "3.11",  # Python version
                "MIT",  # Project license
                "n",  # Create logs package
                "n",  # Create tests directory
                "n",  # Create github actions
            ]
        )
        + "\n"
    )

    result = runner.invoke(create_project, input=inputs, color=True)
    if result.exit_code != 0:
        print("Output:\n", result.output)
        print("Exception:", result.exception)
    assert result.exit_code == 0
    print("Output:\n", result.output)

    # Verify directory structure
    assert project_path.exists()
    assert (src_path / "__init__.py").exists()
    assert (project_path / ".gitignore").exists()
    assert (project_path / ".pre-commit-config.yaml").exists()
    assert (project_path / ".cz.toml").exists()
    assert not (src_path / "logs").exists()
    assert not (project_path / "tests").exists()
    assert not (project_path / "tests" / "test_sample.py").exists()
    assert (project_path / "README.md").exists()
    assert not (project_path / ".github").exists()

    # Verify content of pyproject.toml
    assert (project_path / "pyproject.toml").exists()
    with open(project_path / "pyproject.toml") as f:
        content = f.read()
        assert "[tool.poetry]" in content
        assert f'name = "{project_name}"' in content
        assert 'description = "A tool to create Python project templates"' in content
        assert 'authors = ["Test Author <test@example.com>"]' in content
        assert 'python = "^3.11"' in content
        assert "[tool.poetry.dependencies]" in content
        assert "[tool.poetry.group.dev.dependencies]" in content
        assert "MIT" in content
        assert "[tool.poetry.scripts]" not in content
        assert "pytest" not in content
        assert "loguru" not in content


if __name__ == "__main__":
    pytest.main()
