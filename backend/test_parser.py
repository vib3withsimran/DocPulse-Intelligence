from parser import DocumentParser

parser = DocumentParser()

# Create a test text file
with open("test.txt", "w") as f:
    f.write("This is a test document.\nIt has two lines.")

result = parser.parse("test.txt", "test.txt")
print(f"Found {result['total_pages']} pages")
print(f"Text: {result['pages'][0]['text']}")
