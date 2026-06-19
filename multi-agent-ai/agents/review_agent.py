import torch
from models.model_loader import ModelLoader

from config import (
    MAX_NEW_TOKENS,
    TEMPERATURE,
    DO_SAMPLE,
    REVIEW_MODEL_NAME
)


class ReviewAgent:
    SYSTEM_PROMPT = """
You are a Python runtime error analysis engine.

Your task is to generate concise feedback for another AI model.

Rules:
1. Never suggest installing packages.
2. Never suggest using pip.
3. Never generate shell commands.
4. Never generate Python code.
5. Never generate markdown.
6. Never generate triple backticks.
7. Never recommend unsupported libraries.
8. Never talk directly to the user.
9. Generate feedback for another AI system.
10. Keep the response under five sentences.
"""

    @staticmethod
    def _preprocess_error(stderr: str):

        error = stderr.strip()

        if not error:
            return "SUCCESS"

        if "ModuleNotFoundError" in error:
            return (
                "The generated code uses an unavailable "
                "or unsupported module. "
                "Use only approved libraries."
            )

        if "SyntaxError" in error:
            return (
                "The generated code contains a syntax error. "
                "Generate syntactically valid Python."
            )

        if "NameError" in error:
            return (
                "The generated code references an undefined "
                "variable or function."
            )

        if "TypeError" in error:
            return (
                "The generated code contains a type mismatch."
            )

        if "ValueError" in error:
            return (
                "The generated code contains an invalid value."
            )

        if "IndexError" in error:
            return (
                "The generated code accesses an invalid index."
            )

        if "KeyError" in error:
            return (
                "The generated code accesses a missing key."
            )

        if "ZeroDivisionError" in error:
            return (
                "The generated code divides by zero."
            )

        return None

    @staticmethod
    def _sanitize(response: str):

        response = response.replace(
            "```python",
            ""
        )

        response = response.replace(
            "```",
            ""
        )

        response = response.replace(
            "bash",
            ""
        )

        response = response.replace(
            "pip install",
            "Do not use"
        )

        response = response.replace(
            "conda install",
            "Do not use"
        )

        return response.strip()

    def review(
        self,
        user_prompt: str,
        generated_code: str,
        stdout: str,
        stderr: str
    ) -> str:

        deterministic = self._preprocess_error(
            stderr
        )

        if deterministic is not None:
            return deterministic

        tokenizer, model = ModelLoader.load_model(
            REVIEW_MODEL_NAME
        )

        messages = [
            {
                "role": "system",
                "content": self.SYSTEM_PROMPT.strip()
            },
            {
                "role": "user",
                "content":
f"""
Original Request:
{user_prompt}

Generated Code:
{generated_code}

Sandbox Output:
{stdout}

Sandbox Error:
{stderr}
"""
            }
        ]

        prompt = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )

        inputs = tokenizer(
            prompt,
            return_tensors="pt"
        )

        inputs = {
            key: value.to(model.device)
            for key, value in inputs.items()
        }

        with torch.inference_mode():
            outputs = model.generate(
                **inputs,
                max_new_tokens=MAX_NEW_TOKENS,
                temperature=TEMPERATURE,
                do_sample=DO_SAMPLE,
                pad_token_id=tokenizer.eos_token_id,
                eos_token_id=tokenizer.eos_token_id
            )

        generated_tokens = outputs[
            0,
            inputs["input_ids"].shape[1]:
        ]

        response = tokenizer.decode(
            generated_tokens,
            skip_special_tokens=True
        )

        return self._sanitize(
            response
        )