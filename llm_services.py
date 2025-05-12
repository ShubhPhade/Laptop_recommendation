# llm_services.py
import json
import ollama
from config import (
    LLM_MODEL, PRODUCT_NAME_COLUMN, DESCRIPTION_COLUMN, PRICE_COLUMN, BRAND_COLUMN,
    RAM_COLUMN, STORAGE_COLUMN, DISPLAY_SIZE_COLUMN, OS_COLUMN, BATTERY_LIFE_COLUMN, RATING_COLUMN
)

def ollama_instruct_completion(prompt_text, system_prompt_text=None, model_name=LLM_MODEL):
    """
    Gets a completion from an Ollama model, optionally using a system prompt.
    """
    messages = []
    if system_prompt_text:
        messages.append({'role': 'system', 'content': system_prompt_text})
    messages.append({'role': 'user', 'content': prompt_text})
    
    try:
        response = ollama.chat(
            model=model_name,
            messages=messages
        )
        return response['message']['content']
    except Exception as e:
        print(f"Error with Ollama model {model_name} (instruct): {e}")
        return "Error: Could not get response from local AI model."

def parse_json_response(response_str):
    """
    Tries to parse a JSON object from the LLM's response string.
    """
    try:
        response_str = response_str.strip()
        json_start = response_str.find("{")
        json_end = response_str.rfind("}") + 1
        if json_start == -1 or json_end == -1:
            return None
        return json.loads(response_str[json_start:json_end])
    except json.JSONDecodeError as e:
        print(f"  - JSON parsing error: {e}")
        return None

def classify_query_type(user_query):
    """
    Returns a classification of the query type: informational, transactional, or navigational.
    """
    system_prompt = (
        "Classify the following e-commerce search query as one of: 'informational', 'transactional', or 'navigational'. "
        "Output only the classification word."
    )
    classification = ollama_instruct_completion(user_query, system_prompt_text=system_prompt)
    return classification.strip().lower()

def parse_query_with_llm(user_query):
    """
    Uses Ollama LLM to parse the user query into a structured format.
    Extracts category, brand, features, and constraints to guide semantic search and filtering.
    """
    system_prompt = (
        "You are a query parsing assistant for an e-commerce search system. "
        "Your goal is to extract structured information from the user's query. "
        "Output ONLY in JSON format with the following keys if present: "
        "category, brand, usage, RAM, storage, display_size, OS, battery_life, price_constraint, color, size. "
        "Avoid any explanation or extra text. Only a JSON object."
    )
    
    llm_response = ollama_instruct_completion(user_query, system_prompt_text=system_prompt)
    
    parsed_result = parse_json_response(llm_response)
    if parsed_result is None:
        print(f"  - Failed to parse structured query, falling back to plain query string: {user_query}")
        return {"raw_query": user_query}
    
    return parsed_result

def ollama_chat_interaction(prompt, chat_history=None, context=None, model_name=LLM_MODEL):
    """
    Handles chat interaction using Ollama.
    Adds context as a system message and constructs the full conversation history.
    """
    if not prompt:
        return "Error: No user prompt provided."

    messages = []

    # Add system context if available
    if context:
        messages.append({"role": "system", "content": context})

    # Add previous chat history if provided
    if chat_history:
        messages.extend(chat_history)

    # Add current user message
    messages.append({"role": "user", "content": prompt})

    try:
        response = ollama.chat(
            model=model_name,
            messages=messages
        )
        return response['message']['content']
    except Exception as e:
        print(f"Error with Ollama model {model_name} (chat): {e}")
        return "Error: Could not get response from local AI model for chat."

def generate_enhanced_description(product_data_dict):
    """
    Uses Ollama LLM to generate an enhanced product description,
    leveraging more detailed product attributes.
    """
    product_name = product_data_dict.get(PRODUCT_NAME_COLUMN, "This product")
    brand = product_data_dict.get(BRAND_COLUMN, "")
    description = product_data_dict.get(DESCRIPTION_COLUMN, "No detailed description provided.")
    price = product_data_dict.get(PRICE_COLUMN, "")
    ram = product_data_dict.get(RAM_COLUMN, "")
    storage = product_data_dict.get(STORAGE_COLUMN, "")
    display_size = product_data_dict.get(DISPLAY_SIZE_COLUMN, "")
    os = product_data_dict.get(OS_COLUMN, "")
    battery = product_data_dict.get(BATTERY_LIFE_COLUMN, "")
    rating = product_data_dict.get(RATING_COLUMN, "")

    details_parts = [f"Product Name: {product_name}"]
    if brand: details_parts.append(f"Brand: {brand}")
    if price: details_parts.append(f"Price: {price}") 
    if ram: details_parts.append(f"RAM: {ram}")
    if storage: details_parts.append(f"Storage: {storage}")
    if display_size: details_parts.append(f"Display: {display_size}")
    if os: details_parts.append(f"Operating System: {os}")
    if battery: details_parts.append(f"Battery Life: {battery}")
    if rating and rating.lower() not in ['not found', 'nan', '']: details_parts.append(f"Customer Rating: {rating} out of 5") 
    if description and description.lower() not in ['not found', 'nan', '']: details_parts.append(f"Original Description: {description}")

    product_details_for_prompt = "\n".join(details_parts)

    prompt_text = (
        f"Generate a compelling and highly engaging product description for the following laptop. "
        f"Make it suitable for an e-commerce website. Highlight its key benefits, unique selling points, "
        f"and target audience based on the provided details. Use enthusiastic and persuasive language. "
        f"Structure it into 2-3 concise paragraphs. Do not just list the features; weave them into a narrative.\n\n"
        f"Laptop Details:\n{product_details_for_prompt}"
    )
    
    system_prompt_text = "You are a highly skilled marketing copywriter specializing in e-commerce product descriptions for laptops. Your goal is to maximize customer interest and conversion by creating vivid and appealing narratives."
    enhanced_desc = ollama_instruct_completion(prompt_text, system_prompt_text=system_prompt_text)
    
    return enhanced_desc

if __name__ == '__main__':
    print(f"Testing LLM services with model: {LLM_MODEL}")

    queries_to_test = [
        "Dell XPS 15 with 32GB RAM and 1TB SSD for video editing",
        "i want to buy clothes",
        "fridge"
    ]
    for test_query in queries_to_test:
        print(f"\nTesting query parsing for: '{test_query}'")
        parsed = parse_query_with_llm(test_query)
        print(f"  Original: '{test_query}'\n  Parsed (structured JSON): {parsed}")

    print("\nTesting enhanced description generation:")
    sample_product = {
        PRODUCT_NAME_COLUMN: 'Dell XPS 15 9530',
        BRAND_COLUMN: 'Dell',
        DESCRIPTION_COLUMN: 'A premium laptop for creators and professionals with stunning visuals.',
        PRICE_COLUMN: '₹249990',
        RAM_COLUMN: '32GB DDR5',
        STORAGE_COLUMN: '1TB NVMe SSD',
        DISPLAY_SIZE_COLUMN: '15.6-inch 3.5K OLED Touch',
        OS_COLUMN: 'Windows 11 Pro',
        BATTERY_LIFE_COLUMN: 'Up to 10 hours',
        RATING_COLUMN: '4.7'
    }
    enhanced = generate_enhanced_description(sample_product)
    print(f"Enhanced description for {sample_product[PRODUCT_NAME_COLUMN]}:\n{enhanced}")
