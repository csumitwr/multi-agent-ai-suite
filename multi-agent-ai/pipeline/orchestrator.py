from models.model_loader import ModelLoader
from agents.code_agent import CodeAgent
from agents.review_agent import ReviewAgent

from pipeline.code_sanitizer import CodeSanitizer
from pipeline.import_validator import ImportValidator
from pipeline.sandbox import Sandbox
from pipeline.logger import PipelineLogger

from config import MAX_RETRIES


class Orchestrator:

    def __init__(self):
        self.code_agent = CodeAgent()
        self.review_agent = ReviewAgent()

    def run(
        self,
        user_prompt: str
    ):

        PipelineLogger.initialize()
        PipelineLogger.clear_logs()

        feedback = ""

        sandbox_result = {
            "stdout": "",
            "stderr": "",
            "success": False
        }

        generated_code = ""

        for attempt in range(
            1,
            MAX_RETRIES + 1
        ):

            generated_code = self.code_agent.generate(
                user_prompt=user_prompt,
                feedback=feedback
            )

            generated_code = CodeSanitizer.sanitize(
                generated_code
            )

            PipelineLogger.log_code_agent(
                f"Attempt: {attempt}\n\n"
                f"User Prompt:\n"
                f"{user_prompt}\n\n"
                f"Reviewer Feedback:\n"
                f"{feedback}\n\n"
                f"Generated Code:\n"
                f"{generated_code}"
            )

            valid, validation_result = (
                ImportValidator.validate(
                    generated_code
                )
            )

            if not valid:

                feedback = self.review_agent.review(
                    user_prompt=user_prompt,
                    generated_code=generated_code,
                    stdout="",
                    stderr=validation_result
                )

                PipelineLogger.log_review_agent(
                    feedback
                )

                sandbox_result = {
                    "stdout": "",
                    "stderr": validation_result,
                    "success": False
                }

                continue

            sandbox_result = Sandbox.execute(
                generated_code
            )

            PipelineLogger.log_sandbox(
                f"Attempt: {attempt}\n\n"
                f"STDOUT:\n"
                f"{sandbox_result['stdout']}\n\n"
                f"STDERR:\n"
                f"{sandbox_result['stderr']}"
            )

            if sandbox_result["success"]:
                if not sandbox_result["stdout"].strip():
                    feedback = self.review_agent.review(
                        user_prompt=user_prompt,
                        generated_code=generated_code,
                        stdout="",
                        stderr=""
                    )

                    PipelineLogger.log_review_agent(
                        feedback
                    )

                    continue

                PipelineLogger.log_review_agent(
                    "SUCCESS"
                )

                ModelLoader.unload_model()

                return {
                    "success": True,
                    "code": generated_code,
                    "stdout": sandbox_result[
                        "stdout"
                    ],
                    "stderr": "",
                    "attempts": attempt
                }

            feedback = self.review_agent.review(
                user_prompt=user_prompt,
                generated_code=generated_code,
                stdout=sandbox_result[
                    "stdout"
                ],
                stderr=sandbox_result[
                    "stderr"
                ]
            )

            PipelineLogger.log_review_agent(
                feedback
            )

        ModelLoader.unload_model()

        return {
            "success": False,
            "code": generated_code,
            "stdout": sandbox_result.get(
                "stdout",
                ""
            ),
            "stderr": sandbox_result.get(
                "stderr",
                feedback
            ),
            "attempts": MAX_RETRIES
        }