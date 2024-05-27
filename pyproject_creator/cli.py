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


def prompt_project_details() -> tuple[Path, Path]:
    """Prompt the user for project details and create the project directory structure."""
    for _ in range(5):
        project_name: str = click.prompt("Project name", type=str)
        try:
            validate_project_name(project_name)
        except click.BadParameter as e:
            click.echo(f"Error: {e}")
            continue

        project_path: Path = Path(project_name).resolve()
        if project_path.exists():
            click.echo(f"Error: {project_name} directory already exists.")
            continue

        project_path.mkdir()
        os.chdir(project_path)

        src_path: Path = project_path / project_name.replace("-", "_")
        src_path.mkdir()
        create_file(src_path / "__init__.py")
        return project_path, src_path

    click.echo("Too many attempts. Exiting.")
    exit(1)


@click.command()  # type: ignore
def create_project() -> None:
    """Create a new Python project with Poetry, pre-commit, logs, tests."""

    # Prompt for project details
    project_path, src_path = prompt_project_details()

    description: str = click.prompt("Project description", default="", type=str)
    author: str = click.prompt(
        "Author name", default="Your Name <your.email@example.com>", type=str
    )
    python_version: str = click.prompt("Python version", default="3.11", type=str)
    project_license: str = click.prompt("Project license", default="", type=str)
    need_logs: str = click.prompt("Create logs package? (Y/n)", default="Y", type=str)
    need_tests: str = click.prompt("Create tests(pytest) directory? (Y/n)", default="Y", type=str)
    github_action: str = click.prompt(
        "Create github action for project(master branch)? (Y/n)", default="n", type=str
    )

    # Copy template files
    template_path: Path = BASE_PATH / "template"
    shutil.copy(template_path / ".gitignore", project_path / ".gitignore")
    shutil.copy(
        template_path / ".pre-commit-config.yaml",
        project_path / ".pre-commit-config.yaml",
    )
    shutil.copy(template_path / ".cz.toml", project_path / ".cz.toml")
    if need_logs.lower() == "y":
        shutil.copytree(template_path / "logs", project_path / src_path / "logs")
    if need_tests.lower() == "y":
        shutil.copytree(template_path / "tests", project_path / "tests")
    if github_action.lower() == "y":
        shutil.copytree(template_path / "github_action", project_path / ".github")

    # create pyproject.toml
    shutil.copy(template_path / "pyproject.template", project_path / "pyproject.toml")
    with open(project_path / "pyproject.toml") as _file:
        poetry_config = _file.read()
    template = jinja2.Template(poetry_config)
    rendered_toml = template.render(
        project_name=project_path.name,
        project_description=description,
        author=author,
        python_version=python_version.strip("^"),
        project_license=project_license,
        need_tests=need_tests.lower(),
        need_logs=need_logs.lower(),
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
