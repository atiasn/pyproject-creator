# Pyproject Creator

Pyproject Creator 是一个旨在简化创建 Python 项目过程的工具。它设置了一个包含必要组件的项目结构，如 Poetry 用于包管理、pre-commit 用于代码格式化和 linting、日志包、使用 pytest 的测试，并且可选地，GitHub Action 工作流。

## 安装

要使用 Pyproject Creator，请确保您的系统上已安装了 Python。然后，按照以下步骤操作：

1. **克隆仓库**：将 Pyproject Creator 仓库克隆到您的本地计算机。

2. **安装依赖项**：导航到仓库目录并运行以下命令以安装依赖项：

    ```bash
    poetry install
    ```

3. **设置环境**：激活 Poetry 创建的虚拟环境：

    ```bash
    poetry shell
    ```

4. **运行工具**：执行以下命令运行 Pyproject Creator：

    ```bash
    pypct
    ```

## 使用方法

运行 Pyproject Creator 后，将提示您提供有关项目的详细信息：

- **项目名称**：输入项目名称。名称应以字母或数字开头，仅包含字母、数字、下划线和连字符，但不应以下划线或连字符开头或结尾。

- **项目描述**：提供项目的简要描述。

- **作者名称**：以指定的格式输入您的姓名和电子邮件地址。

- **Python 版本**：指定您想要为项目使用的 Python 版本。

- **项目许可证**：选择项目的许可证。

- **创建日志包**：选择是否在项目中创建日志包。

- **创建测试目录**：选择是否包含使用 pytest 的测试目录。

- **创建 GitHub Action**：选择是否为您的项目的主分支创建 GitHub Action 工作流。

提供必要的详细信息后，Pyproject Creator 将设置您的项目结构并配置必要的文件。按照屏幕上的说明完成流程。

## 依赖项

Pyproject Creator 依赖于以下库：

- **Poetry**：用于 Python 包管理。
- **Jinja2**：用于模板渲染。

## 贡献

欢迎为 Pyproject Creator 做出贡献！如果您遇到任何问题或有改进建议，请随时在 [GitHub 仓库](https://github.com/atiasn/pyproject-creator) 上提出问题或提交拉取请求。

## 许可证

本项目采用 MIT 许可证授权。有关详细信息，请参阅 [LICENSE](LICENSE) 文件。

---
