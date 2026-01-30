#!/usr/bin/env python3
"""
智能图表提取模块 v2
- 使用 PyMuPDF 提取嵌入图像并裁剪
- 解析图注文本作为 caption
- 无法提取时返回提示而非整页截图
"""

import os
import sys
import json
import re
import fitz  # PyMuPDF
from pathlib import Path

# 阅读目的对应的图表提取策略
PURPOSE_STRATEGIES = {
    "quick_scan": {"max_figures": 2, "priority": ["conclusion", "abstract"]},
    "deep_dive": {"max_figures": 5, "priority": ["all"]},
    "method_focus": {"max_figures": 4, "priority": ["method", "framework", "algorithm"]},
    "review_prep": {"max_figures": 10, "priority": ["all"]},
    "brainstorm": {"max_figures": 3, "priority": ["concept", "framework", "overview"]},
    "beginner": {"max_figures": 3, "priority": ["all"]},  # 新增初学者模式
}

# 图表标题识别模式
FIGURE_PATTERNS = [
    r"(Figure|Fig\.?)\s*(\d+)[.:]?\s*(.{0,200}?)(?:\n|$)",
    r"(Table)\s*(\d+)[.:]?\s*(.{0,200}?)(?:\n|$)",
    r"(图)\s*(\d+)[.:]?\s*(.{0,100}?)(?:\n|$)",
    r"(表)\s*(\d+)[.:]?\s*(.{0,100}?)(?:\n|$)",
]

# 区域关键词
REGION_KEYWORDS = {
    "abstract": ["abstract", "摘要", "summary"],
    "conclusion": ["conclusion", "结论", "findings", "results", "发现"],
    "method": ["method", "methodology", "approach", "方法", "框架", "framework"],
    "introduction": ["introduction", "引言", "背景", "background"],
}


def detect_page_region(page_text):
    """检测页面所属区域"""
    text_lower = page_text.lower()
    for region, keywords in REGION_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text_lower:
                return region
    return "body"


def extract_figure_caption(page_text, fig_type, fig_num):
    """
    从页面文本中提取图表的完整 caption
    返回: caption 字符串，如 "Figure 1: The proposed TAM model..."
    """
    for pattern in FIGURE_PATTERNS:
        matches = re.finditer(pattern, page_text, re.IGNORECASE | re.DOTALL)
        for match in matches:
            match_type = match.group(1).lower()
            match_num = match.group(2)
            
            # 匹配类型和编号
            type_match = (
                (fig_type == "figure" and match_type in ["figure", "fig", "fig.", "图"]) or
                (fig_type == "table" and match_type in ["table", "表"])
            )
            
            if type_match and match_num == str(fig_num):
                caption_text = match.group(3).strip() if len(match.groups()) > 2 else ""
                full_caption = f"{match.group(1)} {match_num}"
                if caption_text:
                    full_caption += f": {caption_text}"
                return full_caption
    
    # 默认 caption
    return f"{fig_type.capitalize()} {fig_num}"


def detect_figures_in_page(page_text, page_num):
    """检测页面中的图表引用"""
    figures = []
    seen = set()
    
    for pattern in FIGURE_PATTERNS:
        matches = re.finditer(pattern, page_text, re.IGNORECASE | re.DOTALL)
        for match in matches:
            match_type = match.group(1).lower()
            fig_num = match.group(2)
            
            # 确定类型
            if match_type in ["figure", "fig", "fig.", "图"]:
                fig_type = "figure"
            else:
                fig_type = "table"
            
            key = (fig_type, fig_num)
            if key not in seen:
                seen.add(key)
                caption = extract_figure_caption(page_text, fig_type, fig_num)
                figures.append({
                    "page": page_num,
                    "number": fig_num,
                    "type": fig_type,
                    "caption": caption,
                    "position": match.start()
                })
    
    return figures


def calculate_figure_importance(figure_info, page_text, purpose):
    """计算图表重要性评分"""
    score = 0
    strategy = PURPOSE_STRATEGIES.get(purpose, PURPOSE_STRATEGIES["deep_dive"])
    priority_regions = strategy["priority"]
    
    page_region = detect_page_region(page_text)
    if "all" in priority_regions or page_region in priority_regions:
        score += 10
    
    if figure_info["page"] <= 2:
        score += 5
    
    fig_ref_pattern = rf"(?:Figure|Fig\.?|图)\s*{figure_info['number']}"
    ref_count = len(re.findall(fig_ref_pattern, page_text, re.IGNORECASE))
    score += ref_count * 2
    
    if purpose == "method_focus" and figure_info["type"] == "table":
        score += 3
    
    return score


