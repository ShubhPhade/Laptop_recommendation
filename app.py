# # # app.py
# # import streamlit as st
# # from config import (
# #     PRODUCT_NAME_COLUMN, DESCRIPTION_COLUMN, TOP_N_RESULTS, PRODUCT_ID_COLUMN,
# #     PRICE_COLUMN, BRAND_COLUMN, RAM_COLUMN, STORAGE_COLUMN, DISPLAY_SIZE_COLUMN, OS_COLUMN,
# #     RATING_COLUMN, BATTERY_LIFE_COLUMN # Import new constants for display
# # )
# # from data_loader import load_products
# # from embedding_utils import build_vector_store
# # from llm_services import parse_query_with_llm, ollama_chat_interaction, generate_enhanced_description
# # from retrieval import retrieve_top_products

# # # --- Page Configuration ---
# # st.set_page_config(page_title="Laptop Recommender AI", layout="wide")

# # # --- Initialization & State Management ---
# # def initialize_session_state():
# #     if "products_loaded" not in st.session_state: st.session_state.products_loaded = False
# #     if "vector_store_built" not in st.session_state: st.session_state.vector_store_built = False
# #     if "all_products" not in st.session_state: st.session_state.all_products = []
# #     if "retrieved_products" not in st.session_state: st.session_state.retrieved_products = []
# #     if "chat_history" not in st.session_state: st.session_state.chat_history = []
# #     if "current_product_context_for_chat" not in st.session_state: st.session_state.current_product_context_for_chat = ""
# #     if "last_user_query_category_mismatch" not in st.session_state: st.session_state.last_user_query_category_mismatch = False
# #     if "debug_info" not in st.session_state: st.session_state.debug_info = {}

# # initialize_session_state()

# # # --- Load Data and Build Vector Store ---
# # if not st.session_state.products_loaded:
# #     with st.spinner("Loading product data... Please wait."):
# #         st.session_state.all_products = load_products()
# #         if st.session_state.all_products:
# #             st.session_state.products_loaded = True
# #             st.success(f"Loaded {len(st.session_state.all_products)} laptop products.")
# #         else:
# #             st.error("Failed to load product data. Check CSV and config.py.")
# #             st.stop()

# # if st.session_state.products_loaded and not st.session_state.vector_store_built:
# #     with st.spinner("Building laptop knowledge base (vector store)... This may take time."):
# #         if build_vector_store(st.session_state.all_products):
# #             st.session_state.vector_store_built = True
# #             st.success("Laptop knowledge base ready!")
# #         else:
# #             st.error("Failed to build vector store. Ensure Ollama is running.")

# # # --- UI Layout ---
# # st.title("🛍️ AI-Powered Laptop Recommender")
# # st.markdown("Describe the laptop you're looking for, and I'll find suitable options!")
# # search_col, control_col = st.columns([3,1])
# # with search_col:
# #     user_query = st.text_input("Enter your laptop query (e.g., 'Dell laptop 16GB RAM for gaming'):", key="main_query_input")
# # with control_col:
# #     st.write("")
# #     st.write("")
# #     search_button = st.button("🔍 Search Laptops", type="primary", use_container_width=True, disabled=not st.session_state.vector_store_built)

# # debug_message_area = st.empty()

# # if search_button and user_query:
# #     st.session_state.chat_history = []
# #     st.session_state.retrieved_products = []
# #     st.session_state.current_product_context_for_chat = ""
# #     st.session_state.last_user_query_category_mismatch = False
# #     st.session_state.debug_info = {}

# #     non_laptop_keywords = ["washing machine", "refrigerator", "fridge", "phone", "tv", "camera", "t-shirt", "shoes", "book", "microwave", "oven", "tablet", "desktop"]
# #     laptop_keywords = ["laptop", "notebook", "ultrabook", "macbook", "chromebook", "pc", "computer", "netbook"]
    
# #     query_lower = user_query.lower()
# #     query_is_for_non_laptop = any(keyword in query_lower for keyword in non_laptop_keywords)
# #     query_mentions_laptop_explicitly = any(keyword in query_lower for keyword in laptop_keywords)

# #     st.session_state.debug_info['user_query'] = user_query
# #     st.session_state.debug_info['query_is_for_non_laptop_flag'] = query_is_for_non_laptop
# #     st.session_state.debug_info['query_mentions_laptop_explicitly_flag'] = query_mentions_laptop_explicitly

# #     if query_is_for_non_laptop and not query_mentions_laptop_explicitly:
# #         st.warning("This system only has information about laptops. Please refine your query for laptops.")
# #         st.session_state.last_user_query_category_mismatch = True
# #         st.session_state.retrieved_products = []
# #     else:
# #         with st.spinner("Thinking and searching for laptops..."):
# #             parsed_query = parse_query_with_llm(user_query)
# #             st.session_state.debug_info['parsed_query_by_llm'] = parsed_query
            
# #             parsed_query_is_non_laptop = any(keyword in parsed_query.lower() for keyword in non_laptop_keywords)
# #             parsed_query_mentions_laptop = any(keyword in parsed_query.lower() for keyword in laptop_keywords)
# #             st.session_state.debug_info['parsed_query_is_non_laptop_flag'] = parsed_query_is_non_laptop
# #             st.session_state.debug_info['parsed_query_mentions_laptop_flag'] = parsed_query_mentions_laptop

