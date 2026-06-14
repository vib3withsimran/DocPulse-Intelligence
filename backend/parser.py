import pdfplumber
from pdf2image import convert_from_path
import pytesseract
from typing import Dict, List

class DocumentParser:
    """Handles different document types"""
    
    def parse(self, file_path: str, filename: str) -> Dict:
        """Main entry point - decides which parser to use"""
        filename_lower = filename.lower()
        if filename_lower.endswith('.pdf'):
            return self._parse_pdf(file_path)
        elif filename_lower.endswith(('.png', '.jpg', '.jpeg')):
            return self._parse_image(file_path)
        else:
            return self._parse_text(file_path)
    
    def _parse_pdf(self, file_path: str) -> Dict:
        """Extract text and tables from PDF"""
        pages_data = []
        
        with pdfplumber.open(file_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                # Extract regular text
                text = page.extract_text() or ""
                
                # Extract tables (important for the assignment!)
                tables = page.extract_tables()
                table_text = ""
                for table in tables:
                    if table:
                        for row in table:
                            table_text += " | ".join(str(cell or "") for cell in row) + "\n"
                
                pages_data.append({
                    "page_number": page_num,
                    "text": text + "\n" + table_text,
                    "has_tables": len(tables) > 0
                })
        
        return {
            "filename": file_path,
            "total_pages": len(pages_data),
            "pages": pages_data
        }
    
    def _parse_image(self, file_path: str) -> Dict:
        """Use OCR for images/handwriting"""
        text = pytesseract.image_to_string(file_path)
        return {
            "filename": file_path,
            "total_pages": 1,
            "pages": [{"page_number": 1, "text": text, "has_tables": False}]
        }
    
    def _parse_text(self, file_path: str) -> Dict:
        """Simple text files"""
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
        return {
            "filename": file_path,
            "total_pages": 1,
            "pages": [{"page_number": 1, "text": text, "has_tables": False}]
        }
