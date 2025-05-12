# data_loader.py
import pandas as pd
from config import (
    CSV_FILE_PATH, PRODUCT_ID_COLUMN, PRODUCT_NAME_COLUMN, DESCRIPTION_COLUMN,
    PRICE_COLUMN, BRAND_COLUMN, RAM_COLUMN, STORAGE_COLUMN, DISPLAY_SIZE_COLUMN,
    BATTERY_LIFE_COLUMN, RATING_COLUMN, WEIGHT_COLUMN, WARRANTY_COLUMN, OS_COLUMN
)

def load_products():
    """
    Loads product data from the CSV file specified in config.
    Returns a list of product dictionaries.
    Validates the presence of essential columns.
    """
    print(f"DEBUG: Attempting to load CSV from: {CSV_FILE_PATH}") # DEBUG PRINT

    try:
        df = pd.read_csv(CSV_FILE_PATH)
        
        print("DEBUG: Successfully read CSV. Actual column headers found:") # DEBUG PRINT
        print(df.columns.tolist()) # DEBUG PRINT
        
        required_cols = [
            PRODUCT_ID_COLUMN, PRODUCT_NAME_COLUMN, DESCRIPTION_COLUMN, PRICE_COLUMN,
            BRAND_COLUMN, RAM_COLUMN, STORAGE_COLUMN, DISPLAY_SIZE_COLUMN, OS_COLUMN
        ]
        print("DEBUG: Required columns as per config.py:") # DEBUG PRINT
        print(required_cols) # DEBUG PRINT
        
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            error_message = (
                f"Missing required columns in CSV: {', '.join(missing_cols)}. "
                f"Please check config.py and your CSV file ('{CSV_FILE_PATH}'). "
                "Ensure column names defined as STRING VALUES in config.py (e.g., PRICE_COLUMN = 'Price') "
                "exactly match your CSV headers (case-sensitive)."
            )
            print(f"ERROR: {error_message}") # DEBUG PRINT
            raise ValueError(error_message)

        df = df.astype(str)
        for col in df.columns:
            df[col] = df[col].replace({'nan': '', 'None': ''})

        products = df.to_dict(orient='records')
        
        if not products:
            print("Warning: No products loaded after processing. The CSV might be effectively empty or have issues.")
        return products
        
    except FileNotFoundError:
        print(f"ERROR: The file {CSV_FILE_PATH} was not found.")
        return []
    except pd.errors.EmptyDataError:
        print(f"ERROR: The file {CSV_FILE_PATH} is empty.")
        return []
    except ValueError as ve: 
        # This will catch the ValueError raised above for missing columns
        print(f"Data Loading Configuration Error (likely missing columns): {ve}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred while loading CSV: {e}")
        return []

if __name__ == '__main__':
    products_data = load_products()
    if products_data:
        print(f"\nSuccessfully loaded {len(products_data)} products for independent test run.")
        if products_data:
            print("First product (all values as strings):", products_data[0])
    else:
        print("\nFailed to load products for independent test run.")

