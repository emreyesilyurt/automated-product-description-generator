# AI Product Description Generator

This repository demonstrates how to use an AI agent to automate the generation of product descriptions for technology gadgets using OpenAI's GPT-4-turbo. The AI agent repeatedly generates descriptions for a list of specified gadgets, ensuring efficiency and consistency without human intervention.

## Features

- Automated generation of product descriptions for technology gadgets
- Efficient and consistent output using AI
- No human intervention required

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/ai-product-description-generator.git
    cd ai-product-description-generator
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required libraries:
    ```bash
    pip install -r requirements.txt
    ```

4. Set your OpenAI API key in the `main.py` file:
    ```python
    openai.api_key = 'YOUR_OPENAI_API_KEY'
    ```

## Usage

Run the script to generate product descriptions:
```bash
python main.py
```

The script will generate descriptions for the specified gadgets and print them to the console.

## Folder Structure

- `agent/`
  - `llm_agent.py`: Contains the LLM_Agent class for interacting with GPT-4.
  - `environment.py`: Contains the SimpleEnvironment class.
- `utils/`
  - `generate_description.py`: Contains utility functions for generating product descriptions.
- `main.py`: Main script to run the AI agent.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or additions.
