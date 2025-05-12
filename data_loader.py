# # data_loader.py
# import pandas as pd
# from config import CSV_FILE_PATH, PRODUCT_URL, PRODUCT_NAME_COLUMN, DESCRIPTION_COLUMN, BATTERY_LIFE, RATING, PRICE_COLUMN, WEIGHT, DISPLAY_SIZE, RAM, STORAGE, DISPLAY, WARRANTY, BRAND, OPERATING_SYSTEM 

# def load_products():
#     """
#     Loads product data from the CSV file specified in config.
#     Returns a list of product dictionaries.
#     """
#     PRODUCT_URL
#     try:
#         df = pd.read_csv(CSV_FILE_PATH)
#         # Basic validation: Check if essential columns exist
#         required_cols = [PRODUCT_URL, PRODUCT_NAME_COLUMN, DESCRIPTION_COLUMN,BATTERY_LIFE, RATING, PRICE_COLUMN, WEIGHT, DISPLAY_SIZE, RAM, STORAGE, DISPLAY, WARRANTY, BRAND, OPERATING_SYSTEM]
#         missing_cols = [col for col in required_cols if col not in df.columns]
#         if missing_cols:
#             raise ValueError(f"Missing required columns in CSV: {', '.join(missing_cols)}. Please check config.py and your CSV file.")

#         products = df.to_dict(orient='records')
#         if not products:
#             print("Warning: No products loaded. The CSV might be empty or formatted incorrectly.")
#         return products
#     except FileNotFoundError:
#         print(f"Error: The file {CSV_FILE_PATH} was not found.")
#         return []
#     except pd.errors.EmptyDataError:
#         print(f"Error: The file {CSV_FILE_PATH} is empty.")
#         return []
#     except ValueError as ve:
#         print(f"Configuration Error: {ve}")
#         return []
#     except Exception as e:
#         print(f"An unexpected error occurred while loading CSV: {e}")
#         return []

# if __name__ == '__main__':
#     # For testing data_loader.py independently
#     products_data = load_products()
#     if products_data:
#         print(f"Successfully loaded {len(products_data)} products.")
#         print("First product:", products_data[0])
#     else:
#         print("Failed to load products.")
    
#     print('successful')

# ===================================================================================================


# # data_loader.py
# import pandas as pd
# from config import (
#     CSV_FILE_PATH, PRODUCT_ID_COLUMN, PRODUCT_NAME_COLUMN, DESCRIPTION_COLUMN,
#     PRICE_COLUMN, BRAND_COLUMN, RAM_COLUMN, STORAGE_COLUMN, DISPLAY_SIZE_COLUMN,
#     BATTERY_LIFE_COLUMN, RATING_COLUMN, WEIGHT_COLUMN, WARRANTY_COLUMN, OS_COLUMN
# )

# def load_products():
#     """
#     Loads product data from the CSV file specified in config.
#     Returns a list of product dictionaries.
#     Validates the presence of essential columns.
#     """
#     try:
#         df = pd.read_csv(CSV_FILE_PATH)
        
#         # Define essential columns that should be present in the CSV
#         # These are based on what's defined in config.py and likely used throughout the app
#         required_cols = [
#             PRODUCT_ID_COLUMN, PRODUCT_NAME_COLUMN, DESCRIPTION_COLUMN, PRICE_COLUMN,
#             BRAND_COLUMN, RAM_COLUMN, STORAGE_COLUMN, DISPLAY_SIZE_COLUMN, OS_COLUMN,
#             BATTERY_LIFE_COLUMN, RATING_COLUMN, WEIGHT_COLUMN, WARRANTY_COLUMN
#             # Add other columns here if they are absolutely critical for the app's core functionality
#             # For example, RATING_COLUMN, BATTERY_LIFE_COLUMN might also be considered essential
#             # depending on how you plan to use them.
#         ]
        
#         missing_cols = [col for col in required_cols if col not in df.columns]
#         if missing_cols:
#             raise ValueError(
#                 f"Missing required columns in CSV: {', '.join(missing_cols)}. "
#                 f"Please check config.py and your CSV file ('{CSV_FILE_PATH}'). "
#                 "Ensure column names in config.py exactly match your CSV headers."
#             )

#         # Convert all data to string type initially to avoid type issues with .get() later,
#         # especially for potentially missing values that pandas might infer as float (e.g., for numbers).
#         # Or handle types more carefully if specific numeric/etc. types are needed.
#         # For this RAG app, string representation is often sufficient for text processing.
#         df = df.astype(str) # Convert all columns to string to handle NaNs as 'nan' string
        
#         # Replace 'nan' strings (resulting from astype(str) on NaN values) with empty strings for cleaner .get()
#         for col in df.columns:
#             df[col] = df[col].replace({'nan': '', 'None': ''})


#         products = df.to_dict(orient='records')
        
#         if not products:
#             print("Warning: No products loaded. The CSV might be empty or formatted incorrectly.")
#         return products
        
#     except FileNotFoundError:
#         print(f"Error: The file {CSV_FILE_PATH} was not found.")
#         return []
#     except pd.errors.EmptyDataError:
#         print(f"Error: The file {CSV_FILE_PATH} is empty.")
#         return []
#     except ValueError as ve: # Catches the ValueError raised above for missing columns
#         print(f"Data Loading Configuration Error: {ve}")
#         return []
#     except Exception as e:
#         print(f"An unexpected error occurred while loading CSV: {e}")
#         return []

# if __name__ == '__main__':
#     # For testing data_loader.py independently
#     products_data = load_products()
#     if products_data:
#         print(f"Successfully loaded {len(products_data)} products.")
#         if products_data:
#             print("First product (all values as strings):", products_data[0])
#             print("\nKeys in first product:", list(products_data[0].keys()))
#             print(f"\nValue for '{BRAND_COLUMN}':", products_data[0].get(BRAND_COLUMN, "NOT FOUND"))
#             print(f"Value for '{RAM_COLUMN}':", products_data[0].get(RAM_COLUMN, "NOT FOUND"))
#     else:
#         print("Failed to load products.")



# ===================================================================================================

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

