# Pyproject Creator
![test](https://github.com/atiasn/pyproject-creator/actions/workflows/test.yml/badge.svg?branch=master)
[![PyPI - Version](https://img.shields.io/pypi/v/pyproject-creator)](https://pypi.org/project/pyproject-creator/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyproject-creator)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)

Pyproject Creator 是一个旨在简化创建 Python 项目过程的工具。它可以生成一些基础项目结构组件。

基础组件：
- Poetry 用于包管理
- pre-commit 用于代码格式化和 linting
- Commitizen 用于规范 git commit

可选组件
- 日志
- 使用 pytest 的测试
- GitHub Action 工作流等

## 安装

### 依赖项

项目依赖于以下库：
- **python 3.11+**: https://www.python.org/downloads/
- **poetry 1.8.3**+: https://python-poetry.org/docs/

### 源码安装

按照以下步骤进行源码安装：

1. **克隆仓库**：将 Pyproject Creator 仓库克隆到您的本地计算机。
   ```bash
   git clone https://github.com/atiasn/pyproject-creator.git
   cd pyproject-creator
   ```

2. **安装依赖项**：导航到仓库目录并运行以下命令以安装依赖项：

    ```bash
    poetry install --only main
    ```

3. **运行工具**：执行以下命令运行 Pyproject Creator：

    ```bash
    pypct
    ```

## 使用方法

运行 Pyproject Creator 后，将提示您提供有关项目的详细信息：

- **项目名称**：输入项目名称。名称应以字母或数字开头，仅包含字母、数字、下划线和连字符，但不应以下划线或连字符开头或结尾。

- **项目描述**：提供项目的简要描述，默认为空。

- **作者名称**：以指定的格式输入您的姓名和电子邮件地址，格式为：`"Your Name <your.email@example.com>"`。

- **Python 版本**：指定您想要为项目使用的 Python 版本，默认为 3.11。

- **项目许可证**：选择项目的许可证，默认为空。

- **创建日志包**：选择是否在项目中创建日志包，默认为是。

- **创建测试目录**：选择是否包含使用 pytest 的测试目录，默认为是。

- **创建 GitHub Action**：选择是否为您的项目的主分支创建 GitHub Action 工作流，默认为否。

- **是否发布到 PyPI**：选择是否将项目发布到 PyPI，默认为否。

提供必要的详细信息后，Pyproject Creator 将设置您的项目结构并配置必要的文件。按照屏幕上的说明完成流程。

## 贡献

欢迎为 Pyproject Creator 做出贡献！如果您遇到任何问题或有改进建议，请随时在 [GitHub 仓库](https://github.com/atiasn/pyproject-creator) 上提出问题或提交拉取请求。

## 许可证

本项目采用 MIT 许可证授权。有关详细信息，请参阅 [LICENSE](LICENSE) 文件。

---
