import pdfplumber
import sys
import json

def extract_text(pdf_path, start_page=None, end_page=None):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            pages = pdf.pages
            if start_page is not None:
                pages = pages[start_page-1:end_page]
            
            content = []
            for page in pages:
                content.append({
                    "page": page.page_number,
                    "text": page.extract_text()
                })
            return content
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding='utf-8')
    if len(sys.argv) < 2:
        print("Usage: python extract_quotes.py <pdf_path> [start_page] [end_page]")
        sys.exit(1)
    
    pdf = sys.argv[1]
    start = int(sys.argv[2]) if len(sys.argv) > 2 else None
    end = int(sys.argv[3]) if len(sys.argv) > 3 else None
    
    result = extract_text(pdf, start, end)
    if result:
        print(json.dumps(result, ensure_ascii=False))
    else:
        sys.exit(1)
