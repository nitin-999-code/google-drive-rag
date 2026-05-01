from sentence_transformers import SentenceTransformer

# Load model once globally
model = SentenceTransformer('all-MiniLM-L6-v2')

def generate_embeddings(chunks):
    """
    Convert list of text chunks into embeddings.
    Return numpy array.
    """
    if not chunks:
        import numpy as np
        return np.array([])
        
    embeddings = model.encode(chunks)
    return embeddings
