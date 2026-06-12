import subprocess
import sys
from pathlib import Path

from config import (
    TEMP_SCRIPT,
    SANDBOX_TIMEOUT
)


class Sandbox:

    @staticmethod
    def execute(code: str):
        TEMP_SCRIPT.parent.mkdir(
            parents=True,
            exist_ok=True
        )
        TEMP_SCRIPT.write_text(
            code,
            encoding="utf-8"
        )

        try:
            result = subprocess.run(
                [sys.executable, str(TEMP_SCRIPT)],
                capture_output=True,
                text=True,
                timeout=SANDBOX_TIMEOUT
            )
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "timeout": False
            }

        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "stdout": "",
                "stderr": (
                    f"Execution exceeded "
                    f"{SANDBOX_TIMEOUT} seconds."
                ),
                "timeout": True
            }