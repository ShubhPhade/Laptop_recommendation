# # # app.py
# # import streamlit as st
# # from config import PRODUCT_NAME_COLUMN, DESCRIPTION_COLUMN, TOP_N_RESULTS
# # from data_loader import load_products
# # from embedding_utils import build_vector_store, VECTOR_STORE
# # from llm_services import parse_query_with_llm, ollama_chat_interaction, generate_enhanced_description
# # from retrieval import retrieve_top_products

# # # --- Page Configuration ---
# # st.set_page_config(page_title="Product Recommender AI", layout="wide")

# # # --- Initialization & State Management ---
# # def initialize_session_state():
# #     """Initializes variables in Streamlit's session state."""
# #     if "products_loaded" not in st.session_state:
# #         st.session_state.products_loaded = False
# #     if "vector_store_built" not in st.session_state:
# #         st.session_state.vector_store_built = False
# #     if "all_products" not in st.session_state:
# #         st.session_state.all_products = []
# #     if "retrieved_products" not in st.session_state:
# #         st.session_state.retrieved_products = []
# #     if "chat_history" not in st.session_state:
# #         st.session_state.chat_history = [] # List of {"role": "user/assistant", "content": "..."}
# #     if "current_product_context_for_chat" not in st.session_state:
# #         st.session_state.current_product_context_for_chat = ""

# # initialize_session_state()

# # # --- Load Data and Build Vector Store (once per session) ---
# # if not st.session_state.products_loaded:
# #     with st.spinner("Loading product data... Please wait."):
# #         st.session_state.all_products = load_products()
# #         if st.session_state.all_products:
# #             st.session_state.products_loaded = True
# #             st.success(f"Loaded {len(st.session_state.all_products)} products.")
# #         else:
# #             st.error("Failed to load product data. Please check the CSV file and configurations.")
# #             st.stop() # Stop execution if data loading fails

# # if st.session_state.products_loaded and not st.session_state.vector_store_built:
# #     with st.spinner("Building product knowledge base (vector store)... This may take a few moments."):
# #         if build_vector_store(st.session_state.all_products):
# #             st.session_state.vector_store_built = True
# #             st.success("Product knowledge base ready!")
# #         else:
# #             st.error("Failed to build the vector store. Product search might not work correctly. Ensure Ollama is running and models are pulled.")
# #             # Optionally stop or allow proceeding with limited functionality

# # # --- UI Layout ---
# # st.title("🛍️ AI-Powered Product Recommender")
# # st.markdown("Describe what you're looking for, and I'll help you find suitable products!")

# # # --- Main Search Area ---
# # search_col, control_col = st.columns([3,1])

# # with search_col:
# #     user_query = st.text_input("Enter your product query (e.g., 'budget laptop for remote work'):", key="main_query_input")

# # with control_col:
# #     st.write("") # Spacer
# #     st.write("") # Spacer
# #     search_button = st.button("🔍 Search Products", type="primary", use_container_width=True, disabled=not st.session_state.vector_store_built)

# # if search_button and user_query:
# #     st.session_state.chat_history = [] # Reset chat for new search
# #     st.session_state.retrieved_products = []
# #     st.session_state.current_product_context_for_chat = ""

# #     with st.spinner("Thinking and searching..."):
# #         # 1. Parse query with LLM
# #         parsed_query = parse_query_with_llm(user_query)
# #         st.info(f"Refined search intent: {parsed_query}")

# #         # 2. Retrieve products
# #         retrieved = retrieve_top_products(parsed_query)
# #         st.session_state.retrieved_products = retrieved

# #     if st.session_state.retrieved_products:
# #         st.success(f"Found {len(st.session_state.retrieved_products)} relevant products!")
        
