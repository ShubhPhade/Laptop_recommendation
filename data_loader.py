# data_loader.py
import pandas as pd
from config import CSV_FILE_PATH, PRODUCT_ID_COLUMN, PRODUCT_NAME_COLUMN, DESCRIPTION_COLUMN

def load_products():
    """
    Loads product data from the CSV file specified in config.
    Returns a list of product dictionaries.
    """
    PRODUCT_ID_COLUMN
    try:
        df = pd.read_csv(CSV_FILE_PATH)
        # Basic validation: Check if essential columns exist
        required_cols = [PRODUCT_ID_COLUMN, PRODUCT_NAME_COLUMN, DESCRIPTION_COLUMN]
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns in CSV: {', '.join(missing_cols)}. Please check config.py and your CSV file.")

        products = df.to_dict(orient='records')
        if not products:
            print("Warning: No products loaded. The CSV might be empty or formatted incorrectly.")
        return products
    except FileNotFoundError:
        print(f"Error: The file {CSV_FILE_PATH} was not found.")
        return []
    except pd.errors.EmptyDataError:
        print(f"Error: The file {CSV_FILE_PATH} is empty.")
        return []
    except ValueError as ve:
        print(f"Configuration Error: {ve}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred while loading CSV: {e}")
        return []

if __name__ == '__main__':
    # For testing data_loader.py independently
    products_data = load_products()
    if products_data:
        print(f"Successfully loaded {len(products_data)} products.")
        print("First product:", products_data[0])
    else:
        print("Failed to load products.")
    
    print('successful')
