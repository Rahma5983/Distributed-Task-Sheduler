from fastapi import FastAPI
import time
import random
from threading import Lock

app = FastAPI()

# Track current number of running tasks
current_load = 0

# Lock to prevent race conditions
lock = Lock()


@app.get("/")
def home():
    return {"message": "Worker is running"}


@app.get("/load")
def get_load():
    return {"load": current_load}


@app.post("/execute")
def execute_task(task: dict):
    global current_load

    # Simulate random failure (30% chance)
    if random.random() < 0.3:
        print(f"❌ Task {task['id']} failed due to simulated error")
        raise Exception("Simulated worker failure")

    # Safely increase load
    with lock:
        current_load += 1
        print(f"⚙️ Current Load Increased: {current_load}")

    try:
        print(f"📥 Received Task: {task}")

        # Simulate processing time
        time.sleep(2)

        result = f"Task {task['id']} completed successfully"

        print(f"✅ Completed Task: {task}")

        return {
            "status": "done",
            "result": result
        }

    finally:
        # Ensure load decreases even if something goes wrong
        with lock:
            current_load -= 1
            print(f"⬇️ Current Load Decreased: {current_load}")