# #         # Prepare context for chat
# #         context_list = []
# #         for i, prod in enumerate(st.session_state.retrieved_products):
# #             name = prod.get(PRODUCT_NAME_COLUMN, 'N/A')
# #             desc_snippet = prod.get(DESCRIPTION_COLUMN, 'N/A')[:100] + "..."
# #             context_list.append(f"Product {i+1}: {name} (Similarity: {prod.get('similarity_score',0):.2f}). Snippet: {desc_snippet}")
# #         st.session_state.current_product_context_for_chat = "\n".join(context_list)

# #     else:
# #         st.warning("No products found matching your refined query. Try rephrasing or being more general.")

# # # --- Display Retrieved Products ---
# # if st.session_state.retrieved_products:
# #     st.subheader("Top Recommendations:")
# #     cols = st.columns(TOP_N_RESULTS if st.session_state.retrieved_products else 1) # Create columns for products

# #     for i, product in enumerate(st.session_state.retrieved_products):
# #         # Determine which column to use, cycle if more products than TOP_N_RESULTS (though usually they match)
# #         current_col = cols[i % len(cols)] 
# #         with current_col:
# #             with st.container(border=True):
# #                 prod_name = product.get(PRODUCT_NAME_COLUMN, "N/A")
# #                 prod_desc = product.get(DESCRIPTION_COLUMN, "No description available.")
# #                 prod_score = product.get('similarity_score', 0.0)

# #                 st.markdown(f"**{i+1}. {prod_name}**")
# #                 st.caption(f"Relevance Score: {prod_score:.3f}")
# #                 st.markdown(f"<small>{prod_desc[:150]}...</small>", unsafe_allow_html=True)
                
# #                 # Button to generate enhanced description
# #                 if st.button(f"✨ Enhance Desc. for '{prod_name[:20]}...'", key=f"enhance_{product.get(PRODUCT_ID_COLUMN, i)}", use_container_width=True):
# #                     with st.spinner(f"Generating enhanced description for {prod_name}..."):
# #                         enhanced_desc = generate_enhanced_description(product)
# #                         st.session_state[f"enhanced_desc_{i}"] = enhanced_desc
                
# #                 if f"enhanced_desc_{i}" in st.session_state:
# #                     with st.expander("View Enhanced Description", expanded=True):
# #                         st.markdown(st.session_state[f"enhanced_desc_{i}"])


# # # --- Chat / Follow-up Section ---
# # if st.session_state.retrieved_products or st.session_state.chat_history: # Show chat if products were found OR if there's ongoing chat
# #     st.markdown("---")
# #     st.subheader("💬 Chat with AI Assistant")

# #     # Display chat messages
# #     for message in st.session_state.chat_history:
# #         with st.chat_message(message["role"]):
# #             st.markdown(message["content"])

# #     # User input for chat
# #     if prompt := st.chat_input("Ask a follow-up question about the products or type 'new search'...", disabled=not st.session_state.vector_store_built):
# #         if prompt.lower() == "new search":
# #             st.session_state.retrieved_products = []
# #             st.session_state.chat_history = []
# #             st.session_state.current_product_context_for_chat = ""
# #             st.rerun()

# #         # Add user message to chat history
# #         st.session_state.chat_history.append({"role": "user", "content": prompt})
# #         with st.chat_message("user"):
# #             st.markdown(prompt)

# #         # Prepare messages for LLM
# #         messages_for_llm = []
# #         if st.session_state.current_product_context_for_chat and not any(m['role'] == 'system' for m in st.session_state.chat_history):
# #              # Add system prompt with product context if not already there (or if chat was just reset)
# #             system_prompt_content = (
# #                 "You are a helpful AI assistant. The user has been shown some products. "
# #                 "Here is a summary of the retrieved products:\n"
# #                 f"{st.session_state.current_product_context_for_chat}\n"
# #                 "Answer the user's follow-up questions based on this context if relevant, or use your general knowledge. "
# #                 "If asked for more details about a specific product from the list, try to use the context. "
# #                 "If the user asks to describe a product not in the list, say you don't have info on that specific one from the recent search."
# #             )
# #             messages_for_llm.append({"role": "system", "content": system_prompt_content})
        
