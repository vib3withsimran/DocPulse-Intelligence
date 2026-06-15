import os
import pdfplumber
from pdf2image import convert_from_path
import pytesseract
from typing import Dict, List

# Configure Tesseract path
tesseract_path = os.environ.get("TESSERACT_PATH")
if tesseract_path:
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
else:
    # Fallback to default Windows install path if it exists
    default_win_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    if os.path.exists(default_win_path):
        pytesseract.pytesseract.tesseract_cmd = default_win_path

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
        """Extract text and tables from PDF (falls back to OCR for scanned PDFs)"""
        pages_data = []
        poppler_path = os.environ.get("POPPLER_PATH")
        
        with pdfplumber.open(file_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                # Extract regular digital text
                text = page.extract_text() or ""
                
                # Extract tables (important for the assignment!)
                tables = page.extract_tables()
                table_text = ""
                for table in tables:
                    if table:
                        for row in table:
                            table_text += " | ".join(str(cell or "") for cell in row) + "\n"
                
                # If there's no digital text, this is likely a scanned PDF page. Run OCR.
                if not text.strip():
                    try:
                        images = convert_from_path(
                            file_path,
                            first_page=page_num,
                            last_page=page_num,
                            poppler_path=poppler_path
                        )
                        if images:
                            text = pytesseract.image_to_string(images[0])
                    except Exception as ocr_err:
                        text = f"[OCR Failed on Page {page_num}: {str(ocr_err)}]"
                
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
