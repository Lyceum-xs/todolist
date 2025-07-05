import threading
import requests
import time
from src.gui import main_window
from src.app.db import create_tables
from src.app.main import run_backend

def start_backend():
    run_backend()


def check_backend_ready():
    url = "http://127.0.0.1:8000/health"

    ready = False
    while not ready:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                ready = True
        except requests.exceptions.RequestException:
            ready = False
        time.sleep(1)
    return ready

def main():
    backend_thread = threading.Thread(target = start_backend, daemon = True)
    backend_thread.start()

    if check_backend_ready():
        main_window.show_root()

if __name__ == '__main__':
    main()