# #         messages_for_llm.extend(st.session_state.chat_history)


# #         with st.chat_message("assistant"):
# #             with st.spinner("Assistant is thinking..."):
# #                 response_content = ollama_chat_interaction(messages_for_llm)
# #                 st.markdown(response_content)
        
# #         # Add assistant response to chat history
# #         st.session_state.chat_history.append({"role": "assistant", "content": response_content})

# # elif not st.session_state.vector_store_built:
# #     st.warning("Knowledge base is not ready. Please ensure Ollama is running and models are available.")

# # st.markdown("---")
# # st.caption("Powered by Ollama and Streamlit")








# # app.py
# import streamlit as st
# # Ensure PRODUCT_ID_COLUMN is imported from config
# from config import PRODUCT_NAME_COLUMN, DESCRIPTION_COLUMN, TOP_N_RESULTS, PRODUCT_ID_COLUMN
# from data_loader import load_products
# from embedding_utils import build_vector_store, VECTOR_STORE # VECTOR_STORE is not directly used in app.py but build_vector_store populates it.
# from llm_services import parse_query_with_llm, ollama_chat_interaction, generate_enhanced_description
# from retrieval import retrieve_top_products

# # --- Page Configuration ---
# st.set_page_config(page_title="Product Recommender AI", layout="wide")

# # --- Initialization & State Management ---
# def initialize_session_state():
#     """Initializes variables in Streamlit's session state."""
#     if "products_loaded" not in st.session_state:
#         st.session_state.products_loaded = False
#     if "vector_store_built" not in st.session_state:
#         st.session_state.vector_store_built = False
#     if "all_products" not in st.session_state:
#         st.session_state.all_products = []
#     if "retrieved_products" not in st.session_state:
#         st.session_state.retrieved_products = []
#     if "chat_history" not in st.session_state:
#         st.session_state.chat_history = [] # List of {"role": "user/assistant", "content": "..."}
#     if "current_product_context_for_chat" not in st.session_state:
#         st.session_state.current_product_context_for_chat = ""

# initialize_session_state()

# # --- Load Data and Build Vector Store (once per session) ---
# if not st.session_state.products_loaded:
#     with st.spinner("Loading product data... Please wait."):
#         st.session_state.all_products = load_products()
#         if st.session_state.all_products:
#             st.session_state.products_loaded = True
#             st.success(f"Loaded {len(st.session_state.all_products)} products.")
#         else:
#             st.error("Failed to load product data. Please check the CSV file and configurations (config.py). Ensure column names match.")
#             st.stop() # Stop execution if data loading fails

# if st.session_state.products_loaded and not st.session_state.vector_store_built:
#     with st.spinner("Building product knowledge base (vector store)... This may take a few moments."):
#         if build_vector_store(st.session_state.all_products):
#             st.session_state.vector_store_built = True
#             st.success("Product knowledge base ready!")
#         else:
#             st.error("Failed to build the vector store. Product search might not work correctly. Ensure Ollama is running and models are pulled.")
#             # Optionally stop or allow proceeding with limited functionality

# # --- UI Layout ---
# st.title("🛍️ AI-Powered Product Recommender")
# st.markdown("Describe what you're looking for, and I'll help you find suitable products!")

# # --- Main Search Area ---
# search_col, control_col = st.columns([3,1])

# with search_col:
#     user_query = st.text_input("Enter your product query (e.g., 'budget laptop for remote work'):", key="main_query_input")

# with control_col:
#     st.write("") # Spacer
#     st.write("") # Spacer
#     search_button = st.button("🔍 Search Products", type="primary", use_container_width=True, disabled=not st.session_state.vector_store_built)

# if search_button and user_query:
#     st.session_state.chat_history = [] # Reset chat for new search
#     st.session_state.retrieved_products = []
#     st.session_state.current_product_context_for_chat = ""

#     with st.spinner("Thinking and searching..."):
#         # 1. Parse query with LLM
#         parsed_query = parse_query_with_llm(user_query)
#         st.info(f"Refined search intent: {parsed_query}")

