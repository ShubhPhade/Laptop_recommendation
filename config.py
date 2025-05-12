# config.py

# --- File Paths ---
# Consider using a relative path if the CSV is in the same directory or a subdirectory:
# CSV_FILE_PATH = 'scraped_products.csv'
CSV_FILE_PATH = '/Users/shubhamphade/Documents/VS_Code/Laptop_Final2/product_recommendation_app/scraped_products.csv'

# --- CSV Column Names ---
# IMPORTANT: Ensure these string values exactly match the column headers in your CSV file.

# Assuming 'Product URL' column contains unique identifiers for each product
PRODUCT_ID_COLUMN = 'Product URL=ROWS(A:A)' # Changed from PRODUCT_URL and assuming actual column name

PRODUCT_NAME_COLUMN = 'product_name'
DESCRIPTION_COLUMN = 'description'
PRICE_COLUMN = 'Price' # Now active
BRAND_COLUMN = 'Brand' # Standardized to BRAND_COLUMN for clarity
RAM_COLUMN = 'RAM'
STORAGE_COLUMN = 'Storage'
DISPLAY_SIZE_COLUMN = 'Display Size' # Using this one, removed duplicate 'DISPLAY'
BATTERY_LIFE_COLUMN = 'Battery Life'
RATING_COLUMN = 'Rating'
WEIGHT_COLUMN = 'Weight'
WARRANTY_COLUMN = 'Warranty'
OS_COLUMN = 'OS' # Standardized to OS_COLUMN

# --- Ollama Model Configuration ---
# Ensure these models are pulled in your Ollama instance
EMBEDDING_MODEL = 'nomic-embed-text'    # For generating product and query embeddings
LLM_MODEL = 'llama3:8b'                 # For query parsing, chat, and description generation

# --- Vector Store & Retrieval ---
TOP_N_RESULTS = 3 # Number of products to retrieve

# --- Text for Embedding ---
# Defines how text is combined for creating embeddings.
# UPDATED to include more relevant features for richer embeddings.
def get_text_for_embedding(product_dict):
    """
    Combines product information into a single string for embedding.
    This helps the semantic search understand products based on more than just name/description.
    """
    name = product_dict.get(PRODUCT_NAME_COLUMN, "")
    brand = product_dict.get(BRAND_COLUMN, "")
    description = product_dict.get(DESCRIPTION_COLUMN, "")
    ram = product_dict.get(RAM_COLUMN, "")
    storage = product_dict.get(STORAGE_COLUMN, "")
    display = product_dict.get(DISPLAY_SIZE_COLUMN, "")
    price = product_dict.get(PRICE_COLUMN, "") # Price might not always be ideal for semantic similarity of features
    os = product_dict.get(OS_COLUMN, "")

    # Construct a descriptive string.
    # Example: "Apple MacBook Pro: 16GB RAM, 512GB SSD, 16-inch Display. Powerful laptop for professionals."
    feature_summary = []
    if brand:
        feature_summary.append(f"Brand: {brand}")
    if ram:
        feature_summary.append(f"{ram} RAM")
    if storage:
        feature_summary.append(storage) # Storage often includes "SSD" or "HDD"
    if display:
        feature_summary.append(f"{display} Display")
    if os:
        feature_summary.append(f"{os}")
    if price:
        feature_summary.append(f"{os}")

    text_parts = [
        name,
        ", ".join(filter(None, feature_summary)), # Join features with a comma
        description
    ]
    
    # Join all parts with a space, ensuring to filter out any empty strings that might result
    # from missing data in product_dict.
    full_text = ". ".join(filter(None, text_parts)).strip()
    # Replace multiple spaces with a single space for cleanliness
    return ' '.join(full_text.split())

print('successful')
