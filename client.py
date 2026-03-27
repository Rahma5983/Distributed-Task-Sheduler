import requests
import threading

def send_task(i):
    response = requests.post(
        "http://127.0.0.1:8000/submit",
        json={"id": i}
    )
    print(response.json())

threads = []

for i in range(10):
    t = threading.Thread(target=send_task, args=(i,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()