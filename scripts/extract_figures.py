#!/usr/bin/env python3
"""
智能图表提取模块
根据阅读目的自动筛选和提取 PDF 中的重要图表
"""

import os
import sys
import json
import re
import pypdfium2 as pdfium
from pathlib import Path

# 阅读目的对应的图表提取策略
PURPOSE_STRATEGIES = {
    "quick_scan": {"max_figures": 2, "priority": ["conclusion", "abstract"]},
    "deep_dive": {"max_figures": 5, "priority": ["all"]},
    "method_focus": {"max_figures": 4, "priority": ["method", "framework", "algorithm"]},
    "review_prep": {"max_figures": 10, "priority": ["all"]},
    "brainstorm": {"max_figures": 3, "priority": ["concept", "framework", "overview"]},
}

# 图表标题识别模式
FIGURE_PATTERNS = [
    r"(?:Figure|Fig\.?|图)\s*(\d+)",
    r"(?:Table|表)\s*(\d+)",
    r"(?:Chart|图表)\s*(\d+)",
    r"(?:Diagram|框图)\s*(\d+)",
]

# 区域关键词 (用于判断图表重要性)
REGION_KEYWORDS = {
    "abstract": ["abstract", "摘要", "summary"],
    "conclusion": ["conclusion", "结论", "findings", "results", "发现"],
    "method": ["method", "methodology", "approach", "方法", "框架", "framework"],
    "introduction": ["introduction", "引言", "背景", "background"],
}


def detect_figures_in_page(page_text, page_num):
    """检测页面中的图表引用"""
    figures = []
    for pattern in FIGURE_PATTERNS:
        matches = re.finditer(pattern, page_text, re.IGNORECASE)
        for match in matches:
            fig_num = match.group(1)
            fig_type = "figure" if "fig" in match.group(0).lower() or "图" in match.group(0) else "table"
            figures.append({
                "page": page_num,
                "number": fig_num,
                "type": fig_type,
                "match_text": match.group(0),
                "position": match.start()
            })
    return figures


def detect_page_region(page_text):
    """检测页面所属区域 (abstract/method/conclusion 等)"""
    text_lower = page_text.lower()
    for region, keywords in REGION_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text_lower:
                return region
    return "body"


def calculate_figure_importance(figure_info, page_text, purpose):
    """计算图表重要性评分"""
    score = 0
    strategy = PURPOSE_STRATEGIES.get(purpose, PURPOSE_STRATEGIES["deep_dive"])
    priority_regions = strategy["priority"]
    
    # 区域匹配加分
    page_region = detect_page_region(page_text)
    if "all" in priority_regions or page_region in priority_regions:
        score += 10
    
    # 首页/末页加分 (通常包含关键图)
    if figure_info["page"] <= 2:
        score += 5
    
    # 被多次引用的图表加分
    fig_ref_pattern = rf"(?:Figure|Fig\.?|图)\s*{figure_info['number']}"
    ref_count = len(re.findall(fig_ref_pattern, page_text, re.IGNORECASE))
    score += ref_count * 2
    
    # Table 在 method_focus 时加分
    if purpose == "method_focus" and figure_info["type"] == "table":
        score += 3
    
    return score


def render_page_image(pdf_path, page_num, output_dir, scale=2.0):
    """渲染 PDF 页面为图像"""
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
        img.save(image_path, "PNG", optimize=True)
        
        return image_path
    except Exception as e:
        print(f"Error rendering page {page_num}: {e}", file=sys.stderr)
        return None


def extract_figures(pdf_path, purpose="deep_dive", output_dir=None, max_override=None):
    """
    智能提取 PDF 图表
    
    Args:
        pdf_path: PDF 文件路径
        purpose: 阅读目的 (quick_scan/deep_dive/method_focus/review_prep/brainstorm)
        output_dir: 图片输出目录，默认为 PDF 同目录下的 _figures 文件夹
        max_override: 覆盖默认的最大图表数
    
    Returns:
        list: [{page, type, path, caption, importance}]
    """
    try:
        pdf = pdfium.PdfDocument(pdf_path)
        total_pages = len(pdf)
        
        # 设置输出目录
        if output_dir is None:
            pdf_dir = os.path.dirname(os.path.abspath(pdf_path))
            pdf_name = Path(pdf_path).stem
            output_dir = os.path.join(pdf_dir, f"{pdf_name}_figures")
        
        strategy = PURPOSE_STRATEGIES.get(purpose, PURPOSE_STRATEGIES["deep_dive"])
        max_figures = max_override or strategy["max_figures"]
        
        # 收集所有图表信息
        all_figures = []
        page_texts = {}
        
        for i in range(total_pages):
            page = pdf[i]
            textpage = page.get_textpage()
            page_text = textpage.get_text_range()
            page_texts[i + 1] = page_text
            
            figures_in_page = detect_figures_in_page(page_text, i + 1)
            for fig in figures_in_page:
                fig["importance"] = calculate_figure_importance(fig, page_text, purpose)
                all_figures.append(fig)
        
        # 去重 (同一个图表可能在多页被引用)
        seen = set()
        unique_figures = []
        for fig in all_figures:
            key = (fig["type"], fig["number"])
            if key not in seen:
                seen.add(key)
                unique_figures.append(fig)
        
        # 按重要性排序并选取 top N
        unique_figures.sort(key=lambda x: x["importance"], reverse=True)
        selected_figures = unique_figures[:max_figures]
        
        # 渲染选中的图表页面
        result = []
        for fig in selected_figures:
            image_path = render_page_image(pdf_path, fig["page"], output_dir)
            if image_path:
                result.append({
                    "page": fig["page"],
                    "type": fig["type"],
                    "number": fig["number"],
                    "path": image_path,
                    "caption": f"{fig['type'].capitalize()} {fig['number']}",
                    "importance": fig["importance"]
                })
        
        return result
        
    except Exception as e:
        print(f"Error extracting figures: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return []


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_figures.py <pdf_path> [purpose] [output_dir] [max_figures]")
        print("  purpose: quick_scan|deep_dive|method_focus|review_prep|brainstorm")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    purpose = sys.argv[2] if len(sys.argv) > 2 else "deep_dive"
    output_dir = sys.argv[3] if len(sys.argv) > 3 else None
    max_figs = int(sys.argv[4]) if len(sys.argv) > 4 else None
    
    figures = extract_figures(pdf_path, purpose, output_dir, max_figs)
    print(json.dumps(figures, ensure_ascii=False, indent=2))
