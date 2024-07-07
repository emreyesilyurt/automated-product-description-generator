import openai
from agent.llm_agent import LLM_Agent
from agent.environment import SimpleEnvironment
from utils.generate_description import generate_product_description, automate_generation

# Set your OpenAI API key
openai.api_key = 'YOUR_OPENAI_API_KEY'

# Initialize and train the agent
actions = ["ask", "skip"]
agent = LLM_Agent(actions)
environment = SimpleEnvironment()

agent.train(environment, 1000)

# List of gadget names to generate descriptions for
gadget_names = ["Apple iPhone 13", "Samsung Galaxy Watch 4", "Amazon Echo Dot"]

# Run the automated generation process
automate_generation(agent, gadget_names)