# #             if parsed_query_is_non_laptop and not parsed_query_mentions_laptop:
# #                 st.warning(f"The refined search query ('{parsed_query}') seems non-laptop. I only search laptops.")
# #                 st.session_state.last_user_query_category_mismatch = True
# #                 st.session_state.retrieved_products = []
# #             else:
# #                 st.info(f"Refined search intent for laptops: {parsed_query}")
# #                 retrieved = retrieve_top_products(parsed_query)
# #                 st.session_state.retrieved_products = retrieved

# #                 if st.session_state.retrieved_products:
# #                     st.success(f"Found {len(st.session_state.retrieved_products)} relevant laptops!")
# #                     context_list = []
# #                     for i, prod in enumerate(st.session_state.retrieved_products):
# #                         name = prod.get(PRODUCT_NAME_COLUMN, 'N/A')
# #                         brand = prod.get(BRAND_COLUMN, '')
# #                         price = prod.get(PRICE_COLUMN, '')
# #                         ram = prod.get(RAM_COLUMN, '')
# #                         storage = prod.get(STORAGE_COLUMN, '')
# #                         display = prod.get(DISPLAY_SIZE_COLUMN, '')
# #                         battery = prod.get(BATTERY_LIFE_COLUMN, '')
                        
# #                         context_entry = f"Laptop {i+1}: {name}"
# #                         if brand: context_entry += f" (Brand: {brand})"
# #                         if price: context_entry += f" (Price: {price})"
# #                         if ram: context_entry += f" ({ram} RAM)"
# #                         if storage: context_entry += f" ({storage})"
# #                         if display: context_entry += f" ({display})"
# #                         context_entry += f" (Similarity: {prod.get('similarity_score',0):.2f})."
# #                         context_list.append(context_entry)
# #                     st.session_state.current_product_context_for_chat = "\n".join(context_list)
# #                 else:
# #                     st.warning("Sorry, no laptops found matching your query. Try rephrasing.")
    
# #     if st.session_state.debug_info:
# #         with debug_message_area.container():
# #             st.subheader("Debug Information:")
# #             for key, value in st.session_state.debug_info.items():
# #                 st.text(f"{key}: {value}")

# # # --- Display Retrieved Products ---
# # if st.session_state.retrieved_products:
# #     st.subheader("Top Laptop Recommendations:")
# #     num_display_cols = min(len(st.session_state.retrieved_products), TOP_N_RESULTS)
# #     cols = st.columns(num_display_cols) if num_display_cols > 0 else [st]

# #     for i, product in enumerate(st.session_state.retrieved_products):
# #         current_col = cols[i % num_display_cols] if num_display_cols > 0 else st
# #         with current_col:
# #             with st.container(border=True, height=450): # Added fixed height
# #                 prod_name = product.get(PRODUCT_NAME_COLUMN, "N/A")
# #                 prod_desc_short = product.get(DESCRIPTION_COLUMN, "No description.")[:100] + "..."
                
# #                 st.markdown(f"**{i+1}. {prod_name}**")
# #                 st.caption(f"Relevance: {product.get('similarity_score', 0.0):.3f}")

# #                 # Displaying more attributes
# #                 details_md = ""
# #                 if product.get(BRAND_COLUMN): details_md += f"**Brand:** {product.get(BRAND_COLUMN)}\n"
# #                 if product.get(PRICE_COLUMN): details_md += f"**Price:** {product.get(PRICE_COLUMN)}\n"
# #                 if product.get(RAM_COLUMN): details_md += f"**RAM:** {product.get(RAM_COLUMN)}\n"
# #                 if product.get(STORAGE_COLUMN): details_md += f"**Storage:** {product.get(STORAGE_COLUMN)}\n"
# #                 if product.get(DISPLAY_SIZE_COLUMN): details_md += f"**Display:** {product.get(DISPLAY_SIZE_COLUMN)}\n"
# #                 if product.get(OS_COLUMN): details_md += f"**OS:** {product.get(OS_COLUMN)}\n"
# #                 if product.get(RATING_COLUMN) and product.get(RATING_COLUMN,'').lower() not in ['nan', 'not found','']:
# #                     details_md += f"**Rating:** {product.get(RATING_COLUMN)}\n"
# #                 if product.get(BATTERY_LIFE_COLUMN): details_md += f"**Battery Life** {product.get(BATTERY_LIFE_COLUMN)}\n"
                    
                
# #                 st.markdown(f"<small>{details_md}</small>", unsafe_allow_html=True)
# #                 with st.expander("Short Description"):
# #                     st.markdown(f"<small>{prod_desc_short}</small>", unsafe_allow_html=True)
                
# #                 button_id_part = product.get(PRODUCT_ID_COLUMN, f"index_{i}")
# #                 button_key = f"enhance_{button_id_part}"

# #                 if st.button(f"✨ Enhance Desc.", key=button_key, use_container_width=True):
# #                     with st.spinner(f"Generating enhanced description..."):
# #                         enhanced_desc = generate_enhanced_description(product) # product is already a dict
# #                         st.session_state[f"enhanced_desc_{button_key}"] = enhanced_desc
                
