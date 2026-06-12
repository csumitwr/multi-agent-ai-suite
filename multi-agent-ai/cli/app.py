import requests

API_URL = "http://127.0.0.1:8000"

def main():
    print()
    print("=" * 60)
    print(" Multi-Agent AI Python Code Generator ")
    print("=" * 60)
    print()

    prompt = input(
        "Enter your prompt:\n\n> "
    ).strip()

    if not prompt:
        print()
        print("No prompt entered.")
        return

    print()
    print("Generating...")
    print()

    try:
        response = requests.post(
            f"{API_URL}/generate",
            json={
                "prompt": prompt
            },
            timeout=300
        )

        response.raise_for_status()

        result = response.json()

    except Exception as error:
        print(
            f"Error: {error}"
        )

        return

    print("-" * 60)
    print("Generated Python Code")
    print("-" * 60)
    print()

    print(
        result["code"]
    )

    print()
    print("-" * 60)

    print(
        f"Success : {result['success']}"
    )

    print(
        f"Attempts: {result['attempts']}"
    )

    print()

    print("STDOUT")
    print("-" * 60)

    print(
        result["stdout"]
        if result["stdout"]
        else "(empty)"
    )

    print()

    print("STDERR")
    print("-" * 60)

    print(
        result["stderr"]
        if result["stderr"]
        else "(empty)"
    )

    print()

if __name__ == "__main__":
    main()