# Pyproject Creator
![test](https://github.com/atiasn/pyproject-creator/actions/workflows/test.yml/badge.svg?branch=master)
[![PyPI - Version](https://img.shields.io/pypi/v/pyproject-creator)](https://pypi.org/project/pyproject-creator/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyproject-creator)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)


Pyproject Creator is a tool designed to simplify the process of creating Python projects. It generates some basic project structure components.

Basic components:

- Poetry for package management
- pre-commit for code formatting and linting
- Commitizen for standardized git commits

Optional components:

- Logging
- Testing with pytest
- GitHub Action workflows, etc.

## Installation

### Dependencies

The project depends on the following libraries:
- **python 3.11+**: https://www.python.org/downloads/
- **poetry 1.8.3+**: https://python-poetry.org/docs/

### Source Installation

Follow these steps for source installation:

1. **Clone the repository**: Clone the Pyproject Creator repository to your local computer.
   ```bash
   git clone https://github.com/atiasn/pyproject-creator.git
   cd pyproject-creator
   ```

2. **Install dependencies**: Navigate to the repository directory and run the following command to install dependencies:
   ```bash
   poetry install --only main
   ```

3. **Run the tool**: Execute the following command to run Pyproject Creator:
   ```bash
   pypct
   ```

## Usage

After running Pyproject Creator, you will be prompted to provide details about your project:

- **Project Name**: Enter the project name. The name should start with a letter or number, contain only letters, numbers, underscores, and hyphens, and should not start or end with an underscore or hyphen.

- **Project Description**: Provide a brief description of the project, which is empty by default.

- **Author Name**: Enter your name and email address in the specified format, as: "Your Name <your.email@example.com>".

- **Python Version**: Specify the Python version you want to use for the project, with 3.11 as the default.

- **Project License**: Choose the license for your project, which is empty by default.

- **Create Logging Package**: Choose whether to create a logging package in the project, with 'yes' as the default.

- **Create Test Directory**: Choose whether to include a test directory using pytest, with 'yes' as the default.

- **Create GitHub Action**: Choose whether to create a GitHub Action workflow for the main branch of your project, with 'no' as the default.

- **Publish to PyPI**: Choose whether to publish the project to PyPI, with 'no' as the default.

After providing the necessary details, Pyproject Creator will set up your project structure and configure the necessary files. Follow the on-screen instructions to complete the process.

## Contribution

Contributions to Pyproject Creator are welcome! If you encounter any issues or have suggestions for improvement, feel free to raise an issue or submit a pull request on the [GitHub repository](https://github.com/atiasn/pyproject-creator).

## License

This project is licensed under the MIT License. For more details, please refer to the [LICENSE](../LICENSE) file.
