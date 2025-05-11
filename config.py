# config.py

# --- File Paths ---
CSV_FILE_PATH = '/Users/shubhamphade/Documents/VS_Code/Laptop_Final2/product_recommendation_app/scraped_products.csv'

# --- CSV Column Names ---
# Adjust these to match the exact column names in your CSV file
PRODUCT_ID_COLUMN = 'product_id'        # Example: 'id', 'SKU'
PRODUCT_NAME_COLUMN = 'product_name'    # Example: 'name', 'Title'
DESCRIPTION_COLUMN = 'description'    # Example: 'desc', 'ProductDescription'
# Add other relevant columns if needed, e.g., for price, category
# PRICE_COLUMN = 'price'

# --- Ollama Model Configuration ---
# Ensure these models are pulled in your Ollama instance
EMBEDDING_MODEL = 'nomic-embed-text'    # For generating product and query embeddings
LLM_MODEL = 'llama3:8b'        # For query parsing, chat, and description generation
# Alternative LLM_MODEL (potentially lighter, adjust if needed):
# LLM_MODEL = 'phi3:mini-instruct'
# LLM_MODEL = 'mistral:7b-instruct'

# --- Vector Store & Retrieval ---
TOP_N_RESULTS = 3 # Number of products to retrieve

# --- Text for Embedding ---
# Defines how text is combined for creating embeddings.
# You can customize this based on which columns provide the most semantic value.
def get_text_for_embedding(product_dict):
    """
    Combines product information into a single string for embedding.
    """
    name = product_dict.get(PRODUCT_NAME_COLUMN, "")
    description = product_dict.get(DESCRIPTION_COLUMN, "")
    # Example: include price if it exists and is relevant
    # price = product_dict.get(PRICE_COLUMN, "")
    # text_parts = [name, description, str(price) if price else ""]
    text_parts = [name, description]
    return " ".join(filter(None, text_parts)).strip()

print('successful')