# #                 if f"enhanced_desc_{button_key}" in st.session_state:
# #                     with st.expander("View Enhanced Description", expanded=False): # Default to collapsed
# #                         st.markdown(st.session_state[f"enhanced_desc_{button_key}"])

# # # --- Chat / Follow-up Section ---
# # if st.session_state.retrieved_products or st.session_state.chat_history or st.session_state.last_user_query_category_mismatch:
# #     st.markdown("---")
# #     st.subheader("💬 Chat with Laptop AI Assistant")

# #     for message in st.session_state.chat_history:
# #         with st.chat_message(message["role"]):
# #             st.markdown(message["content"])

# #     if prompt := st.chat_input("Ask a follow-up or type 'new search'...", disabled=not st.session_state.vector_store_built):
# #         if prompt.lower() == "new search":
# #             st.session_state.retrieved_products = []
# #             st.session_state.chat_history = []
# #             st.session_state.current_product_context_for_chat = ""
# #             st.session_state.last_user_query_category_mismatch = False
# #             st.session_state.debug_info = {}
# #             debug_message_area.empty()
# #             for key in list(st.session_state.keys()): 
# #                 if key.startswith("enhanced_desc_"): del st.session_state[key]
# #             st.rerun()

# #         st.session_state.chat_history.append({"role": "user", "content": prompt})
# #         with st.chat_message("user"): st.markdown(prompt)

# #         messages_for_llm = []
# #         system_prompt_content = (
# #             "You are a helpful AI assistant for a laptop recommendation system. "
# #             "Important: Your knowledge base *only contains information about laptops*. "
# #             "If the user asks about non-laptop products, politely inform them that you can only assist with laptop-related queries. "
# #         )
# #         if st.session_state.current_product_context_for_chat: 
# #             system_prompt_content += (
# #                 "The user has been shown some laptops. Here is a summary:\n"
# #                 f"{st.session_state.current_product_context_for_chat}\n"
# #                 "Answer follow-up questions based on this laptop context. You can also use the individual attributes of each laptop (like Brand, Price, RAM, Storage, Display, OS, Rating) to answer specific questions if the user asks for them."
# #             )
# #         elif st.session_state.last_user_query_category_mismatch: 
# #              system_prompt_content += "The user may have previously asked for a non-laptop item. Reiterate that you only handle laptops if they ask again for non-laptops."
# #         else: 
# #              system_prompt_content += "Focus on answering questions about laptops or helping formulate a laptop search query."

# #         messages_for_llm.append({"role": "system", "content": system_prompt_content})
        
# #         for msg in st.session_state.chat_history:
# #             if not (msg["role"] == "system" and "only contains information about laptops" in msg["content"]):
# #                  messages_for_llm.append(msg)

# #         with st.chat_message("assistant"):
# #             with st.spinner("Assistant is thinking..."):
# #                 response_content = ollama_chat_interaction(messages_for_llm)
# #                 st.markdown(response_content)
        
# #         st.session_state.chat_history.append({"role": "assistant", "content": response_content})

# # elif not st.session_state.vector_store_built:
# #     st.warning("Laptop knowledge base not ready. Ensure Ollama is running.")

# # st.markdown("---")
# # st.caption("Powered by Ollama and Streamlit")
# # app.py
# import streamlit as st
# from config import (
#     PRODUCT_NAME_COLUMN, DESCRIPTION_COLUMN, TOP_N_RESULTS, PRODUCT_ID_COLUMN,
#     PRICE_COLUMN, BRAND_COLUMN, RAM_COLUMN, STORAGE_COLUMN, DISPLAY_SIZE_COLUMN, OS_COLUMN,
#     RATING_COLUMN, BATTERY_LIFE_COLUMN
# )
# from data_loader import load_products
# from embedding_utils import build_vector_store
# from llm_services import parse_query_with_llm, ollama_chat_interaction, generate_enhanced_description
# from retrieval import retrieve_top_products

# # --- Page Configuration ---
# st.set_page_config(page_title="Laptop Recommender AI", layout="wide")

# # --- Initialization & State Management ---
# def initialize_session_state():
#     if "products_loaded" not in st.session_state: st.session_state.products_loaded = False
#     if "vector_store_built" not in st.session_state: st.session_state.vector_store_built = False
#     if "all_products" not in st.session_state: st.session_state.all_products = []
#     if "retrieved_products" not in st.session_state: st.session_state.retrieved_products = []
#     if "chat_history" not in st.session_state:
#         st.session_state.chat_history = [{"role": "assistant", "content": "Hello! How can I help you find a laptop today?"}]
#     if "current_product_context_for_chat" not in st.session_state: st.session_state.current_product_context_for_chat = ""
#     if "last_user_query_category_mismatch" not in st.session_state: st.session_state.last_user_query_category_mismatch = False
#     if "last_user_search_query" not in st.session_state: st.session_state.last_user_search_query = ""

# initialize_session_state()