#         # 2. Retrieve products
#         retrieved = retrieve_top_products(parsed_query)
#         st.session_state.retrieved_products = retrieved

#     if st.session_state.retrieved_products:
#         st.success(f"Found {len(st.session_state.retrieved_products)} relevant products!")
        
#         # Prepare context for chat
#         context_list = []
#         for i, prod in enumerate(st.session_state.retrieved_products):
#             name = prod.get(PRODUCT_NAME_COLUMN, 'N/A')
#             desc_snippet = prod.get(DESCRIPTION_COLUMN, 'N/A')[:100] + "..."
#             context_list.append(f"Product {i+1}: {name} (Similarity: {prod.get('similarity_score',0):.2f}). Snippet: {desc_snippet}")
#         st.session_state.current_product_context_for_chat = "\n".join(context_list)

#     else:
#         st.warning("No products found matching your refined query. Try rephrasing or being more general.")

# # --- Display Retrieved Products ---
# if st.session_state.retrieved_products:
#     st.subheader("Top Recommendations:")
#     # Adjust number of columns dynamically based on TOP_N_RESULTS or number of products
#     num_display_cols = min(len(st.session_state.retrieved_products), TOP_N_RESULTS)
#     if num_display_cols > 0:
#         cols = st.columns(num_display_cols)
#     else:
#         cols = [st] # Fallback to main column if no products (though this block won't run)


#     for i, product in enumerate(st.session_state.retrieved_products):
#         current_col = cols[i % num_display_cols] if num_display_cols > 0 else st
#         with current_col:
#             with st.container(border=True):
#                 prod_name = product.get(PRODUCT_NAME_COLUMN, "N/A")
#                 prod_desc = product.get(DESCRIPTION_COLUMN, "No description available.")
#                 prod_score = product.get('similarity_score', 0.0)

#                 st.markdown(f"**{i+1}. {prod_name}**")
#                 st.caption(f"Relevance Score: {prod_score:.3f}")
#                 st.markdown(f"<small>{prod_desc[:150]}...</small>", unsafe_allow_html=True)
                
#                 # Robust key generation for the button
#                 # Use product ID if available, otherwise fallback to index
#                 # This is where the error was reported.
#                 button_id_part = product.get(PRODUCT_ID_COLUMN) # Try to get the product ID
#                 if button_id_part is None: # If product ID is missing or None
#                     button_id_part = f"index_{i}" # Fallback to index
#                     # st.caption(f"Debug: Using index {i} for button key as product ID is missing.") # Optional: for debugging

#                 button_key = f"enhance_{button_id_part}"

#                 if st.button(f"✨ Enhance Desc. for '{prod_name[:20]}...'", key=button_key, use_container_width=True):
#                     with st.spinner(f"Generating enhanced description for {prod_name}..."):
#                         enhanced_desc = generate_enhanced_description(product)
#                         st.session_state[f"enhanced_desc_{button_key}"] = enhanced_desc # Use button_key for session state too
                
#                 if f"enhanced_desc_{button_key}" in st.session_state:
#                     with st.expander("View Enhanced Description", expanded=True):
#                         st.markdown(st.session_state[f"enhanced_desc_{button_key}"])


# # --- Chat / Follow-up Section ---
# if st.session_state.retrieved_products or st.session_state.chat_history: 
#     st.markdown("---")
#     st.subheader("💬 Chat with AI Assistant")

#     for message in st.session_state.chat_history:
#         with st.chat_message(message["role"]):
#             st.markdown(message["content"])

#     if prompt := st.chat_input("Ask a follow-up question or type 'new search'...", disabled=not st.session_state.vector_store_built):
#         if prompt.lower() == "new search":
#             st.session_state.retrieved_products = []
#             st.session_state.chat_history = []
#             st.session_state.current_product_context_for_chat = ""
#             # Clear enhanced descriptions from session state
#             for key in list(st.session_state.keys()):
#                 if key.startswith("enhanced_desc_"):
#                     del st.session_state[key]
#             st.rerun()

