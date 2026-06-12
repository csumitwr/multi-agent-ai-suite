import ast
from config import ALLOWED_LIBRARIES

class ImportValidator:

    @staticmethod
    def validate(code: str):
        try:
            tree = ast.parse(code)
        except SyntaxError as error:
            return False, f"SyntaxError: {error}"

        imported_libraries = set()

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imported_libraries.add(
                        alias.name.split(".")[0]
                    )

            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imported_libraries.add(
                        node.module.split(".")[0]
                    )

        unsupported = imported_libraries - ALLOWED_LIBRARIES

        if unsupported:
            return (
                False,
                f"Unsupported Library Request: "
                f"{', '.join(sorted(unsupported))}"
            )
        
        return True, imported_libraries