# # --- Load Data and Build Vector Store ---
# if not st.session_state.products_loaded:
#     with st.spinner("Loading product data... Please wait."):
#         st.session_state.all_products = load_products()
#         if st.session_state.all_products is not None and not st.session_state.all_products.empty: # Check if DataFrame and not empty
#             st.session_state.products_loaded = True
#             st.success(f"Loaded {len(st.session_state.all_products)} laptop products.")
#         else:
#             st.error("Failed to load product data or no data found. Check CSV and config.py.")
#             st.stop() # Stop execution if data loading fails

# if st.session_state.products_loaded and not st.session_state.vector_store_built:
#     with st.spinner("Building laptop knowledge base (vector store)... This may take some time."):
#         if build_vector_store(st.session_state.all_products): # Assumes this function uses/stores the vector store appropriately
#             st.session_state.vector_store_built = True
#             st.success("Laptop knowledge base ready!")
#         else:
#             st.error("Failed to build vector store. Ensure Ollama is running or embedding model is accessible.")
#             # Optionally, you might want to st.stop() here too if vector store is critical

# # --- UI Layout ---
# st.title("🛍️ AI-Powered Laptop Recommender")
# st.markdown("Describe the laptop you're looking for (e.g., 'lightweight Dell laptop with 16GB RAM for programming'), and I'll find suitable options!")

# search_col, control_col = st.columns([3,1])
# with search_col:
#     user_query = st.text_input(
#         "Enter your laptop query:",
#         key="main_query_input",
#         placeholder="e.g., 'Dell laptop 16GB RAM for gaming'"
#     )
# with control_col:
#     st.write("") # For alignment
#     st.write("") # For alignment
#     search_button = st.button(
#         "🔍 Search Laptops",
#         type="primary",
#         use_container_width=True,
#         disabled=not st.session_state.vector_store_built # Disable if vector store isn't ready
#     )

# # --- Search Logic and Product Retrieval ---
# if search_button and user_query:
#     st.session_state.chat_history = [{"role": "assistant", "content": "I'm looking for laptops based on your new query. Ask me anything once the results are up!"}] # Reset chat for new search
#     st.session_state.retrieved_products = []
#     st.session_state.current_product_context_for_chat = ""
#     st.session_state.last_user_query_category_mismatch = False
#     st.session_state.last_user_search_query = user_query

#     non_laptop_keywords = [
#         "washing machine", "refrigerator", "fridge", "phone", "smartphone",
#         "television", "tv", "camera", "t-shirt", "shoes", "book",
#         "microwave", "oven", "tablet", "desktop", "monitor", "keyboard", "mouse",
#         "printer", "projector", "speaker", "headphone", "earphone", "watch",
#         "fan", "air conditioner", "ac", "cooler", "heater", "furniture", "sofa", "chair", "table", "bed",
#         "clothes", "clothing", "apparel", "garment", "dress", "jeans", "shirt", "pant", "toy"
#     ]
#     laptop_keywords = ["laptop", "notebook", "ultrabook", "macbook", "chromebook", "pc", "computer", "netbook"]

#     query_lower = user_query.lower()
#     # Check if any non-laptop keyword is a WHOLE WORD in the query
#     query_is_for_non_laptop = any(f" {keyword} " in f" {query_lower} " or \
#                                   query_lower.startswith(keyword + " ") or \
#                                   query_lower.endswith(" " + keyword) or \
#                                   query_lower == keyword for keyword in non_laptop_keywords)
#     query_mentions_laptop_explicitly = any(f" {keyword} " in f" {query_lower} " or \
#                                            query_lower.startswith(keyword + " ") or \
#                                            query_lower.endswith(" " + keyword) or \
#                                            query_lower == keyword for keyword in laptop_keywords)

#     if query_is_for_non_laptop and not query_mentions_laptop_explicitly:
#         st.warning("It seems you're looking for something other than a laptop. This system specializes in laptop recommendations. Please refine your query for laptops.")
#         st.session_state.last_user_query_category_mismatch = True
#         st.session_state.retrieved_products = [] # Ensure no products are shown
#     else:
#         st.session_state.last_user_query_category_mismatch = False
#         with st.spinner("🧠 Analyzing your query with AI and searching for the best laptops..."):
#             # 1. Parse query with LLM
#             # Assumes parse_query_with_llm returns an enhanced query string or structured data for retrieval.
#             # If it returns None or fails, we might fall back to user_query.
#             parsed_query_data = parse_query_with_llm(user_query)

#             query_for_retrieval = user_query # Default to original query
#             if parsed_query_data:
#                 # This part depends on what parse_query_with_llm returns.
#                 # If it's a string:
#                 if isinstance(parsed_query_data, str):
#                     query_for_retrieval = parsed_query_data
#                     st.info(f"Using AI-enhanced query: \"{query_for_retrieval}\"")
#                 # If it's a dict (e.g., {'query': '...', 'filters': {...}}):
#                 elif isinstance(parsed_query_data, dict) and "query" in parsed_query_data:
#                     query_for_retrieval = parsed_query_data["query"]
#                     # You might also handle filters here if retrieve_top_products supports them
#                     st.info(f"Using AI-parsed query components.")
#                 # Add more conditions based on the actual structure of parsed_query_data
#             else:
#                 st.warning("Could not enhance query using LLM, using your original query for search.")

