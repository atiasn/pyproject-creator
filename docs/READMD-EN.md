# Pyproject Creator
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)

Pyproject Creator is a tool designed to simplify the process of creating Python projects. It sets up a project structure with essential components such as Poetry for package management, pre-commit for code formatting and linting, logs package, tests using pytest, and optionally, a GitHub Action workflow.

## Installation

To use Pyproject Creator, ensure you have Python installed on your system. Then, follow these steps:

1. **Clone the Repository**: Clone the Pyproject Creator repository to your local machine.

2. **Install Dependencies**: Navigate to the repository directory and run the following command to install dependencies:

    ```bash
    poetry install
    ```

3. **Set Up Environment**: Activate the virtual environment created by Poetry:

    ```bash
    poetry shell
    ```

4. **Run the Tool**: Execute the following command to run Pyproject Creator:

    ```bash
    pypct
    ```

## Usage

Upon running Pyproject Creator, you will be prompted to provide details about your project:

- **Project Name**: Enter a name for your project. The name should start with a letter or number and contain only letters, numbers, underscores, and hyphens, but should not start or end with underscores or hyphens.

- **Project Description**: Provide a brief description of your project.

- **Author Name**: Enter your name and email address in the specified format.

- **Python Version**: Specify the Python version you want to use for your project.

- **Project License**: Choose a license for your project.

- **Create Logs Package**: Choose whether to create a logs package within your project.

- **Create Tests Directory**: Choose whether to include a directory for tests using pytest.

- **Create GitHub Action**: Choose whether to create a GitHub Action workflow for the master branch of your project.

Once you have provided the necessary details, Pyproject Creator will set up your project structure and configure the necessary files. Follow the on-screen instructions to complete the process.

## Dependencies

Pyproject Creator relies on the following dependencies:

- **Poetry**: For Python package management.
- **Jinja2**: For template rendering.

## Contributing

Contributions to Pyproject Creator are welcome! If you encounter any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request on the [GitHub repository](https://github.com/atiasn/pyproject-creator).

## License

This project is licensed under the MIT License. See the [LICENSE](../LICENSE) file for details.

---
