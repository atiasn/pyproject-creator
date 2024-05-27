import subprocess


def check_cuda() -> bool:
    try:
        # Check if CUDA is available
        subprocess.check_output(["nvcc", "--version"])
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def install(env: str = "dev") -> None:
    if env == "dev":
        install_cmd = ["poetry", "install"]
    elif env == "prod":
        install_cmd = ["poetry", "install", "--without", "dev"]
    else:
        raise Exception("Invalid env option, please use 'dev' or 'prod'")

    if check_cuda():
        print("CUDA detected. Installing paddlepaddle-gpu...\n")
        install_cmd.extend(["--with", "gpu"])
    else:
        print("CUDA not detected. Installing paddlepaddle (CPU version)...\n")
        install_cmd.extend(["--with", "cpu"])
    print(f"Installing command: {' '.join(install_cmd)}\n")
    subprocess.check_call(install_cmd)


def install_dev() -> None:
    install()


def install_prod() -> None:
    install("prod")
