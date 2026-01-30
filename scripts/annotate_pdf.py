import fitz
import json
import sys
import os

COLORS = {
    "conclusion": (1, 1, 0),       # Yellow
    "method": (0.6, 1, 0.6),      # Green
    "relevant": (0.6, 0.8, 1),    # Blue
    "question": (1, 0.6, 0.6),    # Red
    "quote": (0.9, 0.7, 1),       # Purple
    "background": (1, 0.8, 0.5),  # Orange
}
 

def highlight_text(page, text_to_highlight, ann_type):
    """Highlight specific text in PDF."""
    color = COLORS.get(ann_type, COLORS["background"])
    text_instances = page.search_for(text_to_highlight)
 
    for inst in text_instances:
        highlight = page.add_highlight_annot(inst)
        highlight.set_colors(stroke=color)
        highlight.update()


def add_text_note(page, x, y, text, color=(1, 0.8, 0.5)):
    """Add text note annotation to PDF."""
    point = fitz.Point(x, y)
    annot = page.add_text_annot(point, text)
    annot.set_colors(stroke=color)
    annot.update()
    return annot


def generate_text_notes(analysis_result, text_content):
    """
    自动生成文本注释
    基于分析结果的关键点
    """
    notes = []
    
    if not analysis_result or not text_content:
        return notes
    
    # 规则1:识别研究问题
    research_keywords = ['research question', 'objective', 'aim', 'purpose', 
                      '研究问题', '研究目的', '研究目标']
    for item in text_content:
        page_num = item.get('page', 1)
        text = item.get('text', '')
        text_lower = text.lower()
        
        for keyword in research_keywords:
            if keyword in text_lower:
                notes.append({
                    "page": page_num,
                    "type": "text_note",
                    "text": f"Key: {keyword}",
                    "x": 100,
                    "y": 100 + len(notes) * 50
                })
                break
    
    # 规则2:识别方法论
    method_keywords = ['method', 'methodology', 'approach', 'framework',
                   '方法', '方法论', '框架']
    for item in text_content:
        page_num = item.get('page', 1)
        text = item.get('text', '')
        text_lower = text.lower()
        
        for keyword in method_keywords:
            if keyword in text_lower:
                notes.append({
                    "page": page_num,
                    "type": "text_note",
                    "text": f"Methodology: {keyword}",
                    "x": 100,
                    "y": 100 + len(notes) * 50
                })
                break
    
    # 规则3:识别核心结论
    conclusion_keywords = ['conclusion', 'finding', 'result', 'key result',
                       '结论', '发现', '结果']
    for item in text_content:
        page_num = item.get('page', 1)
        text = item.get('text', '')
        text_lower = text.lower()
        
        for keyword in conclusion_keywords:
            if keyword in text_lower:
                notes.append({
                    "page": page_num,
                    "type": "text_note",
                    "text": f"Conclusion: {keyword}",
                    "x": 100,
                    "y": 100 + len(notes) * 50
                })
                break
    
    return notes


def annotate_pdf(input_path, annotations_json, output_path, auto_generate_notes=False, text_content=None):
    try:
        doc = fitz.open(input_path)
 
        # Load annotations (highlights) only
        if os.path.exists(annotations_json):
            with open(annotations_json, 'r', encoding='utf-8') as f:
                annotations = json.load(f)
        else:
            annotations = json.loads(annotations_json)
        
        # Auto-generate text notes if requested
        if auto_generate_notes and text_content:
            text_notes = generate_text_notes(annotations, text_content)
            annotations.extend(text_notes)
 
        # Process all annotations
        for ann in annotations:
            page_num = ann.get("page", 1) - 1
            if page_num < 0 or page_num >= len(doc):
                continue
 
            page = doc[page_num]
            ann_type = ann.get("type", "background")
            text_to_highlight = ann.get("text", "")
 
            if ann_type == "text_note":
                x = ann.get("x", 100)
                y = ann.get("y", 100)
                text_note = ann.get("text", "")
                add_text_note(page, x, y, text_note)
            elif text_to_highlight:
                highlight_text(page, text_to_highlight, ann_type)
 
        # Save PDF
        doc.save(output_path)
        doc.close()
        return True
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python annotate_pdf.py <input.pdf> <annotations.json> <output.pdf> [--auto-notes]")
        print("  --auto-notes: 自动生成文本注释")
        sys.exit(1)
    
    input_pdf = sys.argv[1]
    ann_json = sys.argv[2]
    output_pdf = sys.argv[3]
    auto_notes = '--auto-notes' in sys.argv
    
    # Auto-generate text notes if requested
    text_content = None
if auto_notes:
        from extract_content import extract_text
        text_content = extract_text(input_pdf)
    
    if annotate_pdf(input_pdf, ann_json, output_pdf, auto_generate_notes=auto_notes, text_content=text_content):
        print(f"Success: {output_pdf}")
    else:
        sys.exit(1)
