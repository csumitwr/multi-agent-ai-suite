from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

MODELS_DIR = BASE_DIR / "models"
LOGS_DIR = BASE_DIR / "logs"
GENERATED_DIR = BASE_DIR / "generated"

CODE_MODEL_NAME = (
    "Qwen/Qwen2.5-Coder-1.5B-Instruct"
)

REVIEW_MODEL_NAME = (
    "Qwen/Qwen2.5-Coder-3B-Instruct"
)

MAX_RETRIES = 3
SANDBOX_TIMEOUT = 30

MAX_NEW_TOKENS = 512
TEMPERATURE = 0.1
DO_SAMPLE = False

ALLOWED_LIBRARIES = {
    "math",
    "random",
    "datetime",
    "time",
    "collections",
    "itertools",
    "functools",
    "heapq",
    "bisect",
    "re",
    "string",
    "json",
    "csv",
    "pathlib",
    "os",
    "sys",
    "numpy",
    "pandas",
    "matplotlib",
    "pygame",
    "requests",
    "bs4"
}

CODE_AGENT_LOG = LOGS_DIR / "code_agent.txt"
REVIEW_AGENT_LOG = LOGS_DIR / "review_agent.txt"
SANDBOX_LOG = LOGS_DIR / "sandbox.txt"

TEMP_SCRIPT = GENERATED_DIR / "temp_script.py"