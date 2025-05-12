# app.py
import streamlit as st
from config import (
    PRODUCT_NAME_COLUMN, DESCRIPTION_COLUMN, TOP_N_RESULTS, PRODUCT_ID_COLUMN,
    PRICE_COLUMN, BRAND_COLUMN, RAM_COLUMN, STORAGE_COLUMN, DISPLAY_SIZE_COLUMN, OS_COLUMN,
    RATING_COLUMN, BATTERY_LIFE_COLUMN
)
from data_loader import load_products
from embedding_utils import build_vector_store
from llm_services import parse_query_with_llm, ollama_chat_interaction, generate_enhanced_description
from retrieval import retrieve_top_products

# --- Page Configuration ---
st.set_page_config(page_title="Laptop Recommender AI", layout="wide")

# --- Initialization & State Management ---
def initialize_session_state():
    # Initialize session state variables if they don't exist
    if "products_loaded" not in st.session_state: st.session_state.products_loaded = False
    if "vector_store_built" not in st.session_state: st.session_state.vector_store_built = False
    if "all_products" not in st.session_state: st.session_state.all_products = [] # Expecting a list of product dicts
    if "retrieved_products" not in st.session_state: st.session_state.retrieved_products = [] # Expecting a list of product dicts
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [{"role": "assistant", "content": "Hello! How can I help you find a laptop today?"}]
    if "current_product_context_for_chat" not in st.session_state: st.session_state.current_product_context_for_chat = ""
    if "last_user_query_category_mismatch" not in st.session_state: st.session_state.last_user_query_category_mismatch = False
    if "last_user_search_query" not in st.session_state: st.session_state.last_user_search_query = ""

initialize_session_state()

# --- Load Data and Build Vector Store ---
# Load product data if not already loaded
if not st.session_state.products_loaded:
    with st.spinner("Loading product data... Please wait."):
        st.session_state.all_products = load_products() # Assumed to return a list of product dictionaries
        
        # Check if products were loaded successfully
        if st.session_state.all_products is not None and len(st.session_state.all_products) > 0:
            st.session_state.products_loaded = True
            st.success(f"Loaded {len(st.session_state.all_products)} laptop products.")
        else:
            st.error("Failed to load product data or no data found. Check CSV and config.py, and ensure load_products() returns a non-empty list.")
            st.stop() # Stop execution if data loading fails

# Build vector store if products are loaded but store isn't built
if st.session_state.products_loaded and not st.session_state.vector_store_built:
    with st.spinner("Building laptop knowledge base (vector store)... This may take some time."):
        # build_vector_store should handle a list of product dictionaries
        if build_vector_store(st.session_state.all_products): 
            st.session_state.vector_store_built = True
            st.success("Laptop knowledge base ready!")
        else:
            st.error("Failed to build vector store. Ensure Ollama is running or embedding model is accessible.")
            # Consider st.stop() here if vector store is critical for app functionality

# --- UI Layout ---
st.title("🛍️ AI-Powered Laptop Recommender")
st.markdown("Describe the laptop you're looking for (e.g., 'lightweight Dell laptop with 16GB RAM for programming'), and I'll find suitable options!")

# Search input and button
search_col, control_col = st.columns([3,1])
with search_col:
    user_query = st.text_input(
        "Enter your laptop query:",
        key="main_query_input", # Unique key for this input
        placeholder="e.g., 'Dell laptop 16GB RAM for gaming'"
    )
with control_col:
    st.write("") # Vertical alignment helper
    st.write("") # Vertical alignment helper
    search_button = st.button(
        "🔍 Search Laptops",
        type="primary",
        use_container_width=True,
        disabled=not st.session_state.vector_store_built # Disable button if vector store isn't ready
    )

