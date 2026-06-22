import torch
from models.model_loader import ModelLoader

from config import (
    REVIEW_MAX_NEW_TOKENS,
    TEMPERATURE,
    DO_SAMPLE,
    REVIEW_MODEL_NAME
)


class ReviewAgent:

    SYSTEM_PROMPT = """
You are a Python code review agent.

Your job is to provide concise feedback to another AI code generator.

Review for:

- Syntax errors
- Runtime errors
- Missing imports
- Missing classes
- Missing functions
- Undefined variables
- Invalid test cases
- Missing executable examples
- Missing print statements
- Empty output
- Non-executable code

Rules:

1. Never generate code.
2. Never rewrite the solution.
3. Never generate examples.
4. Never explain algorithms.
5. Never teach Python.
6. Never use markdown.
7. Never use bullet points.
8. Never provide step-by-step explanations.
9. Never describe expected output.
10. Keep feedback under 30 words.

Response Format:

Issue: <one sentence>

Fix: <one sentence>

Only identify the most important issue.

Good Example:

Issue: The solution defines the function but never executes it.

Fix: Add a runnable test case and print the result.

Bad Example:

- Long explanations
- Code snippets
- Tutorials
- Multiple paragraphs
- Rewritten solutions

Your response must contain only:

Issue: ...
Fix: ...
"""

    @staticmethod
    def _preprocess_error(stderr: str):

        error = stderr.strip()

        if not error:
            return None

        if "ModuleNotFoundError" in error:
            return (
                "The generated code uses an unavailable "
                "or unsupported module."
            )

        if "SyntaxError" in error:
            return (
                "The generated output contains text that "
                "is not valid Python. Return only "
                "executable Python code."
            )

        if "NameError" in error:
            return (
                "The generated code references undefined "
                "objects. Ensure all classes, functions "
                "and variables are defined."
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

        review_context = ""

        if deterministic is not None:
            review_context = deterministic

        if (
            not stderr.strip()
            and not stdout.strip()
        ):
            review_context = (
                "The generated code executed successfully "
                "but produced no output. The solution "
                "was not demonstrated."
            )

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

Detected Issue:
{review_context}

Return feedback in this exact format:

Issue: <one sentence>
Fix: <one sentence>

Rules:
- Maximum 30 words.
- Never generate code.
- Never generate examples.
- Never explain algorithms.
- Never write more than two lines.
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
                max_new_tokens=REVIEW_MAX_NEW_TOKENS,
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