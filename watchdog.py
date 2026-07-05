import os
import time

while True:

    status = os.system("curl -s http://localhost:5000/health")

    if status != 0:
        print("RESTARTING BOT...")
        os.system("python app.py")

    time.sleep(10)
