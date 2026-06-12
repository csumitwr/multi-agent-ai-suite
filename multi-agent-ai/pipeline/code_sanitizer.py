import ast

class CodeSanitizer:
    STOP_PREFIXES = (
        "This code",
        "The above",
        "The following",
        "Explanation",
        "Output:",
        "Example Output",
        "In this code",
        "This function",
        "This program",
        "This script"
    )

    @classmethod
    def sanitize(
        cls,
        text: str
    ) -> str:
        if not text:
            return ""

        text = text.replace(
            "```python",
            ""
        )

        text = text.replace(
            "```",
            ""
        )

        text = text.strip()
        try:
            ast.parse(text)
            return text

        except SyntaxError:
            pass

        lines = text.splitlines()
        cleaned_lines = []

        for line in lines:
            stripped = line.strip()
            should_stop = False

            for prefix in cls.STOP_PREFIXES:
                if stripped.startswith(
                    prefix
                ):
                    should_stop = True
                    break

            if should_stop:
                break

            cleaned_lines.append(
                line
            )

        cleaned_code = "\n".join(
            cleaned_lines
        ).strip()

        try:
            ast.parse(
                cleaned_code
            )
            return cleaned_code
        
        except SyntaxError:
            return text.strip()

        return cleaned_code