# --- Search Logic and Product Retrieval ---
if search_button and user_query:
    # Reset state for a new search
    st.session_state.chat_history = [{"role": "assistant", "content": "I'm looking for laptops based on your new query. Ask me anything once the results are up!"}] 
    st.session_state.retrieved_products = []
    st.session_state.current_product_context_for_chat = ""
    st.session_state.last_user_query_category_mismatch = False
    st.session_state.last_user_search_query = user_query # Store the original query

    # Keywords for categorizing queries
    non_laptop_keywords = [
        "washing machine", "refrigerator", "fridge", "phone", "smartphone",
        "television", "tv", "camera", "t-shirt", "shoes", "book",
        "microwave", "oven", "tablet", "desktop", "monitor", "keyboard", "mouse",
        "printer", "projector", "speaker", "headphone", "earphone", "watch",
        "fan", "air conditioner", "ac", "cooler", "heater", "furniture", "sofa", "chair", "table", "bed",
        "clothes", "clothing", "apparel", "garment", "dress", "jeans", "shirt", "pant", "toy"
    ]
    laptop_keywords = ["laptop", "notebook", "ultrabook", "macbook", "chromebook", "pc", "computer", "netbook"]

    query_lower = user_query.lower()
    # Check if query is for non-laptop items without explicitly mentioning laptops
    query_is_for_non_laptop = any(f" {keyword} " in f" {query_lower} " or \
                                  query_lower.startswith(keyword + " ") or \
                                  query_lower.endswith(" " + keyword) or \
                                  query_lower == keyword for keyword in non_laptop_keywords)
    query_mentions_laptop_explicitly = any(f" {keyword} " in f" {query_lower} " or \
                                           query_lower.startswith(keyword + " ") or \
                                           query_lower.endswith(" " + keyword) or \
                                           query_lower == keyword for keyword in laptop_keywords)

    if query_is_for_non_laptop and not query_mentions_laptop_explicitly:
        st.warning("It seems you're looking for something other than a laptop. This system specializes in laptop recommendations. Please refine your query for laptops.")
        st.session_state.last_user_query_category_mismatch = True
        st.session_state.retrieved_products = [] # Clear any previous results
    else:
        st.session_state.last_user_query_category_mismatch = False
        with st.spinner("🧠 Analyzing your query with AI and searching for the best laptops..."):
            # 1. Parse and potentially enhance query with LLM
            parsed_query_data = parse_query_with_llm(user_query) # Assumes this returns an enhanced string or structured data

            query_for_retrieval = user_query # Default to original query
            if parsed_query_data:
                if isinstance(parsed_query_data, str) and parsed_query_data.strip(): # Check if it's a non-empty string
                    query_for_retrieval = parsed_query_data
                    st.info(f"Using AI-enhanced query: \"{query_for_retrieval}\"")
                elif isinstance(parsed_query_data, dict) and "query" in parsed_query_data and parsed_query_data["query"].strip():
                    query_for_retrieval = parsed_query_data["query"]
                    # Potentially handle other structured data like filters here
                    st.info(f"Using AI-parsed query components.")
                # Add more conditions based on the actual structure of parsed_query_data if needed
            else:
                st.warning("Could not enhance query using LLM, using your original query for search.")

            # 2. Retrieve top products from vector store
            # Assumes retrieve_top_products uses TOP_N_RESULTS from config.py internally or has its own default
            retrieved_items = retrieve_top_products(
                query_text=query_for_retrieval
            ) # Returns a list of product dictionaries

            if retrieved_items is not None and len(retrieved_items) > 0:
                st.session_state.retrieved_products = retrieved_items 
                st.success(f"Found {len(st.session_state.retrieved_products)} potential laptop matches!")
            else:
                st.info("No laptops found matching your refined query. You could try being more general or rephrasing.")
                st.session_state.retrieved_products = []


