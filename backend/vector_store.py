import os
import chromadb
from chromadb.utils import embedding_functions
import uuid

class VectorStore:
    def __init__(self):
        # Create persistent database in a fixed location inside the backend directory
        db_path = os.path.join(os.path.dirname(__file__), "chroma_db")
        self.client = chromadb.PersistentClient(path=db_path)
        
        # Use free embedding model (runs locally)
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        
        # Create or get collection
        self.collection = self.client.get_or_create_collection(
            name="documents",
            embedding_function=self.embedding_fn
        )
    
    def add_document(self, text: str, metadata: dict):
        """Store document in vector database"""
        doc_id = str(uuid.uuid4())
        
        self.collection.add(
            documents=[text],
            metadatas=[metadata],
            ids=[doc_id]
        )
        return doc_id
    
    def search(self, query: str, top_k: int = 3):
        """Find most relevant documents"""
        results = self.collection.query(
            query_texts=[query],
            n_results=top_k
        )
        
        # Format results
        documents = []
        if results and results.get('documents') and results['documents'][0]:
            for i in range(len(results['documents'][0])):
                documents.append({
                    'text': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i],
                    'relevance_score': 1 - results['distances'][0][i]  # Convert distance to score
                })
        
        return documents
