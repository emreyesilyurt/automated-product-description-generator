from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from app.llm_marketing_agent import LLM_Agent, MarketingCheckerAgent
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

# Ensure the descriptions file exists in the new path
descriptions_dir = "/app/data"
descriptions_file = os.path.join(descriptions_dir, "product_descriptions.json")
logger.info(f"Checking if {descriptions_file} exists")
if not os.path.exists(descriptions_dir):
    os.makedirs(descriptions_dir, exist_ok=True)
    logger.info(f"Created directory {descriptions_dir}")
if not os.path.exists(descriptions_file):
    with open(descriptions_file, 'w') as f:
        json.dump({}, f)
    logger.info("Created product_descriptions.json")

@app.post("/generate_description/")
async def generate_description(request: ProductRequest):
    prompt = f"Create a detailed, unbiased, and straightforward product description for the technology gadget {request.product_name}. Avoid using marketing language or qualifiers."
    description = agent.query_llm(prompt)
    attempts = 0
    max_attempts = 5

    while checker_agent.check_for_marketing_qualifiers(description) and attempts < max_attempts:
        description = agent.query_llm(prompt)
        attempts += 1

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

    # Ensure the descriptions file exists and is loaded correctly
    logger.info(f"Ensuring {descriptions_file} exists")
    if not os.path.exists(descriptions_file):
        with open(descriptions_file, 'w') as f:
            json.dump({}, f)
        logger.info("Created product_descriptions.json inside request handler")

    logger.info(f"Loading {descriptions_file}")
    with open(descriptions_file, 'r') as f:
        try:
            descriptions = json.load(f)
            logger.info("Loaded existing descriptions")
        except json.JSONDecodeError:
            descriptions = {}
            logger.error("Failed to decode JSON from product_descriptions.json")

    # Update descriptions with the new result
    descriptions[request.product_name] = result

    # Write back to the JSON file
    logger.info(f"Writing to {descriptions_file}")
    with open(descriptions_file, 'w') as f:
        json.dump(descriptions, f, indent=4)
        logger.info(f"Updated product_descriptions.json with {request.product_name}")

    return result

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
