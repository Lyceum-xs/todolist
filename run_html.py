import threading
import requests
import time
from http.server import SimpleHTTPRequestHandler, HTTPServer
from src.app.main import run_backend
import webbrowser
import os

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
            time.sleep(1)
    return ready

def start_http_server():
    os.chdir(os.path.join(os.path.dirname(__file__), 'html'))
    server = HTTPServer(('localhost', 3000), SimpleHTTPRequestHandler)
    print("Serving at http://localhost:3000")
    server.serve_forever()

def main():
    backend_thread = threading.Thread(target=start_backend, daemon=True)
    backend_thread.start()
    
    if check_backend_ready():
        http_thread = threading.Thread(target=start_http_server, daemon=True)
        http_thread.start()
        

        webbrowser.open('http://localhost:3000')

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down...")

if __name__ == '__main__':
    main()