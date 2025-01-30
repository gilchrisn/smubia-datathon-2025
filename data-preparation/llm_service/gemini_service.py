from dotenv import load_dotenv
import os
import google.generativeai as genai
from llm_service.prompts import CROSS_REFERENCING_PROMPT, EXTRACT_SUBGRAPH_PROMPT
import json

load_dotenv()

genai.configure(api_key=os.getenv("GENAI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def generate_response(prompt):
    """Generate a response from the LLM model."""
    try:
        # Generate response from LLM
        response = model.generate_content(prompt)
        response_text = response.text

        return response_text
    except Exception as e:
        print(f"Error during LLM processing: {e}")
        return {"error": str(e)}
    
def generate_subgraph(text):
    """Generate a subgraph from the input text."""
    prompt = EXTRACT_SUBGRAPH_PROMPT + "\n" + text
    response = generate_response(prompt)

    return parse_response(response)

def cross_reference_entities(text_1 : str, text_2 : str):
    """Cross-reference entities from two texts."""
    prompt = CROSS_REFERENCING_PROMPT + "text_1:\n" + text_1 + "text_2:\n" + text_2
    response = generate_response(prompt)

    return parse_response(response)
    
def parse_response(response):
    cleaned_response = response.strip().strip('```json')

    # Parse response into a dictionary
    response_dict = json.loads(cleaned_response)
    return response_dict