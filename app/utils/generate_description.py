from fastapi import FastAPI, HTTPException, Request
import json
import os

app = FastAPI()

outputs_dir = os.path.join(os.getcwd(), "outputs")
descriptions_file = os.path.join(outputs_dir, "product_descriptions.json")

@app.get("/get_descriptions")
async def get_descriptions():
    if not os.path.exists(descriptions_file):
        raise HTTPException(status_code=404, detail="Descriptions file not found")
    with open(descriptions_file, 'r') as f:
        descriptions = json.load(f)
    return descriptions

@app.post("/generate_description/")
async def generate_description(request: Request):
    data = await request.json()
    product_name = data.get("product_name")
    if not product_name:
        raise HTTPException(status_code=400, detail="Product name is required")

    # Here, you should implement your logic to generate the product description.
    description = f"Description for {product_name}"

    # Load existing descriptions
    if os.path.exists(descriptions_file):
        with open(descriptions_file, 'r') as f:
            descriptions = json.load(f)
    else:
        descriptions = {}

    # Add new description
    descriptions[product_name] = description

    # Save updated descriptions
    with open(descriptions_file, 'w') as f:
        json.dump(descriptions, f)

    return {"product_name": product_name, "description": description}
