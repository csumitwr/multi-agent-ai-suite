import ast

class CodeSanitizer:
    STOP_PREFIXES = (
        "This code",
        "This Python",
        "This program",
        "This script",
        "The above",
        "The following",
        "Explanation",
        "Output:",
        "Expected Output",
        "Example Output",
        "Sample Output",
        "Sample Input",
        "Input:",
        "Expected:",
        "Note:",
        "Here's",
        "When you run",
        "The algorithm",
        "The function",
        "This solution",
        "Test Case",
        "Test Cases"
    )

    @classmethod
    def sanitize(cls, text: str) -> str:

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

        lines = text.splitlines()
        cleaned_lines = []

        for line in lines:

            stripped = line.strip()

            stop = False

            for prefix in cls.STOP_PREFIXES:

                if stripped.startswith(prefix):
                    stop = True
                    break

            if stop:
                break

            cleaned_lines.append(line)

        cleaned_code = (
            "\n".join(cleaned_lines)
            .rstrip()
        )

        try:
            ast.parse(cleaned_code)
            return cleaned_code

        except Exception:

            # Last resort:
            # Keep removing lines from bottom
            # until valid Python remains

            lines = cleaned_lines[:]

            while lines:

                try:

                    candidate = "\n".join(lines)

                    ast.parse(candidate)

                    return candidate.strip()

                except Exception:

                    lines.pop()

            return ""