# # llm_services.py
# import ollama
# from config import LLM_MODEL

# def ollama_instruct_completion(prompt_text, system_prompt_text=None, model_name=LLM_MODEL):
#     """
#     Gets a completion from an Ollama instruction-tuned model.
#     """
#     messages = []
#     if system_prompt_text:
#         messages.append({'role': 'system', 'content': system_prompt_text})
#     messages.append({'role': 'user', 'content': prompt_text})
    
#     try:
#         # print(f"\n[Ollama LLM] Getting completion from {model_name} for prompt: '{prompt_text[:100]}...'")
#         response = ollama.chat(
#             model=model_name,
#             messages=messages
#         )
#         return response['message']['content']
#     except Exception as e:
#         print(f"Error with Ollama model {model_name} (instruct): {e}")
#         return "Error: Could not get response from local AI model."

# def ollama_chat_interaction(chat_history_messages, model_name=LLM_MODEL):
#     """
#     Gets a chat completion from Ollama, using the provided chat history.
#     `chat_history_messages` should be a list of dicts, e.g., [{'role': 'user', 'content': 'Hi'}]
#     """
#     if not chat_history_messages:
#         return "Error: No chat history provided."
#     try:
#         # print(f"\n[Ollama Chat] Getting response from {model_name}. History length: {len(chat_history_messages)}")
#         response = ollama.chat(
#             model=model_name,
#             messages=chat_history_messages
#         )
#         return response['message']['content']
#     except Exception as e:
#         print(f"Error with Ollama model {model_name} (chat): {e}")
#         return "Error: Could not get response from local AI model for chat."

# def parse_query_with_llm(user_query):
#     """
#     Uses Ollama LLM to parse the user query for better search intent.
#     """
#     # print(f"\n[LLM Query Parser] Parsing query: '{user_query}'")
#     system_prompt = (
#         """You must only provide information related to laptops. If the user asks about any product or topic that is not related to laptops, politely decline to answer and encourage the user to search for laptops instead"""
#         "You are an expert query understanding system. Your task is to rephrase the user's product search query "
#         "to be more effective for semantic search. Focus on extracting key product types, features, brand names, "
#         "and any specific requirements. Output only the refined query. For example, if the user says "
#         "'I need a cheap laptop for coding and school under $700', you might output: "
#         "'budget laptop for programming and student use under $700'. If the query is already good, "
#         "you can return it as is or make minor improvements for clarity."
#     )
#     refined_query = ollama_instruct_completion(user_query, system_prompt_text=system_prompt)
    
#     if "Error:" in refined_query: # Check if LLM call failed
#         print(f"  - Query parsing failed, using original query: {user_query}")
#         return user_query # Fallback to original query
        
#     # print(f"  - Original Query: {user_query}")
#     # print(f"  - Refined Query by LLM: {refined_query}")
#     return refined_query

# def generate_enhanced_description(product_data_dict):
#     """
#     Uses Ollama LLM to generate an enhanced product description.
#     `product_data_dict` is a dictionary of the selected product.
#     """
#     from config import PRODUCT_NAME_COLUMN, DESCRIPTION_COLUMN # Import here to avoid circular dependency if this file was imported elsewhere
    
#     product_name = product_data_dict.get(PRODUCT_NAME_COLUMN, "This product")
#     original_desc = product_data_dict.get(DESCRIPTION_COLUMN, "No detailed description provided.")
#     # You can add more fields from product_data_dict to the prompt if they exist in your CSV and config
#     # price = product_data_dict.get(config.PRICE_COLUMN, None)

#     prompt_text = (
#          """You must only provide information related to laptops. If the user asks about any product or topic that is not related to laptops, politely decline to answer and encourage the user to search for laptops instead"""
#         f"Generate a compelling and engaging product description for the following item. "
#         f"Make it suitable for an e-commerce website. Highlight key benefits and unique selling points. "
#         f"Use enthusiastic and persuasive language. Keep it to 1-2 concise paragraphs.\n\n"
#         f"Product Name: {product_name}\n"
#         f"Existing Description/Details: {original_desc}\n"
#         # + (f"Price: {price}\n" if price else "")
#     )
    
#     system_prompt_text = "You are a highly skilled marketing copywriter specializing in e-commerce product descriptions. Your goal is to maximize customer interest and conversion."
#     enhanced_desc = ollama_instruct_completion(prompt_text, system_prompt_text=system_prompt_text)
    
