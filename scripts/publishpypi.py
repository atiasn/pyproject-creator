from __future__ import annotations

import subprocess


def publish_package() -> None:
    subprocess.run(["poetry", "build", "-vvv"], check=True)
    result = subprocess.run(["poetry", "publish"], capture_output=True, text=True)
    if result.returncode != 0:
        if "HTTP Error 400: File already exists" not in result.stderr:
            print(result.stderr)
            raise SystemExit(result.returncode)
        else:
            print("\nThe version already exists, so there's no need to publish it again.")
            subprocess.run(["poetry", "version"])
    print("\n", result.stdout)


if __name__ == "__main__":
    publish_package()
