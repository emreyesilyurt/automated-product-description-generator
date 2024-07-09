import subprocess
import requests
import time

def find_free_port():
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]

def is_server_running(url):
    try:
        response = requests.get(f"{url}/health")
        return response.status_code == 200
    except requests.ConnectionError:
        return False

def start_fastapi_server():
    port = find_free_port()
    server_url = f"http://localhost:{port}"
    process = subprocess.Popen(["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", str(port)])
    # Check every second up to 10 seconds if the server is running
    for _ in range(10):
        time.sleep(1)
        if is_server_running(server_url):
            print(f"Server is up and running on {server_url}!")
            return process, server_url
    print("Server failed to start in time.")
    process.kill()  # Ensure no process hangs
    return None, None

def main():
    server_process, server_url = start_fastapi_server()
    if server_process:
        print(f"Server started at {server_url}. Performing actions while the server is running.")
        # Here, include any actions you'd like to perform while the server is up

        # Cleanup when done
        print("Stopping FastAPI server...")
        server_process.terminate()

if __name__ == "__main__":
    main()
