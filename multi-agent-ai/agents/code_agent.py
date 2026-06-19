import torch
from models.model_loader import ModelLoader

from config import (
    MAX_NEW_TOKENS,
    TEMPERATURE,
    DO_SAMPLE,
    CODE_MODEL_NAME
)


class CodeAgent:
    SYSTEM_PROMPT = """
You are a Python code generation engine.

Return ONLY executable Python code.


Rules:
1. Output only Python code.
2. Do not output explanations.
3. Do not use markdown.
4. Do not use triple backticks.
5. Do not use ```python.
6. Do not repeat the user's request.
7. Do not generate text outside the code.
8. Do not ask questions.
9. Do not use input().
10. Do not require terminal interaction.
11. Generate runnable Python code only.
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
                    "role": "assistant",
                    "content": feedback
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
            "\nNote:"
        ]

        for phrase in STOP_PHRASES:
            if phrase in response:
                response = response.split(phrase)[0]

        return response.strip()