#         st.session_state.chat_history.append({"role": "user", "content": prompt})
#         with st.chat_message("user"):
#             st.markdown(prompt)

#         messages_for_llm = []
#         # Add system prompt with product context if it's the start of a follow-up session
#         is_first_follow_up = not any(m['role'] == 'system' and "retrieved products" in m['content'] for m in st.session_state.chat_history[:-1])

#         if st.session_state.current_product_context_for_chat and is_first_follow_up :
#             system_prompt_content = (
#                 "You are a helpful AI assistant. The user has been shown some products. "
#                 "Here is a summary of the retrieved products:\n"
#                 f"{st.session_state.current_product_context_for_chat}\n"
#                 "Answer the user's follow-up questions based on this context if relevant, or use your general knowledge. "
#                 "If asked for more details about a specific product from the list, try to use the context. "
#             )
#             messages_for_llm.append({"role": "system", "content": system_prompt_content})
        
#         messages_for_llm.extend(st.session_state.chat_history)


#         with st.chat_message("assistant"):
#             with st.spinner("Assistant is thinking..."):
#                 response_content = ollama_chat_interaction(messages_for_llm)
#                 st.markdown(response_content)
        
#         st.session_state.chat_history.append({"role": "assistant", "content": response_content})

# elif not st.session_state.vector_store_built:
#     st.warning("Knowledge base is not ready. Please ensure Ollama is running and models are available.")

# st.markdown("---")
# st.caption("Powered by Ollama and Streamlit")






# ================================================================================================

# app.py
import streamlit as st
from config import PRODUCT_NAME_COLUMN, DESCRIPTION_COLUMN, TOP_N_RESULTS, PRODUCT_ID_COLUMN
from data_loader import load_products
from embedding_utils import build_vector_store # VECTOR_STORE is populated by this
from llm_services import parse_query_with_llm, ollama_chat_interaction, generate_enhanced_description
from retrieval import retrieve_top_products

# --- Page Configuration ---
st.set_page_config(page_title="Laptop Recommender AI", layout="wide") # Updated title

# --- Initialization & State Management ---
def initialize_session_state():
    """Initializes variables in Streamlit's session state."""
    if "products_loaded" not in st.session_state:
        st.session_state.products_loaded = False
    if "vector_store_built" not in st.session_state:
        st.session_state.vector_store_built = False
    if "all_products" not in st.session_state:
        st.session_state.all_products = []
    if "retrieved_products" not in st.session_state:
        st.session_state.retrieved_products = []
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "current_product_context_for_chat" not in st.session_state:
        st.session_state.current_product_context_for_chat = ""
    if "last_user_query_category_mismatch" not in st.session_state: # Flag for non-laptop queries
        st.session_state.last_user_query_category_mismatch = False


initialize_session_state()

# --- Load Data and Build Vector Store (once per session) ---
if not st.session_state.products_loaded:
    with st.spinner("Loading product data... Please wait."):
        st.session_state.all_products = load_products()
        if st.session_state.all_products:
            st.session_state.products_loaded = True
            # Assuming all products are laptops as per user statement.
            st.success(f"Loaded {len(st.session_state.all_products)} laptop products from the database.")
        else:
            st.error("Failed to load product data. Please check the CSV file and configurations (config.py). Ensure column names match.")
            st.stop()

if st.session_state.products_loaded and not st.session_state.vector_store_built:
    with st.spinner("Building laptop knowledge base (vector store)... This may take a few moments."):
        if build_vector_store(st.session_state.all_products):
            st.session_state.vector_store_built = True
            st.success("Laptop knowledge base ready!")
        else:
            st.error("Failed to build the vector store. Product search might not work correctly. Ensure Ollama is running and models are pulled.")

# --- UI Layout ---
st.title("🛍️ AI-Powered Laptop Recommender") # Updated title
st.markdown("Describe the laptop you're looking for, and I'll help you find suitable options from our database!") # Updated description

