
# retrieval.py
from embedding_utils import generate_ollama_embeddings, cosine_similarity, VECTOR_STORE
from config import TOP_N_RESULTS

def retrieve_top_products(query_text):
    """
    Retrieves top N products from the VECTOR_STORE based on semantic similarity to the query_text.
    Returns a list of product dictionaries with an added 'similarity_score'.
    """
    if not query_text:
        return []
        
    if not VECTOR_STORE["embeddings"] or not VECTOR_STORE["product_data"]:
        print("Error: Vector store is not built or is empty. Cannot retrieve products.")
        return []

    query_embedding_list = generate_ollama_embeddings([query_text])
    if not query_embedding_list or not query_embedding_list[0]:
        print("Could not generate embedding for the query. Cannot retrieve products.")
        return []
    query_embedding = query_embedding_list[0]

    similarities = []
    for i, product_embedding in enumerate(VECTOR_STORE["embeddings"]):
        if not product_embedding: # Skip if any product embedding was invalid
            continue
        similarity = cosine_similarity(query_embedding, product_embedding)
        # Add the original product data along with its similarity score
        # We make a copy of the product dict to avoid modifying the original in VECTOR_STORE
        product_with_score = VECTOR_STORE["product_data"][i].copy() 
        product_with_score['similarity_score'] = similarity
        similarities.append(product_with_score)

    # Sort products by similarity score in descending order
    similarities.sort(key=lambda x: x['similarity_score'], reverse=True)
    
    return similarities[:TOP_N_RESULTS]

if __name__ == '__main__':
    # For testing retrieval.py independently
    # This requires Ollama server, models, and a built vector store.
    # You'd typically call build_vector_store first.
    
    # Mock building the vector store for testing purposes here:
    from embedding_utils import build_vector_store # For testing
    from data_loader import load_products # For testing
    
    print("Testing retrieval module...")
    test_products = load_products()
    if test_products:
        print(f"Loaded {len(test_products)} products for test.")
        # Build store with a small subset for speed
        if build_vector_store(test_products[:10]): 
            print("Vector store built for testing retrieval.")
            
            sample_query = "laptop for programming"
            print(f"\nRetrieving products for query: '{sample_query}'")
            results = retrieve_top_products(sample_query)
            
            if results:
                print(f"\nFound {len(results)} products:")
                for i, prod in enumerate(results):
                    print(f"  {i+1}. {prod.get('product_name', 'N/A')} (Score: {prod.get('similarity_score', 0.0):.4f})")
                    print(f"     Desc: {prod.get('description', 'N/A')[:60]}...")
            else:
                print("No products retrieved for the sample query.")
        else:
            print("Could not build vector store for retrieval test.")
    else:
        print("Could not load products for retrieval test.")
