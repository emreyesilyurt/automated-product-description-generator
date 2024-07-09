# Product Overview Bot

Product Overview Bot leverages AI to generate high-level product overviews. This tool uses language models to create concise, informative summaries of products, making it easier to understand key features and benefits quickly. Easily deployable with Docker and equipped with a FastAPI backend, Product Overview Bot ensures efficient and automated product overview generation.

## Table of Contents

- [Features](#features)
- [Setup](#setup)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [Running the Server](#running-the-server)
  - [Generating Descriptions](#generating-descriptions)
  - [Checking Server Health](#checking-server-health)
- [Development](#development)
  - [Project Structure](#project-structure)
  - [Running Tests](#running-tests)
- [Contributing](#contributing)
- [License](#license)

## Features

- Generate product descriptions using language models.
- Verify descriptions to ensure they do not contain marketing qualifiers.
- Easily deployable with Docker.
- Simple health check endpoint for server status monitoring.

## Setup

### Prerequisites

Ensure you have the following installed:

- Python 3.8 or higher
- Docker
- Docker Compose

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/automated-product-description-generator.git
    cd automated-product-description-generator
    ```

2. Create a virtual environment and activate it:

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows, use `.venv\\Scripts\\activate`
    ```

3. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Build and start the Docker containers:

    ```bash
    docker-compose up -d
    ```

## Usage

### Running the Server

To start the FastAPI server:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
### Generating Descriptions

Use the trigger_requests.py script to start the server and generate product descriptions:

```bash
python app_initializer.py
```

### Checking Server Health

To check if the server is running, access the health check endpoint:

```bash
curl http://localhost:8000/health
```

## Development
### Project Structure

```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── llm_agent.py
│   └── utils
├── outputs
│   └── product_descriptions.json
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── trigger_requests.py
└── README.md
```


### Running Tests
To run tests (assuming you have test scripts):

```bash
pytest
```

## Contributing
Contributions are welcome! Please fork the repository and use a feature branch. Pull requests are reviewed actively.

Fork the Project
* Create your Feature Branch (git checkout -b feature/AmazingFeature)
* Commit your Changes (git commit -m 'Add some AmazingFeature')
* Push to the Branch (git push origin feature/AmazingFeature)
* Open a Pull Request

## License
Distributed under the MIT License. See LICENSE for more information.
