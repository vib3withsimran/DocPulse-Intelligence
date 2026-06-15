import os
from classifier import DocumentClassifier

# Retrieve API key from environment, or fall back to dummy string
api_key = os.environ.get("GROQ_API_KEY", "your-groq-api-key")

classifier = DocumentClassifier(api_key=api_key)

test_text = "INVOICE #123\nDate: Jan 1, 2024\nTotal: $500"
result = classifier.classify(test_text, "invoice.pdf")

print(f"Type: {result['document_type']}")
print(f"Sensitivity: {result['sensitivity']}")
print(f"Has tables: {result['has_tables']}")
if "error" in result:
    print(f"\nNote: Fallback configuration was used: {result['error']}")
else:
    print("\nStatus: Successfully classified using Groq LLM!")