#             # 2. Retrieve top products
#             # Assumes retrieve_top_products takes a query text (and optionally other params like filters, or all_products for post-filtering)
#             # and uses the vector store implicitly (e.g., loads it from a file or a global variable set by build_vector_store)
#             retrieved_items = retrieve_top_products(
#                 query_text=query_for_retrieval, # Use the (potentially enhanced) query
#                 # products_df=st.session_state.all_products, # Pass if retrieve_top_products needs it for filtering/lookup
#                 # vector_store=st.session_state.get('vector_store_object'), # Pass if build_vector_store returns it and you store it
#                 top_n=TOP_N_RESULTS
#             )

#             if retrieved_items is not None and len(retrieved_items) > 0:
#                 st.session_state.retrieved_products = retrieved_items
#                 st.success(f"Found {len(st.session_state.retrieved_products)} potential laptop matches!")
#             else:
#                 st.info("No laptops found matching your refined query. You could try being more general or rephrasing.")
#                 st.session_state.retrieved_products = []


# # --- Display Retrieved Products ---
# if st.session_state.retrieved_products:
#     st.markdown("---")
#     st.subheader("✨ Here are your AI-curated laptop recommendations:")

#     for i, product in enumerate(st.session_state.retrieved_products):
#         # Ensure product is a dictionary (or Series, convert to dict)
#         if not isinstance(product, dict):
#             try:
#                 product_dict = dict(product) #Handles Pandas Series if products are Series
#             except (TypeError, ValueError):
#                 st.error(f"Skipping a product due to unexpected data format: {type(product)}")
#                 continue
#         else:
#             product_dict = product

#         # Use .get() for safer access to dictionary keys
#         product_name = product_dict.get(PRODUCT_NAME_COLUMN, "N/A")
#         product_id = product_dict.get(PRODUCT_ID_COLUMN, f"product_{i}") # Fallback ID

#         with st.container(border=True): # Added border to container for better separation
#             col1, col2 = st.columns([1, 2]) # Adjust column ratio as needed

#             with col1:
#                 # Placeholder for image - replace with actual image if available
#                 # st.image(product_dict.get("image_url", "https://placehold.co/300x200/eee/ccc?text=Laptop"), use_column_width=True)
#                 st.markdown(f"##### {product_name}") # Product name as subheader

#             with col2:
#                 price = product_dict.get(PRICE_COLUMN)
#                 brand = product_dict.get(BRAND_COLUMN, "N/A")
#                 ram = product_dict.get(RAM_COLUMN, "N/A")
#                 storage = product_dict.get(STORAGE_COLUMN, "N/A")
#                 display = product_dict.get(DISPLAY_SIZE_COLUMN, "N/A")
#                 os_val = product_dict.get(OS_COLUMN, "N/A") # Renamed to avoid conflict with os module
#                 rating = product_dict.get(RATING_COLUMN, "N/A")
#                 battery = product_dict.get(BATTERY_LIFE_COLUMN, "N/A")

#                 price_display = f"${price:,.2f}" if isinstance(price, (int, float)) else (price if price else "N/A")
#                 st.markdown(f"**Brand:** {brand} | **Price:** {price_display}")
#                 st.markdown(f"**RAM:** {ram} | **Storage:** {storage} | **Display:** {display}\"")
#                 st.markdown(f"**OS:** {os_val} | **Rating:** {rating}/5 | **Battery:** {battery} hrs" if battery != "N/A" else f"**OS:** {os_val} | **Rating:** {rating}/5")

#                 description = product_dict.get(DESCRIPTION_COLUMN, "No description available.")
#                 with st.expander("View Description"):
#                     st.caption(description)

#                 # Optional: AI Enhanced Description (can be slow)
#                 # with st.expander("View AI Enhanced Description"):
#                 #     if st.button(f"Generate AI Description for {product_name[:30]}...", key=f"gen_desc_{product_id}"):
#                 #         enhanced_desc = generate_enhanced_description(product_dict) # Pass the product dictionary
#                 #         st.write(enhanced_desc)

#                 # Chat about this product button
#                 chat_button_key = f"chat_btn_{product_id}_{i}" # Ensure unique key
#                 if st.button(f"💬 Discuss: {product_name[:40]}...", key=chat_button_key, help="Click to ask specific questions about this laptop."):
#                     product_context = f"The user is asking about the {product_name}."
#                     product_context += f"\nKey Details: Price {price_display}, Brand {brand}, RAM {ram}, Storage {storage}, Display {display}, OS {os_val}."
#                     # Add more details as needed for the LLM context
#                     st.session_state.current_product_context_for_chat = product_context
#                     st.session_state.chat_history = [
#                         {"role": "assistant", "content": f"Okay, let's talk about the {product_name}. What specific questions do you have about it?"}
#                     ]
#                     st.rerun() # Rerun to update chat interface immediately and focus chat

#             # st.markdown("---") # Use container border instead of markdown line

# # --- Chat Interface (General or Product-Specific) ---
# # Placed in the sidebar
# st.sidebar.title("🤖 Laptop Chat Assistant")

