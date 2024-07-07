def generate_product_description(agent, product_name):
    prompt = f"Create a product description for the technology gadget {product_name}."
    return agent.query_llm(prompt)

def automate_generation(agent, product_names):
    for i, product_name in enumerate(product_names):
        print(f"\nIteration {i+1} for {product_name}:")
        llm_response = generate_product_description(agent, product_name)
        print(f"LLM Response for {product_name}: {llm_response}")