# --- Display Retrieved Products ---
if st.session_state.retrieved_products: # Check if there are products to display
    st.markdown("---")
    st.subheader("✨ Here are your AI-curated laptop recommendations:")

    for i, product_dict in enumerate(st.session_state.retrieved_products): # Iterate through the list of product dicts
        if not isinstance(product_dict, dict):
            st.error(f"Skipping a product due to unexpected data format: {type(product_dict)}. Expected a dictionary.")
            continue # Skip this item and go to the next

        # Safely get product details using .get() with fallbacks
        product_name = product_dict.get(PRODUCT_NAME_COLUMN, "N/A")
        product_id_value = product_dict.get(PRODUCT_ID_COLUMN)
        # Create a unique key for Streamlit elements, especially buttons inside loops
        product_id_for_key = product_id_value if product_id_value is not None else f"product_fallback_{i}"


        with st.container(border=True): # Use border for visual separation of products
            col1, col2 = st.columns([1, 2]) # Adjust ratio as needed for image/details

            with col1:
                # Placeholder for an image; replace with actual image if available
                # st.image(product_dict.get("image_url", "https://placehold.co/300x200/eee/ccc?text=Laptop"), use_column_width=True)
                st.markdown(f"##### {product_name}") # Display product name

            with col2:
                # Extract and display product attributes
                price = product_dict.get(PRICE_COLUMN)
                brand = product_dict.get(BRAND_COLUMN, "N/A")
                ram = product_dict.get(RAM_COLUMN, "N/A")
                storage = product_dict.get(STORAGE_COLUMN, "N/A")
                display = product_dict.get(DISPLAY_SIZE_COLUMN, "N/A")
                os_val = product_dict.get(OS_COLUMN, "N/A") # Renamed to avoid conflict with os module
                rating = product_dict.get(RATING_COLUMN, "N/A")
                battery = product_dict.get(BATTERY_LIFE_COLUMN, "N/A")
                url = product_dict.get(PRODUCT_ID_COLUMN)

                price_display = f"${price:,.2f}" if isinstance(price, (int, float)) else (str(price) if price is not None else "N/A")
                
                st.markdown(f"**Brand:** {brand} | **Price:** {price_display}")
                st.markdown(f"**RAM:** {ram} | **Storage:** {storage} | **Display:** {display}\"")
                battery_info = f" | **Battery:** {battery} hrs" if battery not in ["N/A", None, ""] else ""
                st.markdown(f"**OS:** {os_val} | **Rating:** {rating}/5{battery_info}")

                description = product_dict.get(DESCRIPTION_COLUMN, "No description available.")
                with st.expander("View Description"):
                    st.caption(description)

                # Optional: AI Enhanced Description (can be slow, enable if needed)
                # with st.expander("View AI Enhanced Description"):
                #     gen_desc_button_key = f"gen_desc_{product_id_for_key}"
                #     if st.button(f"Generate AI Description for {product_name[:30]}...", key=gen_desc_button_key):
                #         enhanced_desc = generate_enhanced_description(product_dict) # Pass the product dictionary
                #         st.write(enhanced_desc)

                # Button to discuss this specific product in chat
                chat_button_key = f"chat_btn_{product_id_for_key}" # Ensure unique key
                if st.button(f"💬 Discuss: {product_name[:40]}...", key=chat_button_key, help="Click to ask specific questions about this laptop."):
                    # Prepare context for the chat about this specific product
                    product_context = f"The user is asking about the {product_name}."
                    product_context += f"\nKey Details: Price {price_display}, Brand {brand}, RAM {ram}, Storage {storage}, Display {display}, OS {os_val}."
                    # Add more relevant details to the context string if needed
                    st.session_state.current_product_context_for_chat = product_context
                    # Reset chat history to focus on this product
                    st.session_state.chat_history = [
                        {"role": "assistant", "content": f"Okay, let's talk about the {product_name}. What specific questions do you have about it?"}
                    ]
                    st.rerun() # Rerun to update chat interface immediately

# --- Chat Interface (General or Product-Specific) ---
# Typically placed in the sidebar for better UX
st.sidebar.title("🤖 Laptop Chat Assistant")

if not st.session_state.vector_store_built:
    st.sidebar.warning("Knowledge base is not yet built. Chat will be enabled once it's ready.")
else:
    # Display context if chatting about a specific product
    if st.session_state.current_product_context_for_chat:
        try:
            # Attempt to parse product name from context for display
            current_product_name = st.session_state.current_product_context_for_chat.splitlines()[0].split("about the ")[1].rstrip('.')
            st.sidebar.info(f"Chatting about: **{current_product_name}**")
        except IndexError: # Fallback if parsing fails
            st.sidebar.info("Chatting about a specific product.")
    elif st.session_state.retrieved_products: # If products were retrieved but no specific one selected for chat
         st.sidebar.info("You can ask about the recommended laptops or general laptop questions.")
    else: # General state
        st.sidebar.info("Search for laptops to get recommendations. You can then chat about them or ask general questions.")

    # Display chat history
    for message in st.session_state.chat_history:
        with st.sidebar.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input field
    user_chat_input = st.sidebar.chat_input(
        "Ask a follow-up question...",
        key="chat_input_main", # Unique key for chat input
        disabled=not st.session_state.vector_store_built # Disable if knowledge base not ready
    )

    if user_chat_input:
        st.session_state.chat_history.append({"role": "user", "content": user_chat_input})
        with st.sidebar.chat_message("user"): # Display user message immediately
            st.markdown(user_chat_input)

        with st.spinner("AI is thinking..."):
            # CORRECTED CONTEXT PREPARATION:
            # Use the specific product context if available
            if st.session_state.current_product_context_for_chat:
                context_for_llm = st.session_state.current_product_context_for_chat
            else: # Otherwise, build a general context
                context_for_llm = "The user is asking a general question about laptops."
                if st.session_state.last_user_search_query: # Add previous search if any
                    context_for_llm += f" Their previous search query was: '{st.session_state.last_user_search_query}'."
                if st.session_state.retrieved_products: # Mention if recommendations were shown
                     context_for_llm += " They were recently shown some laptop recommendations."
            
            # Call Ollama chat interaction with the prepared context
            response = ollama_chat_interaction(
                prompt=user_chat_input,
                chat_history=st.session_state.chat_history, # Pass the full history
                context=context_for_llm
            )
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            st.rerun() # Rerun to display the new assistant message in the sidebar

