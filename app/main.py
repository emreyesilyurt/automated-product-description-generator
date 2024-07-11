from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from app.llm_agent import LLM_Agent, MarketingCheckerAgent
import json
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

class ProductRequest(BaseModel):
    product_name: str

agent = LLM_Agent()
checker_agent = MarketingCheckerAgent()

# Use the 'outputs' directory for storing descriptions
descriptions_dir = "outputs"
descriptions_file = os.path.join(descriptions_dir, "product_descriptions.json")

# Ensure the directory exists
if not os.path.exists(descriptions_dir):
    os.makedirs(descriptions_dir, exist_ok=True)
    logger.info(f"Created directory {descriptions_dir}")

# Ensure the file exists
if not os.path.exists(descriptions_file):
    with open(descriptions_file, 'w') as f:
        json.dump({}, f)
    logger.info("Created product_descriptions.json")

@app.post("/generate_description/")
async def generate_description(request: ProductRequest):
    prompt = f"Create a detailed, unbiased, and straightforward product description for the technology gadget {request.product_name}. Avoid using marketing language or qualifiers."
    
    attempts = 0
    max_attempts = 5
    description = agent.query_llm(prompt)
    logger.info(f"Initial generated description for {request.product_name}: {description}")

    while checker_agent.check_for_marketing_qualifiers(description) and attempts < max_attempts:
        description = agent.query_llm(prompt)
        attempts += 1
        logger.info(f"Attempt {attempts} - Generated description for {request.product_name}: {description}")

    if attempts == max_attempts:
        result = {
            "description": description,
            "timestamp": datetime.now().isoformat(),
            "warning": "Max attempts reached. The description may contain marketing qualifiers."
        }
    else:
        result = {
            "description": description,
            "timestamp": datetime.now().isoformat()
        }

    # Log the generated description
    logger.info(f"Final generated description for {request.product_name}: {description}")

    # Load existing descriptions
    try:
        with open(descriptions_file, 'r') as f:
            descriptions = json.load(f)
            logger.info("Loaded existing descriptions")
    except json.JSONDecodeError:
        descriptions = {}
        logger.error("Failed to decode JSON from product_descriptions.json")

    # Update descriptions with the new result
    descriptions[request.product_name] = result

    # Write back to the JSON file
    with open(descriptions_file, 'w') as f:
        json.dump(descriptions, f, indent=4)
        logger.info(f"Updated product_descriptions.json with {request.product_name}")

    return result

@app.get("/health")
async def health_check():
    return {"status": "OK"}

@app.get("/get_descriptions/")
async def get_descriptions():
    with open(descriptions_file, 'r') as f:
        descriptions = json.load(f)
    return descriptions

@app.get("/get_description/{product_name}")
async def get_description(product_name: str):
    with open(descriptions_file, 'r') as f:
        descriptions = json.load(f)

    if product_name in descriptions:
        return descriptions[product_name]
    else:
        raise HTTPException(status_code=404, detail="Product description not found")
