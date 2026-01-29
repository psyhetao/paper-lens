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


def annotate_pdf(input_path, annotations_json, output_path):
    try:
        doc = fitz.open(input_path)

        # Load annotations (highlights) only
        if os.path.exists(annotations_json):
            with open(annotations_json, 'r', encoding='utf-8') as f:
                annotations = json.load(f)
        else:
            annotations = json.loads(annotations_json)

        # Process highlights ONLY
        for ann in annotations:
            page_num = ann.get("page", 1) - 1
            if page_num < 0 or page_num >= len(doc):
                continue

            page = doc[page_num]
            text_to_highlight = ann.get("text", "")
            ann_type = ann.get("type", "background")

            if text_to_highlight:
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
        print("Usage: python annotate_pdf.py <input.pdf> <annotations.json> <output.pdf>")
        sys.exit(1)

    input_pdf = sys.argv[1]
    ann_json = sys.argv[2]
    output_pdf = sys.argv[3]

    if annotate_pdf(input_pdf, ann_json, output_pdf):
        print(f"Success: {output_pdf}")
    else:
        sys.exit(1)