# --- Main Search Area ---
search_col, control_col = st.columns([3,1])

with search_col:
    user_query = st.text_input("Enter your laptop query (e.g., 'budget laptop for remote work'):", key="main_query_input")

with control_col:
    st.write("")
    st.write("")
    search_button = st.button("🔍 Search Laptops", type="primary", use_container_width=True, disabled=not st.session_state.vector_store_built) # Updated button text

if search_button and user_query:
    st.session_state.chat_history = []
    st.session_state.retrieved_products = []
    st.session_state.current_product_context_for_chat = ""
    st.session_state.last_user_query_category_mismatch = False # Reset mismatch flag

    # Heuristic to check if user is asking for a non-laptop item
    non_laptop_keywords = ["washing machine", "refrigerator", "phone", "smartphone", "television", "tv", "camera", "t-shirt", "shoes", "book", "microwave", "oven", "tablet"] # Added more
    query_is_for_non_laptop = any(keyword in user_query.lower() for keyword in non_laptop_keywords)
    # Keywords that indicate a laptop query
    laptop_keywords = ["laptop", "notebook", "ultrabook", "macbook", "chromebook", "pc", "computer"]
    query_mentions_laptop_explicitly = any(keyword in user_query.lower() for keyword in laptop_keywords)


    if query_is_for_non_laptop and not query_mentions_laptop_explicitly:
        st.warning("It looks like you're asking for a product other than a laptop. Currently, this system only has information about laptops. If you'd like to search for laptops, please refine your query.")
        st.session_state.last_user_query_category_mismatch = True # Set mismatch flag
        # Optionally, we can decide not to proceed with the search at all for non-laptop items
        # For now, we'll let it search, but the user is warned.
        # To stop search:
        # st.session_state.retrieved_products = [] # Ensure no products are shown
        # user_query = "" # Clear query to prevent search if button is pressed again without change
        # st.stop() # Or just don't proceed to the search block
    
    if not st.session_state.last_user_query_category_mismatch: # Proceed with search only if not a clear non-laptop query or if it mentions laptops
        with st.spinner("Thinking and searching for laptops..."):
            parsed_query = parse_query_with_llm(user_query)
            st.info(f"Refined search intent for laptops: {parsed_query}")
            retrieved = retrieve_top_products(parsed_query)
            st.session_state.retrieved_products = retrieved

        if st.session_state.retrieved_products:
            st.success(f"Found {len(st.session_state.retrieved_products)} relevant laptops!")
            context_list = []
            for i, prod in enumerate(st.session_state.retrieved_products):
                name = prod.get(PRODUCT_NAME_COLUMN, 'N/A')
                desc_snippet = prod.get(DESCRIPTION_COLUMN, 'N/A')[:100] + "..."
                context_list.append(f"Laptop {i+1}: {name} (Similarity: {prod.get('similarity_score',0):.2f}). Snippet: {desc_snippet}")
            st.session_state.current_product_context_for_chat = "\n".join(context_list)
        else:
            st.warning("Sorry, no laptops were found in our database that match your query. Please try rephrasing or being more general.")
    elif not st.session_state.retrieved_products: # If it was a non-laptop query and we decided to not search, this ensures no "no products found" message if already warned.
        pass


