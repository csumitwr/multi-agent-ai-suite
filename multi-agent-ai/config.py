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

MAX_RETRIES = 4
SANDBOX_TIMEOUT = 30

CODE_MAX_NEW_TOKENS = 512
REVIEW_MAX_NEW_TOKENS = 64
TEMPERATURE = 0.1
DO_SAMPLE = False

CODE_AGENT_LOG = LOGS_DIR / "code_agent.txt"
REVIEW_AGENT_LOG = LOGS_DIR / "review_agent.txt"
SANDBOX_LOG = LOGS_DIR / "sandbox.txt"

TEMP_SCRIPT = GENERATED_DIR / "temp_script.py"