# if not st.session_state.vector_store_built:
#     st.sidebar.warning("Knowledge base is not yet built. Chat will be enabled once it's ready.")
# else:
#     if st.session_state.current_product_context_for_chat:
#         # Extracting product name for display in a more readable way
#         try:
#             current_product_name = st.session_state.current_product_context_for_chat.splitlines()[0].split("about the ")[1].rstrip('.')
#             st.sidebar.info(f"Chatting about: **{current_product_name}**")
#         except IndexError: # Fallback if parsing context string fails
#             st.sidebar.info("Chatting about a specific product.")

#     elif st.session_state.retrieved_products:
#          st.sidebar.info("You can ask about the recommended laptops or general laptop questions.")
#     else:
#         st.sidebar.info("Search for laptops to get recommendations. You can then chat about them or ask general questions.")

#     # Display chat history
#     for message in st.session_state.chat_history:
#         with st.sidebar.chat_message(message["role"]):
#             st.markdown(message["content"])

#     # Chat input
#     user_chat_input = st.sidebar.chat_input(
#         "Ask a follow-up question...",
#         key="chat_input",
#         disabled=not st.session_state.vector_store_built # Disable if not ready
#     )

#     if user_chat_input:
#         st.session_state.chat_history.append({"role": "user", "content": user_chat_input})
#         with st.sidebar.chat_message("user"): # Display user message immediately
#             st.markdown(user_chat_input)

#         with st.sidebar.spinner("AI is thinking..."):
#             # Construct context for Ollama
#             context_for_llm = st.session_state.current_product_context_for_chat # Product specific context

#             if not context_for_llm: # If no specific product, build general context
#                 context_for_llm = "The user is asking a general question about laptops."
#                 if st.session_state.last_user_search_query:
#                     context_for_llm += f" Their previous search query was: '{st.session_state.last_user_search_query}'."
#                 if st.session_state.retrieved_products:
#                      context_for_llm += " They were recently shown some laptop recommendations."

#             # Call Ollama chat interaction
#             # Assumes ollama_chat_interaction takes the latest prompt, full chat history, and context string
#             response = ollama_chat_interaction(
#                 prompt=user_chat_input,
#                 chat_history=st.session_state.chat_history, # Pass the full history
#                 context=context_for_llm
#             )
#             st.session_state.chat_history.append({"role": "assistant", "content": response})
#             # Rerun to display the new assistant message in the sidebar
#             st.rerun()




# ============================================================================================================

# # app.py
# import streamlit as st
# from config import (
#     PRODUCT_NAME_COLUMN, DESCRIPTION_COLUMN, TOP_N_RESULTS, PRODUCT_ID_COLUMN,
#     PRICE_COLUMN, BRAND_COLUMN, RAM_COLUMN, STORAGE_COLUMN, DISPLAY_SIZE_COLUMN, OS_COLUMN,
#     RATING_COLUMN, BATTERY_LIFE_COLUMN
# )
# from data_loader import load_products
# from embedding_utils import build_vector_store
# from llm_services import parse_query_with_llm, ollama_chat_interaction, generate_enhanced_description
# from retrieval import retrieve_top_products

# # --- Page Configuration ---
# st.set_page_config(page_title="Laptop Recommender AI", layout="wide")

# # --- Initialization & State Management ---
# def initialize_session_state():
#     if "products_loaded" not in st.session_state: st.session_state.products_loaded = False
#     if "vector_store_built" not in st.session_state: st.session_state.vector_store_built = False
#     if "all_products" not in st.session_state: st.session_state.all_products = [] # Initialize as list
#     if "retrieved_products" not in st.session_state: st.session_state.retrieved_products = []
#     if "chat_history" not in st.session_state:
#         st.session_state.chat_history = [{"role": "assistant", "content": "Hello! How can I help you find a laptop today?"}]
#     if "current_product_context_for_chat" not in st.session_state: st.session_state.current_product_context_for_chat = ""
#     if "last_user_query_category_mismatch" not in st.session_state: st.session_state.last_user_query_category_mismatch = False
#     if "last_user_search_query" not in st.session_state: st.session_state.last_user_search_query = ""

# initialize_session_state()

# # --- Load Data and Build Vector Store ---
# if not st.session_state.products_loaded:
#     with st.spinner("Loading product data... Please wait."):
#         st.session_state.all_products = load_products() # This should return a list of product dicts or a DataFrame
        
#         # CORRECTED CHECK:
#         # If load_products() is intended to return a list of dictionaries:
#         if st.session_state.all_products is not None and len(st.session_state.all_products) > 0:
#             st.session_state.products_loaded = True
#             st.success(f"Loaded {len(st.session_state.all_products)} laptop products.")
#         # If load_products() is intended to return a Pandas DataFrame (and was mistakenly returning a list):
#         # Make sure load_products() actually returns a DataFrame. If it does, the original check was:
#         # if st.session_state.all_products is not None and not st.session_state.all_products.empty:
#         # For now, assuming it's a list as per the error.
#         else:
#             st.error("Failed to load product data or no data found. Check CSV and config.py, and ensure load_products() returns a non-empty list or DataFrame.")
#             st.stop() # Stop execution if data loading fails