#     # print(f"  - Generated Enhanced Description for {product_name}:\n{enhanced_desc}")
#     return enhanced_desc

# if __name__ == '__main__':
#     # For testing llm_services.py independently
#     # Requires Ollama server to be running with LLM_MODEL
#     print(f"Testing LLM services with model: {LLM_MODEL}")

#     # Test query parsing
#     test_query = "Tell me about good cheap laptops for students for programming"
#     print(f"\nTesting query parsing for: '{test_query}'")
#     parsed = parse_query_with_llm(test_query)
#     print(f"Parsed query: {parsed}")

#     # Test chat interaction
#     print("\nTesting chat interaction:")
#     history = [{"role": "user", "content": "Hello, what is Ollama?"}]
#     response = ollama_chat_interaction(history)
#     print(f"Response to 'Hello, what is Ollama?': {response}")
    
#     if "Error:" not in response:
#         history.append({"role": "assistant", "content": response})
#         history.append({"role": "user", "content": "How can I use it with Python?"})
#         response2 = ollama_chat_interaction(history)
#         print(f"Response to 'How can I use it with Python?': {response2}")

#     # Test description generation
#     print("\nTesting enhanced description generation:")
#     sample_product = {
#         'product_id': 'T123',
#         'product_name': 'UltraBook Pro X1',
#         'description': '14 inch display, 8GB RAM, 256GB SSD. Good for work.'
#         # 'price': '699.99' # Example if price column is used
#     }
#     enhanced = generate_enhanced_description(sample_product)
#     print(f"Enhanced description for {sample_product['product_name']}:\n{enhanced}")


# ====================================================================================================


# llm_services.py
import ollama
from config import LLM_MODEL

def ollama_instruct_completion(prompt_text, system_prompt_text=None, model_name=LLM_MODEL):
    """
    Gets a completion from an Ollama instruction-tuned model.
    """
    messages = []
    if system_prompt_text:
        messages.append({'role': 'system', 'content': system_prompt_text})
    messages.append({'role': 'user', 'content': prompt_text})
    
    try:
        # print(f"\n[Ollama LLM] Getting completion from {model_name} for prompt: '{prompt_text[:100]}...'")
        response = ollama.chat(
            model=model_name,
            messages=messages
        )
        return response['message']['content']
    except Exception as e:
        print(f"Error with Ollama model {model_name} (instruct): {e}")
        return "Error: Could not get response from local AI model."

def ollama_chat_interaction(chat_history_messages, model_name=LLM_MODEL):
    """
    Gets a chat completion from Ollama, using the provided chat history.
    `chat_history_messages` should be a list of dicts, e.g., [{'role': 'user', 'content': 'Hi'}]
    """
    if not chat_history_messages:
        return "Error: No chat history provided."
    try:
        # print(f"\n[Ollama Chat] Getting response from {model_name}. History length: {len(chat_history_messages)}")
        response = ollama.chat(
            model=model_name,
            messages=chat_history_messages
        )
        return response['message']['content']
    except Exception as e:
        print(f"Error with Ollama model {model_name} (chat): {e}")
        return "Error: Could not get response from local AI model for chat."

def parse_query_with_llm(user_query):
    """
    Uses Ollama LLM to parse the user query for better search intent.
    The goal is to create a query that is effective for semantic search,
    emphasizing the preservation of the core product category.
    """
    # print(f"\n[LLM Query Parser] Parsing query: '{user_query}'")
    system_prompt = (
        "You are an expert query understanding system. Your primary task is to refine the user's product search query "
        "for effective semantic search. Crucially, if the user specifies a clear product category (e.g., 'laptop', 'washing machine', 'smartphone', 't-shirt'), "
        "ensure this exact product category is preserved and emphasized in the refined query. "
        "Also extract other key features, brand names, colors, sizes, and requirements. Output only the refined query. "
        "For example, if user says 'washing machine front load 8kg', output 'front load 8kg washing machine'. "
        "If user says 'tell me about budget laptops for students', output 'budget student laptops'. "
        "If user says 'red cotton t-shirt large', output 'large red cotton t-shirt'. "
        "If the query is already very specific and clear, you can return it with minimal changes or as is."
    )
    refined_query = ollama_instruct_completion(user_query, system_prompt_text=system_prompt)
    
    if "Error:" in refined_query: # Check if LLM call failed
        print(f"  - Query parsing failed, using original query: {user_query}")
        return user_query # Fallback to original query
        
    # print(f"  - Original Query: {user_query}")
    # print(f"  - Refined Query by LLM: {refined_query}")
    return refined_query

