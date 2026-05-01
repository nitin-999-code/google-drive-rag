import faiss
import numpy as np

# Global in-memory storage
index = None
chunk_mapping = {}  # Map index position to chunk text
chunk_sources = {}  # Map index position to source file name

def initialize_index(dimension):
    """
    Initialize FAISS index.
    """
    global index
    index = faiss.IndexFlatL2(dimension)

def store_embeddings(embeddings, chunks, source_name="unknown"):
    """
    Store embeddings in FAISS index and keep mapping to chunks.
    """
    global index, chunk_mapping, chunk_sources
    
    if len(embeddings) == 0:
        return
        
    if index is None:
        dimension = embeddings.shape[1]
        initialize_index(dimension)
        
    start_idx = index.ntotal
    index.add(np.array(embeddings).astype('float32'))
    
    for i, chunk in enumerate(chunks):
        chunk_mapping[start_idx + i] = chunk
        chunk_sources[start_idx + i] = source_name

def search_similar(query, query_embedding, top_k=5):
    """
    Search vector database for top matching chunks.
    """
    global index, chunk_mapping, chunk_sources
    
    if index is None or index.ntotal == 0:
        return [], []
        
    D, I = index.search(np.array([query_embedding]).astype('float32'), top_k)
    
    results = []
    for i, idx in enumerate(I[0]):
        if idx != -1 and idx in chunk_mapping:
            chunk_text = chunk_mapping[idx]
            source = chunk_sources[idx]
            score = float(D[0][i])
            
            if query.lower() in chunk_text.lower():
                score = score * 0.8
                
            results.append({
                "chunk": chunk_text,
                "source": source,
                "score": score
            })
            
    results.sort(key=lambda x: x["score"])
    
    final_chunks = [r["chunk"] for r in results]
    final_sources = [r["source"] for r in results]
            
    return final_chunks, final_sources
