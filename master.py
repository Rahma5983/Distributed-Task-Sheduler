from fastapi import FastAPI
import requests
import threading
import time

app = FastAPI()

workers = ["http://127.0.0.1:8001", "http://127.0.0.1:8002"]

task_queue = []
lock = threading.Lock()


def get_worker_load(worker):
    try:
        response = requests.get(f"{worker}/load")
        return response.json()["load"]
    except:
        return float("inf")


def process_tasks():
    while True:
        if task_queue:
            with lock:
                task = task_queue.pop(0)

            # sort workers by load
            loads = [(w, get_worker_load(w)) for w in workers]
            sorted_workers = sorted(loads, key=lambda x: x[1])

            # try workers
            for worker, load in sorted_workers:
                try:
                    print(f"🚀 Assigning Task {task} to {worker}")

                    requests.post(
                        f"{worker}/execute",
                        json=task,
                        timeout=3
                    )
                    break

                except:
                    print(f"❌ Worker {worker} failed, retrying...")

        time.sleep(1)


# Start background thread
threading.Thread(target=process_tasks, daemon=True).start()


@app.post("/submit")
def submit_task(task: dict):
    with lock:
        task_queue.append(task)

    return {"status": "queued", "task": task}