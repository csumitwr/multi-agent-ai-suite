import ast

class ImportValidator:
    @staticmethod
    def validate(code: str):

        try:
            ast.parse(code)

            return (
                True,
                "VALID"
            )

        except SyntaxError as error:
            return (
                False,
                f"SyntaxError: {error}"
            )