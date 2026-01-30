#!/usr/bin/env python3
"""
统一内容提取模块
整合文本提取、图表提取，返回结构化内容
"""

import os
import sys
import json
import pypdfium2 as pdfium
from pathlib import Path

# 导入图表提取模块
from extract_figures import extract_figures, PURPOSE_STRATEGIES


def extract_text(pdf_path, start_page=None, end_page=None):
    """
    使用 pypdfium2 快速提取文本
    
    Returns:
        list: [{"page": 1, "text": "..."}]
    """
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
        print(f"Error extracting text: {e}", file=sys.stderr)
        return []


def extract_metadata(pdf_path):
    """提取 PDF 元数据"""
    try:
        pdf = pdfium.PdfDocument(pdf_path)
        metadata = {}
        
        # 尝试获取标准元数据字段
        meta_keys = ["Title", "Author", "Subject", "Keywords", "Creator", "Producer"]
        for key in meta_keys:
            try:
                value = pdf.get_metadata_value(key)
                if value:
                    metadata[key.lower()] = value
            except:
                pass
        
        metadata["total_pages"] = len(pdf)
        metadata["filename"] = Path(pdf_path).name
        
        return metadata
    except Exception as e:
        print(f"Error extracting metadata: {e}", file=sys.stderr)
        return {"filename": Path(pdf_path).name}


def get_pages_for_purpose(purpose, total_pages):
    """根据阅读目的确定需要提取的页面范围"""
    if purpose == "quick_scan":
        # 前3页 + 最后2页
        pages = list(range(1, min(4, total_pages + 1)))
        if total_pages > 3:
            pages.extend(range(max(total_pages - 1, 4), total_pages + 1))
        return sorted(set(pages))
    
    elif purpose == "method_focus":
        # 全文 (方法通常在中间)
        return list(range(1, total_pages + 1))
    
    elif purpose == "review_prep":
        # 全文
        return list(range(1, total_pages + 1))
    
    else:  # deep_dive, brainstorm, default
        # 全文
        return list(range(1, total_pages + 1))


def extract_content(pdf_path, purpose="deep_dive", pages=None, include_figures=True, output_dir=None):
    """
    统一内容提取入口
    
    Args:
        pdf_path: PDF 文件路径
        purpose: 阅读目的
        pages: 指定页码范围 (如 "1-5" 或 [1,2,3,4,5])
        include_figures: 是否提取图表
        output_dir: 图片输出目录
    
    Returns:
        dict: {
            "text": [...],
            "figures": [...],
            "metadata": {...}
        }
    """
    result = {
        "text": [],
        "figures": [],
        "metadata": {}
    }
    
    # 提取元数据
    result["metadata"] = extract_metadata(pdf_path)
    total_pages = result["metadata"].get("total_pages", 0)
    
    # 确定页码范围
    if pages is None:
        page_list = get_pages_for_purpose(purpose, total_pages)
    elif isinstance(pages, str):
        # 解析 "1-5" 格式
        if "-" in pages:
            start, end = pages.split("-")
            page_list = list(range(int(start), int(end) + 1))
        else:
            page_list = [int(pages)]
    else:
        page_list = pages
    
    # 提取文本
    if page_list:
        start_page = min(page_list)
        end_page = max(page_list)
        result["text"] = extract_text(pdf_path, start_page, end_page)
    
    # 提取图表
    if include_figures:
        result["figures"] = extract_figures(pdf_path, purpose, output_dir)
    
    return result


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Extract content from PDF")
    parser.add_argument("pdf_path", help="Path to PDF file")
    parser.add_argument("--purpose", "-p", default="deep_dive",
                        choices=["quick_scan", "deep_dive", "method_focus", "review_prep", "brainstorm"],
                        help="Reading purpose")
    parser.add_argument("--pages", help="Page range (e.g., 1-5)")
    parser.add_argument("--no-figures", action="store_true", help="Skip figure extraction")
    parser.add_argument("--output-dir", "-o", help="Output directory for figures")
    parser.add_argument("--output-file", "-f", help="Save result to JSON file")
    
    args = parser.parse_args()
    
    content = extract_content(
        args.pdf_path,
        purpose=args.purpose,
        pages=args.pages,
        include_figures=not args.no_figures,
        output_dir=args.output_dir
    )
    
    output_json = json.dumps(content, ensure_ascii=False, indent=2)
    
    if args.output_file:
        with open(args.output_file, 'w', encoding='utf-8') as f:
            f.write(output_json)
        print(f"Content extracted to {args.output_file}")
    else:
        print(output_json)
