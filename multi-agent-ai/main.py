import subprocess
import sys
import time
import requests

BACKEND_URL = "http://127.0.0.1:8000/status"

def wait_for_backend():
    print("\nStarting Backend...\n")
    print("Waiting for backend to become ready...\n")

    while True:
        try:
            response = requests.get(
                BACKEND_URL,
                timeout=2
            )

            if response.status_code == 200:
                print("Backend is ready.\n")
                return

        except Exception:
            pass

        time.sleep(1)


def launch_web():
    backend = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "backend.app:app",
            "--reload"
        ]
    )

    try:
        wait_for_backend()

        frontend = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "streamlit",
                "run",
                "frontend/app.py"
            ]
        )

        print("Web Application Running.")
        print("Press CTRL+C to stop.\n")

        backend.wait()

    except KeyboardInterrupt:
        print("\nShutting down...\n")

        backend.terminate()
        frontend.terminate()

        backend.wait()
        frontend.wait()


def launch_cli():
    backend = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "backend.app:app",
            "--reload"
        ]
    )

    try:
        wait_for_backend()

        cli = subprocess.Popen(
            [
                sys.executable,
                "cli/app.py"
            ]
        )

        cli.wait()

    except KeyboardInterrupt:
        pass

    finally:
        print("\nShutting down...\n")

        backend.terminate()
        backend.wait()


def main():
    while True:
        print("=" * 55)
        print(" Multi-Agent AI Python Code Generator ")
        print("=" * 55)
        print()

        print("1. Launch Web Application")
        print("2. Launch CLI")
        print("3. Exit")
        print()

        choice = input(
            "Select option: "
        ).strip()

        if choice == "1":
            launch_web()
            break

        elif choice == "2":
            launch_cli()
            break

        elif choice == "3":
            print("\nGoodbye.\n")
            break

        else:
            print("\nInvalid option.\n")


if __name__ == "__main__":
    main()