def generate_enhanced_description(product_data_dict):
    """
    Uses Ollama LLM to generate an enhanced product description.
    `product_data_dict` is a dictionary of the selected product.
    """
    # Importing config variables locally to avoid potential circular import issues
    # if this file were to be imported by config or a file config imports.
    from config import PRODUCT_NAME_COLUMN, DESCRIPTION_COLUMN 
    
    product_name = product_data_dict.get(PRODUCT_NAME_COLUMN, "This product")
    original_desc = product_data_dict.get(DESCRIPTION_COLUMN, "No detailed description provided.")
    # Example: You could add other product attributes from product_data_dict to the prompt
    # price = product_data_dict.get(config.PRICE_COLUMN, None) # If you had PRICE_COLUMN in config

    prompt_text = (
        f"Generate a compelling and engaging product description for the following item. "
        f"Make it suitable for an e-commerce website. Highlight key benefits and unique selling points. "
        f"Use enthusiastic and persuasive language. Keep it to 1-2 concise paragraphs.\n\n"
        f"Product Name: {product_name}\n"
        f"Existing Description/Details: {original_desc}\n"
        # + (f"Price: {price}\n" if price else "") # Example if using price
    )
    
    system_prompt_text = "You are a highly skilled marketing copywriter specializing in e-commerce product descriptions. Your goal is to maximize customer interest and conversion."
    enhanced_desc = ollama_instruct_completion(prompt_text, system_prompt_text=system_prompt_text)
    
    # print(f"  - Generated Enhanced Description for {product_name}:\n{enhanced_desc}")
    return enhanced_desc

if __name__ == '__main__':
    # For testing llm_services.py independently
    # Requires Ollama server to be running with LLM_MODEL
    print(f"Testing LLM services with model: {LLM_MODEL}")

    # Test query parsing
    queries_to_test = [
        "Tell me about good cheap laptops for students for programming",
        "washing machine",
        "front load 8kg washing machine with dryer",
        "red cotton t-shirt large"
    ]
    for test_query in queries_to_test:
        print(f"\nTesting query parsing for: '{test_query}'")
        parsed = parse_query_with_llm(test_query)
        print(f"  Original: '{test_query}'\n  Parsed:   '{parsed}'")


    # Test chat interaction
    print("\nTesting chat interaction:")
    history = [{"role": "user", "content": "Hello, what is Ollama?"}]
    response = ollama_chat_interaction(history)
    print(f"Response to 'Hello, what is Ollama?': {response}")
    
    if "Error:" not in response:
        history.append({"role": "assistant", "content": response})
        history.append({"role": "user", "content": "How can I use it with Python?"})
        response2 = ollama_chat_interaction(history)
        print(f"Response to 'How can I use it with Python?': {response2}")

    # Test description generation
    print("\nTesting enhanced description generation:")
    sample_product = {
        # Ensure these keys match what's defined in your config.py for column names
        'product_name': 'EcoWash Deluxe 8000', # Assuming PRODUCT_NAME_COLUMN is 'product_name'
        'description': 'Front-loading washing machine, 8kg capacity, 15 wash programs, energy efficient A+++.' # Assuming DESCRIPTION_COLUMN is 'description'
        # 'price': '499.99' # Example if price column is used
    }
    # If your config.py uses different keys, adjust sample_product accordingly:
    # from config import PRODUCT_NAME_COLUMN, DESCRIPTION_COLUMN
    # sample_product = {
    #     PRODUCT_NAME_COLUMN: 'EcoWash Deluxe 8000',
    #     DESCRIPTION_COLUMN: 'Front-loading washing machine, 8kg capacity, 15 wash programs, energy efficient A+++.'
    # }

    enhanced = generate_enhanced_description(sample_product)
    print(f"Enhanced description for {sample_product.get(PRODUCT_NAME_COLUMN, 'N/A')}:\n{enhanced}")

