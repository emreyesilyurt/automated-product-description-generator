import requests
import json
import subprocess
import time
import os
import sys

def is_server_running(url="http://localhost:8001/get_descriptions"):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
    except requests.ConnectionError:
        return False
    return False

def start_fastapi_server():
    process = subprocess.Popen([sys.executable, "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"])
    return process

def create_outputs_directory_and_file():
    outputs_dir = os.path.join(os.getcwd(), "outputs")
    descriptions_file = os.path.join(outputs_dir, "product_descriptions.json")
    
    if not os.path.exists(outputs_dir):
        os.makedirs(outputs_dir)
        print(f"Created directory {outputs_dir}")
    
    if not os.path.exists(descriptions_file):
        with open(descriptions_file, 'w') as f:
            json.dump({}, f)
        print(f"Created file {descriptions_file}")

def wait_for_server(url, timeout=30):
    start_time = time.time()
    while time.time() - start_time < timeout:
        if is_server_running(url):
            return True
        time.sleep(1)
    return False

def send_requests(file_path="products.json"):
    with open(file_path, "r") as f:
        products = json.load(f)["products"]

    for product_name in products:
        response = requests.post("http://localhost:8001/generate_description/", json={"product_name": product_name})
        if response.status_code == 200:
            print(f"Successfully processed {product_name}")
        else:
            print(f"Failed to process {product_name}")

def main():
    create_outputs_directory_and_file()

    if not is_server_running():
        print("Starting FastAPI server...")
        server_process = start_fastapi_server()
    else:
        server_process = None

    if wait_for_server("http://localhost:8001/get_descriptions"):
        send_requests()
    else:
        print("Failed to connect to the FastAPI server within the timeout period.")

    if server_process:
        print("Stopping FastAPI server...")
        server_process.terminate()

if __name__ == "__main__":
    main()
