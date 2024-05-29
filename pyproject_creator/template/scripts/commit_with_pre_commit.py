from __future__ import annotations

import subprocess


def run_pre_commit() -> int:
    """Run pre-commit checks and return the result."""
    result = subprocess.run(
        ["pre-commit", "run", "--all-files", "-vvv"], capture_output=True, text=True
    )
    return result.returncode


if __name__ == "__main__":
    run_pre_commit()