# --- Display Retrieved Products ---
if st.session_state.retrieved_products:
    st.subheader("Top Laptop Recommendations:")
    num_display_cols = min(len(st.session_state.retrieved_products), TOP_N_RESULTS)
    cols = st.columns(num_display_cols) if num_display_cols > 0 else [st]

    for i, product in enumerate(st.session_state.retrieved_products):
        current_col = cols[i % num_display_cols] if num_display_cols > 0 else st
        with current_col:
            with st.container(border=True):
                prod_name = product.get(PRODUCT_NAME_COLUMN, "N/A")
                prod_desc = product.get(DESCRIPTION_COLUMN, "No description available.")
                prod_score = product.get('similarity_score', 0.0)

                st.markdown(f"**{i+1}. {prod_name}**")
                st.caption(f"Relevance Score: {prod_score:.3f}")
                st.markdown(f"<small>{prod_desc[:150]}...</small>", unsafe_allow_html=True)
                
                button_id_part = product.get(PRODUCT_ID_COLUMN)
                if button_id_part is None:
                    button_id_part = f"index_{i}"
                button_key = f"enhance_{button_id_part}"

                if st.button(f"✨ Enhance Desc. for '{prod_name[:20]}...'", key=button_key, use_container_width=True):
                    with st.spinner(f"Generating enhanced description for {prod_name}..."):
                        enhanced_desc = generate_enhanced_description(product)
                        st.session_state[f"enhanced_desc_{button_key}"] = enhanced_desc
                
                if f"enhanced_desc_{button_key}" in st.session_state:
                    with st.expander("View Enhanced Description", expanded=True):
                        st.markdown(st.session_state[f"enhanced_desc_{button_key}"])

# --- Chat / Follow-up Section ---
# Show chat if products were retrieved OR if there's an ongoing chat OR if a non-laptop query was attempted (to allow AI to clarify)
if st.session_state.retrieved_products or st.session_state.chat_history or st.session_state.last_user_query_category_mismatch:
    st.markdown("---")
    st.subheader("💬 Chat with Laptop AI Assistant")

    # Display chat messages from history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input for chat
    if prompt := st.chat_input("Ask a follow-up about these laptops or type 'new search'...", disabled=not st.session_state.vector_store_built):
        if prompt.lower() == "new search":
            st.session_state.retrieved_products = []
            st.session_state.chat_history = []
            st.session_state.current_product_context_for_chat = ""
            st.session_state.last_user_query_category_mismatch = False
            for key in list(st.session_state.keys()): # Clear previous enhanced descriptions
                if key.startswith("enhanced_desc_"):
                    del st.session_state[key]
            st.rerun()

        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Prepare messages for LLM, including the system prompt about laptop-only data
        messages_for_llm = []
        
        system_prompt_content = (
            "You are a helpful AI assistant for a laptop recommendation system. "
            "Important: Your knowledge base *only contains information about laptops*. "
            "If the user asks about non-laptop products, politely inform them that you can only assist with laptop-related queries. Do not attempt to find non-laptop products. "
        )
        if st.session_state.current_product_context_for_chat: # If laptops were retrieved
            system_prompt_content += (
                "The user has been shown some laptops based on their recent query. "
                "Here is a summary of those retrieved laptops:\n"
                f"{st.session_state.current_product_context_for_chat}\n"
                "Answer the user's follow-up questions based on this laptop context if relevant. "
            )
        elif st.session_state.last_user_query_category_mismatch: # If user previously asked for non-laptop
             system_prompt_content += "The user may have previously asked for a non-laptop item. Reiterate that you can only help with laptops if they ask again for non-laptops."
        else: # General chat, no specific products shown yet or a failed search for laptops
             system_prompt_content += "Focus on answering questions about laptops in general."

        messages_for_llm.append({"role": "system", "content": system_prompt_content})
        
        # Add actual chat history, excluding any previous identical system prompts to avoid redundancy
        # This simple check might need refinement for more complex system prompt updates.
        for msg in st.session_state.chat_history:
            if not (msg["role"] == "system" and "only contains information about laptops" in msg["content"]):
                 messages_for_llm.append(msg)


        with st.chat_message("assistant"):
            with st.spinner("Assistant is thinking..."):
                response_content = ollama_chat_interaction(messages_for_llm)
                st.markdown(response_content)
        
        st.session_state.chat_history.append({"role": "assistant", "content": response_content})

elif not st.session_state.vector_store_built:
    st.warning("Laptop knowledge base is not ready. Please ensure Ollama is running and models are available.")

st.markdown("---")
st.caption("Powered by Ollama and Streamlit")

