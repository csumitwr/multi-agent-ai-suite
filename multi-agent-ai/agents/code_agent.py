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
- Output only Python code.
- Do not explain anything.
- Do not use markdown.
- Do not use triple backticks.
- Do not use ```python.
- Do not repeat the user's request.
- Do not generate text outside the code.
- Do not ask questions.
- Do not use input().
- Do not require terminal interaction.
- Generate runnable Python code only.
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
        
        return response.strip()