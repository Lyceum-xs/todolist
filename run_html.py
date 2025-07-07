import threading
import requests
import time
from http.server import SimpleHTTPRequestHandler, HTTPServer
from src.app.main import run_backend
import webbrowser
import os
import sys
from pathlib import Path
import importlib.resources

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

def get_html_dir():
    """智能获取HTML目录路径"""
    # 尝试开发模式路径（直接运行）
    dev_path = Path(__file__).parent / "html"
    if dev_path.exists():
        return str(dev_path)
    
    # 尝试打包后的安装路径
    try:
        # 方法1：Python包资源
        with importlib.resources.path('todolist_app.html', 'index.html') as p:
            return str(p.parent)
    except:
        try:
            # 方法2：系统共享目录
            if sys.platform == "win32":
                program_data = os.environ.get("ProgramData", "")
                install_path = Path(program_data) / "todolist/html"
            else:
                install_path = Path("/usr/share/todolist/html")
            
            if install_path.exists():
                return str(install_path)
        except:
            pass
    
    # 最终回退方案：当前工作目录
    fallback_path = Path.cwd() / "html"
    if fallback_path.exists():
        return str(fallback_path)
    
    raise FileNotFoundError(
        "无法找到HTML目录，请检查：\n"
        "1. 开发模式：确保html/目录与run_html.py同级\n"
        "2. 安装模式：确认已正确打包HTML资源"
    )

def start_http_server():
    try:
        html_dir = get_html_dir()
        print(f"[INFO] Serving HTML from: {html_dir}")
        os.chdir(html_dir)
        server = HTTPServer(('localhost', 3000), SimpleHTTPRequestHandler)
        print("[INFO] HTTP server started at http://localhost:3000")
        server.serve_forever()
    except Exception as e:
        print(f"[ERROR] Failed to start HTTP server: {str(e)}")
        raise

def main():
    # 启动后端服务
    backend_thread = threading.Thread(target=start_backend, daemon=True)
    backend_thread.start()
    
    # 等待后端就绪
    if check_backend_ready():
        # 启动HTTP服务器
        http_thread = threading.Thread(target=start_http_server, daemon=True)
        http_thread.start()
        
        # 打开浏览器
        webbrowser.open('http://localhost:3000')
        print("[INFO] Application started successfully!")
    else:
        print("[ERROR] Backend service failed to start")
        return

    # 主线程保持运行
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[INFO] Shutting down server...")

if __name__ == '__main__':
    main()