def extract_embedded_images(pdf_path, page_num, output_dir, fig_info):
    """
    使用 PyMuPDF 提取页面中的嵌入图像
    返回: (image_path, success) 或 (None, False)
    """
    try:
        doc = fitz.open(pdf_path)
        page = doc[page_num - 1]
        
        # 获取页面中的所有图像
        image_list = page.get_images(full=True)
        
        if not image_list:
            return None, False
        
        os.makedirs(output_dir, exist_ok=True)
        
        # 选择最大的图像（通常是主要图表）
        best_image = None
        best_size = 0
        
        for img_index, img_info in enumerate(image_list):
            xref = img_info[0]
            try:
                base_image = doc.extract_image(xref)
                if base_image:
                    image_bytes = base_image["image"]
                    size = len(image_bytes)
                    if size > best_size:
                        best_size = size
                        best_image = base_image
            except:
                continue
        
        if best_image and best_size > 1000:  # 至少 1KB
            ext = best_image.get("ext", "png")
            filename = f"{fig_info['type']}_{fig_info['number']}.{ext}"
            image_path = os.path.join(output_dir, filename)
            
            with open(image_path, "wb") as f:
                f.write(best_image["image"])
            
            doc.close()
            return image_path, True
        
        doc.close()
        return None, False
        
    except Exception as e:
        print(f"Error extracting image from page {page_num}: {e}", file=sys.stderr)
        return None, False


def extract_figures(pdf_path, purpose="deep_dive", output_dir=None, max_override=None):
    """
    智能提取 PDF 图表
    
    Args:
        pdf_path: PDF 文件路径
        purpose: 阅读目的
        output_dir: 图片输出目录
        max_override: 覆盖默认的最大图表数
    
    Returns:
        list: [{page, type, number, path, caption, importance, extractable}]
    """
    try:
        doc = fitz.open(pdf_path)
        total_pages = len(doc)
        
        # 设置输出目录
        if output_dir is None:
            pdf_dir = os.path.dirname(os.path.abspath(pdf_path))
            pdf_name = Path(pdf_path).stem
            output_dir = os.path.join(pdf_dir, pdf_name, "figures")
        
        strategy = PURPOSE_STRATEGIES.get(purpose, PURPOSE_STRATEGIES["deep_dive"])
        max_figures = max_override or strategy["max_figures"]
        
        # 收集所有图表信息
        all_figures = []
        page_texts = {}
        
        for i in range(total_pages):
            page = doc[i]
            page_text = page.get_text()
            page_texts[i + 1] = page_text
            
            figures_in_page = detect_figures_in_page(page_text, i + 1)
            for fig in figures_in_page:
                fig["importance"] = calculate_figure_importance(fig, page_text, purpose)
                all_figures.append(fig)
        
        doc.close()
        
        # 去重
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
        
        # 提取图像
        result = []
        unextractable_count = 0
        
        for fig in selected_figures:
            image_path, success = extract_embedded_images(pdf_path, fig["page"], output_dir, fig)
            
            if success and image_path:
                result.append({
                    "page": fig["page"],
                    "type": fig["type"],
                    "number": fig["number"],
                    "path": image_path,
                    "caption": fig["caption"],
                    "importance": fig["importance"],
                    "extractable": True
                })
            else:
                unextractable_count += 1
                result.append({
                    "page": fig["page"],
                    "type": fig["type"],
                    "number": fig["number"],
                    "path": None,
                    "caption": fig["caption"],
                    "importance": fig["importance"],
                    "extractable": False,
                    "message": f"该{fig['type']}为矢量格式或无法单独提取，请参阅原PDF第{fig['page']}页"
                })
        
        if unextractable_count > 0:
            print(f"[paper-lens] {unextractable_count} 个图表无法单独提取，已跳过", file=sys.stderr)
        
        return result
        
    except Exception as e:
        print(f"Error extracting figures: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return []


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_figures.py <pdf_path> [purpose] [output_dir] [max_figures]")
        print("  purpose: quick_scan|deep_dive|method_focus|review_prep|brainstorm|beginner")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    purpose = sys.argv[2] if len(sys.argv) > 2 else "deep_dive"
    output_dir = sys.argv[3] if len(sys.argv) > 3 else None
    max_figs = int(sys.argv[4]) if len(sys.argv) > 4 else None
    
    figures = extract_figures(pdf_path, purpose, output_dir, max_figs)
    print(json.dumps(figures, ensure_ascii=False, indent=2))
