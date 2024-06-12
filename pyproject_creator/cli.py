from __future__ import annotations

import os
import re
import shutil
import subprocess
from pathlib import Path

import click
import jinja2


BASE_PATH: Path = Path(__file__).parent.resolve()


def validate_project_name(value: str) -> str:
    """Validate the project name to ensure it meets the required criteria."""
    if not re.match(r"^[a-zA-Z0-9][a-zA-Z0-9_-]*$", value):
        raise click.BadParameter(
            "Project name should start with a letter or number and contain only letters, numbers, "
            "underscores, and hyphens, but not start with underscores or hyphens."
        )
    if value.endswith("-") or value.endswith("_"):
        raise click.BadParameter("Project name should not end with a hyphen or underscore.")
    return value


def check_poetry_installed() -> None:
    """Check if Poetry is installed, otherwise prompt the user to install it."""
    try:
        subprocess.run(["poetry", "--version"], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        click.echo("Poetry is not installed.")
        click.echo(
            "Please install Poetry by following the instructions at https://python-poetry.org/docs/#installation"
        )
        click.echo(
            "Installation command: `curl -sSL https://install.python-poetry.org | python3 -`"
        )
        exit(1)


def run_command(command: str) -> None:
    """Run a shell command and handle any errors."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True,
        )
        click.echo(result.stdout)
    except subprocess.CalledProcessError as e:
        if e.stderr:
            click.echo(f"Error: {e.stderr}")
        exit(1)


def create_file(file_path: Path | str, content: str | None = None) -> None:
    """Create a file with the specified content."""
    if content is None:
        content = ""
    with open(file_path, "w") as f:
        f.write(content)


def prompt_project_details(value: str) -> tuple[Path, Path]:
    """Prompt the user for project details and create the project directory structure."""
    validate_project_name(value)
    project_path: Path = Path(value).resolve()
    if project_path.exists():
        click.echo(f"Error: {value} directory already exists.")
        exit(1)

    project_path.mkdir()
    os.chdir(project_path)

    src_path: Path = project_path / value.replace("-", "_")
    src_path.mkdir()
    create_file(src_path / "__init__.py")
    return project_path, src_path


@click.command()  # type: ignore
@click.option("--name", prompt="Project name", required=True, help="Enter the project name.")
@click.option(
    "--description",
    prompt="Project description",
    default="",
    help="Provide a brief description of the project.",
)
@click.option(
    "--author",
    prompt="Author name",
    default="Your Name <your.email@example.com>",
    help="Enter the author's name and email.",
)
@click.option(
    "--python-version",
    prompt="Python version",
    default="3.11",
    help="Specify the Python version to use.",
)
@click.option(
    "--project-license",
    prompt="Project license",
    default="",
    help="Specify the license for the project.",
)
@click.option(
    "--pypi-package",
    prompt="Create pypi package?",
    type=bool,
    is_flag=True,
    default=False,
    help="Do you want to create a PyPI package? Enter 'y' or 'N'.",
)
@click.option(
    "--logs",
    "--need-logs",
    prompt="Create logs package?",
    type=bool,
    is_flag=True,
    default=True,
    help="Do you need a logs package? Enter 'Y' or 'n'.",
)
@click.option(
    "--tests",
    "--need-tests",
    prompt="Create tests(pytest) directory?",
    type=bool,
    is_flag=True,
    default=True,
    help="Do you need a tests directory for pytest? Enter 'Y' or 'n'.",
)
@click.option(
    "--github-action",
    prompt="Create github action for project(master branch)?",
    type=bool,
    is_flag=True,
    default=False,
    help="Do you want to create a GitHub action for the master branch? Enter 'y' or 'N'.",
)
def create_project(
    name: str,
    description,
    author,
    python_version,
    project_license,
    logs,
    tests,
    github_action,
    pypi_package,
) -> None:
    """Create a new Python project with Poetry, pre-commit, logs, tests."""

    # Prompt for project details
    project_path, src_path = prompt_project_details(name)

    # Copy template files
    template_path: Path = BASE_PATH / "template"
    shutil.copy(template_path / ".gitignore", project_path / ".gitignore")
    shutil.copy(
        template_path / ".pre-commit-config.yaml",
        project_path / ".pre-commit-config.yaml",
    )
    shutil.copy(template_path / ".cz.toml", project_path / ".cz.toml")
    shutil.copytree(template_path / "scripts", project_path / "scripts")
    if logs:
        shutil.copytree(template_path / "logs", project_path / src_path / "logs")
    if logs:
        shutil.copytree(template_path / "tests", project_path / "tests")
    if github_action:
        _github_action_path = project_path / ".github"
        _github_action_path.mkdir(exist_ok=True, parents=True)
        shutil.copy(
            template_path / "github_action" / "workflows" / "test.yml",
            _github_action_path / "test.yml",
        )
        shutil.copy(
            template_path / "github_action" / "workflows" / "bumpversion.yml",
            _github_action_path / "bumpversion.yml",
        )
        if pypi_package:
            shutil.copy(
                template_path / "github_action" / "workflows" / "pythonpublish.yml",
                _github_action_path / "pythonpublish.yml",
            )

    # create pyproject.toml
    shutil.copy(template_path / "pyproject.template", project_path / "pyproject.toml")
    with open(project_path / "pyproject.toml") as _file:
        poetry_config = _file.read()
    template = jinja2.Template(poetry_config)
    rendered_toml = template.render(
        project_name=project_path.name,
        project_description=description,
        author=author,
        is_pypi_package="true" if pypi_package else "false",
        python_version=python_version.strip("^"),
        project_license=project_license,
        need_tests=tests,
        need_logs=tests,
        project_src_name=src_path.name,
    )

    with open("pyproject.toml", "w") as file:
        file.write(rendered_toml)

    # Create README.md
    create_file("README.md", f"# {project_path.name}\n")

    # Check if Poetry is installed
    check_poetry_installed()
    click.echo("\n")
    click.echo("Project created successfully!")
    click.echo(f"Next steps: `cd {project_path.name}` and `poetry install`, then start coding!")


if __name__ == "__main__":
    create_project()
