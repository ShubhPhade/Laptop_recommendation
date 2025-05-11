# embedding_utils.py
import ollama
import math
from config import EMBEDDING_MODEL, get_text_for_embedding

# This will be our simple in-memory vector store
# For production, consider ChromaDB, FAISS, Weaviate, etc.
VECTOR_STORE = {
    "embeddings": [],    # List of product embeddings
    "product_data": []   # Corresponding list of product data dicts
}

def generate_ollama_embeddings(text_chunks, model_name=EMBEDDING_MODEL):
    """
    Generates vector embeddings for a list of text chunks using Ollama.
    Returns a list of embeddings.
    """
    if not text_chunks:
        return []
    
    all_embeddings = []
    try:
        for i, chunk in enumerate(text_chunks):
            if not chunk or not chunk.strip(): # Skip empty or whitespace-only chunks
                # print(f"Skipping empty chunk at index {i} for embedding.")
                all_embeddings.append([]) # Placeholder for consistent list length if needed, or handle differently
                continue
            response = ollama.embeddings(model=model_name, prompt=chunk)
            all_embeddings.append(response['embedding'])
        # print(f"Generated {sum(1 for emb in all_embeddings if emb)} embeddings out of {len(text_chunks)} chunks.")
    except Exception as e:
        print(f"Error generating Ollama embeddings for model {model_name}: {e}")
        print("Ensure Ollama server is running and the model is pulled.")
        # Depending on desired behavior, you might re-raise or return partial results
    return all_embeddings

def build_vector_store(products):
    """
    Builds an in-memory vector store from the product list.
    Populates VECTOR_STORE.
    """
    global VECTOR_STORE
    print("Building in-memory vector store...")
    VECTOR_STORE["embeddings"] = []
    VECTOR_STORE["product_data"] = []

    texts_to_embed = []
    valid_products_for_embedding = []

    for product in products:
        text = get_text_for_embedding(product)
        if text:
            texts_to_embed.append(text)
            valid_products_for_embedding.append(product)
        else:
            # print(f"Warning: Product ID {product.get(config.PRODUCT_ID_COLUMN, 'N/A')} resulted in empty text for embedding.")
            pass
            
    if not texts_to_embed:
        print("No valid product texts found to generate embeddings for the vector store.")
        return False

    product_embeddings = generate_ollama_embeddings(texts_to_embed)
    
    # Filter out products for which embedding generation might have failed (empty list returned)
    successful_embeddings = []
    corresponding_products = []
    for i, emb in enumerate(product_embeddings):
        if emb: # Check if embedding is not empty
            successful_embeddings.append(emb)
            corresponding_products.append(valid_products_for_embedding[i])

    if successful_embeddings:
        VECTOR_STORE["embeddings"] = successful_embeddings
        VECTOR_STORE["product_data"] = corresponding_products
        print(f"In-memory vector store built with {len(VECTOR_STORE['embeddings'])} product embeddings.")
        return True
    else:
        print("Error: No embeddings were successfully generated. Vector store not built.")
        return False


def cosine_similarity(vec1, vec2):
    """Computes cosine similarity between two vectors."""
    if not vec1 or not vec2 or len(vec1) != len(vec2):
        # print(f"Cosine similarity error: vec1 len {len(vec1) if vec1 else 'None'}, vec2 len {len(vec2) if vec2 else 'None'}")
        return 0.0
    
    dot_product = sum(p * q for p, q in zip(vec1, vec2))
    magnitude1 = math.sqrt(sum(p * p for p in vec1))
    magnitude2 = math.sqrt(sum(q * q for q in vec2))
    
    if not magnitude1 or not magnitude2:
        return 0.0
    return dot_product / (magnitude1 * magnitude2)

if __name__ == '__main__':
    # For testing embedding_utils.py independently
    # This requires Ollama server to be running with the EMBEDDING_MODEL
    print(f"Testing with embedding model: {EMBEDDING_MODEL}")
    sample_texts = [
        "This is a test sentence for embedding.",
        "Another example to generate vector representation."
    ]
    embeddings = generate_ollama_embeddings(sample_texts)
    if embeddings and all(e for e in embeddings): # Check if all embeddings were generated
        print(f"Generated {len(embeddings)} embeddings.")
        print(f"Dimension of first embedding: {len(embeddings[0])}")
        if len(embeddings) > 1:
            sim = cosine_similarity(embeddings[0], embeddings[1])
            print(f"Similarity between the two test sentences: {sim:.4f}")
    else:
        print("Failed to generate embeddings for testing.")

    # Test building vector store (requires data_loader and config)
    # from data_loader import load_products
    # test_products = load_products()
    # if test_products:
    #     if build_vector_store(test_products[:5]): # Test with a few products
    #         print("Vector store built successfully for testing.")
    #         print(f"Number of items in store: {len(VECTOR_STORE['embeddings'])}")
    #     else:
    #         print("Failed to build vector store for testing.")
