import time
import subprocess


def start_bot():

    while True:

        try:
            print("Starting bot...")

            subprocess.run(
                ["python", "app.py"],
                check=True,
            )

        except Exception as e:

            print(f"Bot crashed: {e}")
            print("Restarting in 5 seconds...")

            time.sleep(5)


if __name__ == "__main__":
    start_bot()
