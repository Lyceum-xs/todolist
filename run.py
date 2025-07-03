from src.gui import main_window
from src.app.db import create_tables
from src.app.main import run_backend
import threading
from urllib import response
import requests

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
    return ready

if __name__ == '__main__':
    backend_thread = threading.Thread(target = start_backend, daemon = True)
    backend_thread.start()
    
    if check_backend_ready():
        main_window.show_root()