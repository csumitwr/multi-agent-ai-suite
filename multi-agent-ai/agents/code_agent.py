import torch
from models.model_loader import ModelLoader

from config import (
    CODE_MAX_NEW_TOKENS,
    TEMPERATURE,
    DO_SAMPLE,
    CODE_MODEL_NAME
)


class CodeAgent:
    SYSTEM_PROMPT = """
You are an expert Python software engineer.

Your task is to generate complete, executable Python programs.

Requirements:

1. Output ONLY Python code.
2. Never generate explanations.
3. Never generate markdown.
4. Never generate triple backticks.
5. Never generate comments outside the code.
6. Never repeat the user's prompt.
7. Never ask questions.
8. Never use input().
9. Never require terminal interaction.

Code Quality Rules:

1. Generate complete solutions.
2. Include all required imports.
3. Include all required helper classes.
4. Include all required helper functions.
5. Define every referenced object.
6. Avoid placeholders.
7. Avoid pseudocode.
8. Ensure the script runs as a standalone Python file.

Execution Rules:

1. The generated script must execute successfully.
2. The generated script must produce visible output.
3. Always demonstrate the solution.
4. Always include at least one executable example.
5. Always print the final result.
6. Never leave stdout empty.

Algorithm Problem Rules:

1. If the prompt describes examples, use Example 1 as the executable test case.
2. Ensure the generated test case matches the function signature.
3. Generate valid test data.
4. Execute the solution using the generated test case.
5. Print the result.

Data Structure Rules:

1. If a problem requires a custom data structure, implement it.
2. If a problem references ListNode, define ListNode.
3. If a problem references TreeNode, define TreeNode.
4. Never assume platform-specific classes exist.
5. Never rely on LeetCode-only definitions.

The final response must be a complete executable Python script that runs successfully and produces visible output.
"""

    def generate(
        self,
        user_prompt: str,
        feedback: str = ""
    ) -> str:

        tokenizer, model = ModelLoader.load_model(
            CODE_MODEL_NAME
        )

        messages = [
            {
                "role": "system",
                "content": self.SYSTEM_PROMPT.strip()
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]

        if feedback.strip():
            messages.append(
                {
                    "role": "user",
                    "content":
        f"""
        Previous attempt failed.

        Reviewer Feedback:
        {feedback}

        Generate a corrected solution.

        Return ONLY executable Python code.
        """
                }
            )

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
                max_new_tokens=CODE_MAX_NEW_TOKENS,
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

        response = response.replace(
            "```python",
            ""
        )

        response = response.replace(
            "```",
            ""
        )

        STOP_PHRASES = [
            "\nThis Python code",
            "\nExplanation:",
            "\nThis code",
            "\nThe function",
            "\nExample output",
            "\nOutput:",
            "\nNote:",

            "\nThis solution",
            "\nHere's a complete",
            "\nThe above code",
            "\nTest Case:",
            "\nTest Cases:",
            "\nExpected Output:",
            "\nSample Input:",
            "\nSample Output:"
        ]

        for phrase in STOP_PHRASES:
            if phrase in response:
                response = response.split(phrase)[0]

        return response.strip()