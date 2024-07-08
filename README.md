# Automated Product Description Generator

This project is an automated product description generator using Huggingface models.

## Setup

### Prerequisites

1. Python 3.12 or higher
2. Virtualenv
3. Git

### Steps

1. **Clone the repository**

    ```sh
    git clone <repository_url>
    cd automated-product-description-generator
    ```

2. **Create a virtual environment**

    ```sh
    python3.12 -m venv .venv
    source .venv/bin/activate
    ```

3. **Install dependencies**

    ```sh
    pip install -r requirements.txt
    ```

4. **Download the Huggingface model**

    Ensure you have the model downloaded and placed in the appropriate directory.

5. **Run the application**

    ```sh
    python initialize_requests.py
    ```

## Usage

The application runs a FastAPI server that generates product descriptions. 

### Endpoints

- `GET /get_descriptions`: Retrieve generated product descriptions
- `POST /generate_description/`: Generate a product description for a given product

## Example

To generate a product description, send a POST request to `/generate_description/` with the product name.

```sh
curl -X POST "http://localhost:8001/generate_description/" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"product_name\": \"Apple iPhone 13\"}"
Stopping the Server
To stop the server, simply press CTRL+C in the terminal where the server is running.

Troubleshooting
If you encounter any issues, ensure that:

All dependencies are correctly installed.
The model is correctly placed and accessible.
The server is running and accessible.
License
This project is licensed under the MIT License.