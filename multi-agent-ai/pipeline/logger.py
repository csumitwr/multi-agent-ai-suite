from datetime import datetime

from config import (
    LOGS_DIR,
    CODE_AGENT_LOG,
    REVIEW_AGENT_LOG,
    SANDBOX_LOG
)


class PipelineLogger:

    @staticmethod
    def initialize():
        LOGS_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        for log_file in (
            CODE_AGENT_LOG,
            REVIEW_AGENT_LOG,
            SANDBOX_LOG
        ):
            if not log_file.exists():
                log_file.write_text(
                    "",
                    encoding="utf-8"
                )

    @staticmethod
    def clear_logs():
        LOGS_DIR.mkdir(
            parents=True,
            exist_ok=True
        )
        for log_file in (
            CODE_AGENT_LOG,
            REVIEW_AGENT_LOG,
            SANDBOX_LOG
        ):
            log_file.write_text(
                "",
                encoding="utf-8"
            )

    @staticmethod
    def _write(
        log_path,
        title,
        message
    ):
        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        with open(
            log_path,
            "a",
            encoding="utf-8"
        ) as file:
            file.write(
                f"[{timestamp}]\n"
            )
            file.write(
                f"{title}\n"
            )
            file.write(
                f"{message}\n"
            )
            file.write(
                "\n"
                + "-" * 60
                + "\n\n"
            )

    @classmethod
    def log_code_agent(
        cls,
        message
    ):
        
        cls._write(
            CODE_AGENT_LOG,
            "CODE AGENT",
            message
        )

    @classmethod
    def log_review_agent(
        cls,
        message
    ):
        
        cls._write(
            REVIEW_AGENT_LOG,
            "REVIEW AGENT",
            message
        )

    @classmethod
    def log_sandbox(
        cls,
        message
    ):

        cls._write(
            SANDBOX_LOG,
            "SANDBOX",
            message
        )