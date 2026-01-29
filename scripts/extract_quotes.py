import pdfplumber
import pypdfium2 as pdfium
import os
import sys
import json

def extract_text_pdfplumber(pdf_path, start_page=None, end_page=None):
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

def extract_text_pypdfium2(pdf_path, start_page=None, end_page=None):
    try:
        pdf = pdfium.PdfDocument(pdf_path)
        total_pages = len(pdf)
        
        start = start_page - 1 if start_page is not None else 0
        end = end_page if end_page is not None else total_pages
        
        content = []
        for i in range(start, end):
            page = pdf[i]
            textpage = page.get_textpage()
            text = textpage.get_text_range()
            content.append({
                "page": i + 1,
                "text": text
            })
        return content
    except Exception as e:
        print(f"Error: {e}")
        return None

def extract_text(pdf_path, start_page=None, end_page=None, method="pypdfium2"):
    if method == "pypdfium2":
        return extract_text_pypdfium2(pdf_path, start_page, end_page)
    else:
        return extract_text_pdfplumber(pdf_path, start_page, end_page)

def render_page_for_image(pdf_path, page_num, output_dir, scale=2.0):
    try:
        os.makedirs(output_dir, exist_ok=True)
        pdf = pdfium.PdfDocument(pdf_path)
        
        if page_num < 1 or page_num > len(pdf):
            return None
        
        page = pdf[page_num - 1]
        bitmap = page.render(scale=int(scale), rotation=0)
        
        from PIL import Image
        img = bitmap.to_pil()
        
        image_path = os.path.join(output_dir, f"page_{page_num}.png")
        img.save(image_path, "PNG")
        
        return image_path
    except Exception as e:
        print(f"Error rendering page {page_num}: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_quotes.py <pdf_path> [start_page] [end_page] [output_file]")
        sys.exit(1)
    
    pdf = sys.argv[1]
    start = int(sys.argv[2]) if len(sys.argv) > 2 else None
    end = int(sys.argv[3]) if len(sys.argv) > 3 else None
    output_file = sys.argv[4] if len(sys.argv) > 4 else None
    
    result = extract_text(pdf, start, end)
    if result:
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            print(f"Text extracted to {output_file}")
        else:
            print(json.dumps(result, ensure_ascii=False))
    else:
        sys.exit(1)
