import os
from vector_store import VectorStore
from rag_agent import RAGAgent

# Load environment variables from .env file
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    with open(dotenv_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)
                os.environ[key.strip()] = val.strip()

api_key = os.environ.get("GROQ_API_KEY")

print("Initializing VectorStore (loading SentenceTransformer)...")
store = VectorStore()

print("\nAdding test documents to VectorStore...")
doc1_id = store.add_document(
    text="ACME Corp Invoice #98765. Date: June 15, 2026. Total Amount Due: $1,250.50. Payment terms: Net 30 days. Bill to: John Doe.",
    metadata={"filename": "invoice_98765.pdf", "page": 1}
)
doc2_id = store.add_document(
    text="This agreement is entered into between ACME Corp and John Doe. It defines the software development consulting terms. The daily rate is set to $500 USD.",
    metadata={"filename": "consulting_agreement.pdf", "page": 1}
)
doc3_id = store.add_document(
    text="The quarterly performance report for Q2 2026 shows a 15% increase in revenue. Growth was driven primarily by cloud service subscriptions and enterprise API integrations.",
    metadata={"filename": "q2_report.pdf", "page": 3}
)
print("Documents added successfully!")

# Test 1: Direct Semantic Search
query = "How much does John Doe owe?"
print(f"\n1. Running semantic search for query: '{query}'...")
search_results = store.search(query, top_k=2)
for idx, res in enumerate(search_results, 1):
    print(f"  Match {idx}:")
    print(f"    Source: {res['metadata']['filename']} (Page {res['metadata']['page']})")
    print(f"    Text: {res['text']}")
    print(f"    Relevance Score: {res['relevance_score']:.4f}")

# Test 2: RAG Answer
if api_key:
    print(f"\n2. Running RAG Agent query using Groq LLM...")
    agent = RAGAgent(api_key=api_key)
    rag_result = agent.answer(query)
    print(f"\n  Answer: {rag_result['answer']}")
    print("\n  Citations:")
    for cit in rag_result['citations']:
        print(f"    - File: {cit['document']} (Page {cit['page']}), Relevance: {cit['relevance']:.4f}")
else:
    print("\n2. RAG Agent query skipped: GROQ_API_KEY not found in .env")
