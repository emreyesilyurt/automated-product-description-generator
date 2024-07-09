import json
from datetime import datetime
from app.llm_marketing_agent import LLM_Agent, MarketingCheckerAgent

def generate_product_description(agent, product_name, attempt=1):
    prompt = f"Create a detailed, unbiased, and straightforward product description for the technology gadget {product_name}. Avoid using marketing language or qualifiers."
    description = agent.query_llm(prompt)
    return description

def automate_generation(agent, checker_agent, product_names):
    descriptions = {}
    max_attempts = 5
    for i, product_name in enumerate(product_names):
        print(f"\nIteration {i+1} for {product_name}:")
        attempts = 0
        llm_response = generate_product_description(agent, product_name)
        
        while checker_agent.check_for_marketing_qualifiers(llm_response) and attempts < max_attempts:
            print(f"Marketing qualifier found in the description for {product_name}. Regenerating... Attempt {attempts+1}")
            llm_response = generate_product_description(agent, product_name, attempts + 1)
            attempts += 1

        if attempts == max_attempts:
            print(f"Max attempts reached for {product_name}. Proceeding with the best available description.")

        print(f"LLM Response for {product_name}: {llm_response}")
        descriptions[product_name] = {
            "description": llm_response,
            "timestamp": datetime.now().isoformat()
        }

    # Write the descriptions to a JSON file
    with open('product_descriptions.json', 'w') as f:
        json.dump(descriptions, f, indent=4)