# if st.session_state.products_loaded and not st.session_state.vector_store_built:
#     with st.spinner("Building laptop knowledge base (vector store)... This may take some time."):
#         # Ensure build_vector_store can handle the format of st.session_state.all_products
#         # (e.g., a list of dicts or a DataFrame)
#         if build_vector_store(st.session_state.all_products): 
#             st.session_state.vector_store_built = True
#             st.success("Laptop knowledge base ready!")
#         else:
#             st.error("Failed to build vector store. Ensure Ollama is running or embedding model is accessible.")
#             # Optionally, you might want to st.stop() here too if vector store is critical

# # --- UI Layout ---
# st.title("🛍️ AI-Powered Laptop Recommender")
# st.markdown("Describe the laptop you're looking for (e.g., 'lightweight Dell laptop with 16GB RAM for programming'), and I'll find suitable options!")

# search_col, control_col = st.columns([3,1])
# with search_col:
#     user_query = st.text_input(
#         "Enter your laptop query:",
#         key="main_query_input",
#         placeholder="e.g., 'Dell laptop 16GB RAM for gaming'"
#     )
# with control_col:
#     st.write("") # For alignment
#     st.write("") # For alignment
#     search_button = st.button(
#         "🔍 Search Laptops",
#         type="primary",
#         use_container_width=True,
#         disabled=not st.session_state.vector_store_built # Disable if vector store isn't ready
#     )

# # --- Search Logic and Product Retrieval ---
# if search_button and user_query:
#     st.session_state.chat_history = [{"role": "assistant", "content": "I'm looking for laptops based on your new query. Ask me anything once the results are up!"}] # Reset chat for new search
#     st.session_state.retrieved_products = []
#     st.session_state.current_product_context_for_chat = ""
#     st.session_state.last_user_query_category_mismatch = False
#     st.session_state.last_user_search_query = user_query

#     non_laptop_keywords = [
#         "washing machine", "refrigerator", "fridge", "phone", "smartphone",
#         "television", "tv", "camera", "t-shirt", "shoes", "book",
#         "microwave", "oven", "tablet", "desktop", "monitor", "keyboard", "mouse",
#         "printer", "projector", "speaker", "headphone", "earphone", "watch",
#         "fan", "air conditioner", "ac", "cooler", "heater", "furniture", "sofa", "chair", "table", "bed",
#         "clothes", "clothing", "apparel", "garment", "dress", "jeans", "shirt", "pant", "toy"
#     ]
#     laptop_keywords = ["laptop", "notebook", "ultrabook", "macbook", "chromebook", "pc", "computer", "netbook"]

#     query_lower = user_query.lower()
#     # Check if any non-laptop keyword is a WHOLE WORD in the query
#     query_is_for_non_laptop = any(f" {keyword} " in f" {query_lower} " or \
#                                   query_lower.startswith(keyword + " ") or \
#                                   query_lower.endswith(" " + keyword) or \
#                                   query_lower == keyword for keyword in non_laptop_keywords)
#     query_mentions_laptop_explicitly = any(f" {keyword} " in f" {query_lower} " or \
#                                            query_lower.startswith(keyword + " ") or \
#                                            query_lower.endswith(" " + keyword) or \
#                                            query_lower == keyword for keyword in laptop_keywords)

#     if query_is_for_non_laptop and not query_mentions_laptop_explicitly:
#         st.warning("It seems you're looking for something other than a laptop. This system specializes in laptop recommendations. Please refine your query for laptops.")
#         st.session_state.last_user_query_category_mismatch = True
#         st.session_state.retrieved_products = [] # Ensure no products are shown
#     else:
#         st.session_state.last_user_query_category_mismatch = False
#         with st.spinner("🧠 Analyzing your query with AI and searching for the best laptops..."):
#             # 1. Parse query with LLM
#             parsed_query_data = parse_query_with_llm(user_query)

#             query_for_retrieval = user_query 
#             if parsed_query_data:
#                 if isinstance(parsed_query_data, str):
#                     query_for_retrieval = parsed_query_data
#                     st.info(f"Using AI-enhanced query: \"{query_for_retrieval}\"")
#                 elif isinstance(parsed_query_data, dict) and "query" in parsed_query_data:
#                     query_for_retrieval = parsed_query_data["query"]
#                     st.info(f"Using AI-parsed query components.")
#             else:
#                 st.warning("Could not enhance query using LLM, using your original query for search.")

#             # 2. Retrieve top products
#             # CORRECTED: Removed the 'top_n' argument.
#             # Assumes retrieve_top_products uses TOP_N_RESULTS from config.py internally.
#             retrieved_items = retrieve_top_products(
#                 query_text=query_for_retrieval
#             )

#             if retrieved_items is not None and len(retrieved_items) > 0:
#                 st.session_state.retrieved_products = retrieved_items # retrieved_items should be a list of dicts
#                 st.success(f"Found {len(st.session_state.retrieved_products)} potential laptop matches!")
#             else:
#                 st.info("No laptops found matching your refined query. You could try being more general or rephrasing.")
#                 st.session_state.retrieved_products = []


# # --- Display Retrieved Products ---
# if st.session_state.retrieved_products: # This is a list
#     st.markdown("---")
#     st.subheader("✨ Here are your AI-curated laptop recommendations:")

