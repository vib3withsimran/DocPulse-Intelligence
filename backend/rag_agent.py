from groq import Groq
from vector_store import VectorStore

class RAGAgent:
    def __init__(self, api_key: str):
        self.vector_store = VectorStore()
        self.llm = Groq(api_key=api_key)
    
    def answer(self, question: str) -> dict:
        # Step 1: Search for relevant documents
        relevant_docs = self.vector_store.search(question)
        
        if not relevant_docs:
            return {
                "answer": "I couldn't find relevant information to answer your question.",
                "citations": []
            }
        
        # Step 2: Build context from retrieved documents
        context = ""
        citations = []
        
        for doc in relevant_docs:
            context += f"\nFrom {doc['metadata']['filename']}:\n{doc['text'][:500]}\n"
            citations.append({
                "document": doc['metadata']['filename'],
                "page": doc['metadata'].get('page', 1),
                "relevance": doc['relevance_score']
            })
        
        # Step 3: Ask LLM with context
        prompt = f"""Answer the question based ONLY on the context below.

Context:
{context}

Question: {question}

Answer concisely with specific information from the context.
If the context doesn't contain the answer, say "I don't have enough information."

Answer:"""

        response = self.llm.chat.completions.create(
            model="llama-3.1-8b-instant",  # Updated to active Groq model
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        
        return {
            "answer": response.choices[0].message.content,
            "citations": citations
        }
