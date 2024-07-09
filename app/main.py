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

#descriptions_dir = "/app/data"
# Use a relative path or a path that you know is writable on your local system
descriptions_dir = "data"  # This will create/use a directory in the current working directory of the project

descriptions_file = os.path.join(descriptions_dir, "product_descriptions.json")
os.makedirs(descriptions_dir, exist_ok=True)
if not os.path.exists(descriptions_file):
    with open(descriptions_file, 'w') as f:
        json.dump({}, f)

@app.post("/generate_description/")
async def generate_description(request: ProductRequest):
    prompt = f"Create a detailed, unbiased, and straightforward product description for the technology gadget {request.product_name}. Avoid using marketing language or qualifiers."
    description = agent.query_llm(prompt)
    attempts = 0
    max_attempts = 5

    while checker_agent.check_for_marketing_qualifiers(description) and attempts < max_attempts:
        description = agent.query_llm(prompt)
        attempts += 1

    result = {
        "description": description,
        "timestamp": datetime.now().isoformat(),
        "warning": "Max attempts reached. The description may contain marketing qualifiers." if attempts == max_attempts else None
    }

    with open(descriptions_file, 'r+') as f:
        descriptions = json.load(f)
        descriptions[request.product_name] = result
        f.seek(0)
        json.dump(descriptions, f, indent=4)

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