#     for i, product_dict in enumerate(st.session_state.retrieved_products): # Iterate directly if it's a list of dicts
#         # Ensure product_dict is a dictionary. If retrieve_top_products sometimes returns other types, add handling.
#         if not isinstance(product_dict, dict):
#             st.error(f"Skipping a product due to unexpected data format: {type(product_dict)}. Expected a dictionary.")
#             continue

#         product_name = product_dict.get(PRODUCT_NAME_COLUMN, "N/A")
#         # Ensure product_id is unique if PRODUCT_ID_COLUMN might be missing or not unique
#         product_id_value = product_dict.get(PRODUCT_ID_COLUMN)
#         product_id_for_key = product_id_value if product_id_value is not None else f"product_fallback_{i}"


#         with st.container(border=True):
#             col1, col2 = st.columns([1, 2]) 

#             with col1:
#                 st.markdown(f"##### {product_name}") 

#             with col2:
#                 price = product_dict.get(PRICE_COLUMN)
#                 brand = product_dict.get(BRAND_COLUMN, "N/A")
#                 ram = product_dict.get(RAM_COLUMN, "N/A")
#                 storage = product_dict.get(STORAGE_COLUMN, "N/A")
#                 display = product_dict.get(DISPLAY_SIZE_COLUMN, "N/A")
#                 os_val = product_dict.get(OS_COLUMN, "N/A") 
#                 rating = product_dict.get(RATING_COLUMN, "N/A")
#                 battery = product_dict.get(BATTERY_LIFE_COLUMN, "N/A")

#                 price_display = f"${price:,.2f}" if isinstance(price, (int, float)) else (str(price) if price is not None else "N/A")
#                 st.markdown(f"**Brand:** {brand} | **Price:** {price_display}")
#                 st.markdown(f"**RAM:** {ram} | **Storage:** {storage} | **Display:** {display}\"")
#                 st.markdown(f"**OS:** {os_val} | **Rating:** {rating}/5 | **Battery:** {battery} hrs" if battery not in ["N/A", None, ""] else f"**OS:** {os_val} | **Rating:** {rating}/5")

#                 description = product_dict.get(DESCRIPTION_COLUMN, "No description available.")
#                 with st.expander("View Description"):
#                     st.caption(description)

#                 # Chat about this product button
#                 chat_button_key = f"chat_btn_{product_id_for_key}_{i}" 
#                 if st.button(f"💬 Discuss: {product_name[:40]}...", key=chat_button_key, help="Click to ask specific questions about this laptop."):
#                     product_context = f"The user is asking about the {product_name}."
#                     product_context += f"\nKey Details: Price {price_display}, Brand {brand}, RAM {ram}, Storage {storage}, Display {display}, OS {os_val}."
#                     st.session_state.current_product_context_for_chat = product_context
#                     st.session_state.chat_history = [
#                         {"role": "assistant", "content": f"Okay, let's talk about the {product_name}. What specific questions do you have about it?"}
#                     ]
#                     st.rerun() 

# # --- Chat Interface (General or Product-Specific) ---
# st.sidebar.title("🤖 Laptop Chat Assistant")

# if not st.session_state.vector_store_built:
#     st.sidebar.warning("Knowledge base is not yet built. Chat will be enabled once it's ready.")
# else:
#     if st.session_state.current_product_context_for_chat:
#         try:
#             current_product_name = st.session_state.current_product_context_for_chat.splitlines()[0].split("about the ")[1].rstrip('.')
#             st.sidebar.info(f"Chatting about: **{current_product_name}**")
#         except IndexError: 
#             st.sidebar.info("Chatting about a specific product.")

#     elif st.session_state.retrieved_products:
#          st.sidebar.info("You can ask about the recommended laptops or general laptop questions.")
#     else:
#         st.sidebar.info("Search for laptops to get recommendations. You can then chat about them or ask general questions.")

#     for message in st.session_state.chat_history:
#         with st.sidebar.chat_message(message["role"]):
#             st.markdown(message["content"])

#     user_chat_input = st.sidebar.chat_input(
#         "Ask a follow-up question...",
#         key="chat_input",
#         disabled=not st.session_state.vector_store_built
#     )

#     if user_chat_input:
#         st.session_state.chat_history.append({"role": "user", "content": user_chat_input})
#         with st.sidebar.chat_message("user"): 
#             st.markdown(user_chat_input)

#         with st.spinner("AI is thinking..."):
#             context_for_llm = generate_enhanced_description(st.session_state.current_product_context_for_chat)

#             if not context_for_llm: 
#                 context_for_llm = "The user is asking a general question about laptops."
#                 if st.session_state.last_user_search_query:
#                     context_for_llm += f" Their previous search query was: '{st.session_state.last_user_search_query}'."
#                 if st.session_state.retrieved_products:
#                      context_for_llm += " They were recently shown some laptop recommendations."

#             response = ollama_chat_interaction(
#                 prompt=user_chat_input,
#                 chat_history=st.session_state.chat_history, 
#                 context=context_for_llm
#             )
#             st.session_state.chat_history.append({"role": "assistant", "content": response})
#             st.rerun()






















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

