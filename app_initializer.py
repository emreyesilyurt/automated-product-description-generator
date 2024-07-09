import requests
import json
import subprocess
import time

def is_server_running(url="http://localhost:8000/health"):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
    except requests.ConnectionError:
        return False
    return False

def start_fastapi_server():
    process = subprocess.Popen(["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"])
    time.sleep(5)  # Wait for the server to start
    return process

def send_requests(file_path="products.json"):
    with open(file_path, "r") as f:
        products = json.load(f)["products"]

    for product_name in products:
        for _ in range(5):  # Retry mechanism
            try:
                response = requests.post("http://localhost:8000/generate_description/", json={"product_name": product_name})
                if response.status_code == 200:
                    print(f"Successfully processed {product_name}")
                    break
                else:
                    print(f"Failed to process {product_name}")
            except requests.ConnectionError:
                print(f"Server not ready, retrying for {product_name}...")
                time.sleep(2)
        else:
            print(f"Failed to process {product_name} after multiple attempts")

def main():
    if not is_server_running():
        print("Starting FastAPI server...")
        server_process = start_fastapi_server()
    else:
        server_process = None

    # Wait until the server is up and running
    while not is_server_running():
        print("Waiting for server to be ready...")
        time.sleep(10)
    print("Server is up and running!")

    send_requests()

    if server_process:
        print("Stopping FastAPI server...")
        server_process.terminate()

if __name__ == "__main__":
    main()
