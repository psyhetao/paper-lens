#!/usr/bin/env python3
"""
统一内容提取模块 v2
- 统一输出到 PDF 同目录同名文件夹
- 支持 beginner 模式
- 清理临时文件
"""

import os
import sys
import json
import shutil
import fitz  # PyMuPDF for metadata
from pathlib import Path

# 导入图表提取模块
from extract_figures import extract_figures, PURPOSE_STRATEGIES


def resolve_output_dir(pdf_path):
    """
    解析输出目录：PDF 同目录下建立同名文件夹
    返回: output_dir 路径
    """
    pdf_path = os.path.abspath(pdf_path)
    pdf_dir = os.path.dirname(pdf_path)
    pdf_name = Path(pdf_path).stem
    
    output_dir = os.path.join(pdf_dir, pdf_name)
    os.makedirs(output_dir, exist_ok=True)
    
    # 创建 figures 子目录
    figures_dir = os.path.join(output_dir, "figures")
    os.makedirs(figures_dir, exist_ok=True)
    
    return output_dir


def extract_text_fitz(pdf_path, start_page=None, end_page=None):
    """
    使用 PyMuPDF 提取文本
    """
    try:
        doc = fitz.open(pdf_path)
        total_pages = len(doc)
        
        start = start_page - 1 if start_page is not None else 0
        end = end_page if end_page is not None else total_pages
        
        content = []
        for i in range(start, end):
            page = doc[i]
            text = page.get_text()
            content.append({
                "page": i + 1,
                "text": text
            })
        
        doc.close()
        return content
    except Exception as e:
        print(f"Error extracting text: {e}", file=sys.stderr)
        return []


def extract_metadata(pdf_path):
    """提取 PDF 元数据"""
    try:
        doc = fitz.open(pdf_path)
        metadata = doc.metadata or {}
        
        result = {}
        for key in ["title", "author", "subject", "keywords", "creator", "producer"]:
            if key in metadata and metadata[key]:
                result[key] = metadata[key]
        
        result["total_pages"] = len(doc)
        result["filename"] = Path(pdf_path).name
        
        doc.close()
        return result
    except Exception as e:
        print(f"Error extracting metadata: {e}", file=sys.stderr)
        return {"filename": Path(pdf_path).name}


def get_pages_for_purpose(purpose, total_pages):
    """根据阅读目的确定需要提取的页面范围"""
    if purpose == "quick_scan":
        pages = list(range(1, min(4, total_pages + 1)))
        if total_pages > 3:
            pages.extend(range(max(total_pages - 1, 4), total_pages + 1))
        return sorted(set(pages))
    else:
        # deep_dive, method_focus, review_prep, brainstorm, beginner: 全文
        return list(range(1, total_pages + 1))


def cleanup_temp_files(output_dir, *files):
    """清理临时文件"""
    for f in files:
        try:
            path = os.path.join(output_dir, f) if not os.path.isabs(f) else f
            if os.path.exists(path):
                os.remove(path)
        except:
            pass


def extract_content(pdf_path, purpose="deep_dive", pages=None, include_figures=True, output_dir=None):
    """
    统一内容提取入口
    
    Args:
        pdf_path: PDF 文件路径
        purpose: 阅读目的 (quick_scan/deep_dive/method_focus/review_prep/brainstorm/beginner)
        pages: 指定页码范围
        include_figures: 是否提取图表
        output_dir: 输出目录 (默认 PDF 同目录同名文件夹)
    
    Returns:
        dict: {text, figures, metadata, output_dir}
    """
    # 解析输出目录
    if output_dir is None:
        output_dir = resolve_output_dir(pdf_path)
    
    figures_dir = os.path.join(output_dir, "figures")
    
    result = {
        "text": [],
        "figures": [],
        "metadata": {},
        "output_dir": output_dir
    }
    
    # 提取元数据
    result["metadata"] = extract_metadata(pdf_path)
    total_pages = result["metadata"].get("total_pages", 0)
    
    # 确定页码范围
    if pages is None:
        page_list = get_pages_for_purpose(purpose, total_pages)
    elif isinstance(pages, str):
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
        result["text"] = extract_text_fitz(pdf_path, start_page, end_page)
    
    # 提取图表
    if include_figures:
        result["figures"] = extract_figures(pdf_path, purpose, figures_dir)
    
    return result


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Extract content from PDF")
    parser.add_argument("pdf_path", help="Path to PDF file")
    parser.add_argument("--purpose", "-p", default="deep_dive",
                        choices=["quick_scan", "deep_dive", "method_focus", "review_prep", "brainstorm", "beginner"],
                        help="Reading purpose")
    parser.add_argument("--pages", help="Page range (e.g., 1-5)")
    parser.add_argument("--no-figures", action="store_true", help="Skip figure extraction")
    parser.add_argument("--output-dir", "-o", help="Output directory")
    parser.add_argument("--output-file", "-f", help="Save result to JSON file (debug only)")
    
    args = parser.parse_args()
    
    content = extract_content(
        args.pdf_path,
        purpose=args.purpose,
        pages=args.pages,
        include_figures=not args.no_figures,
        output_dir=args.output_dir
    )
    
    # Print-safe JSON (avoid Windows console encoding issues)
    output_json = json.dumps(content, ensure_ascii=True, indent=2)
    
    if args.output_file:
        with open(args.output_file, 'w', encoding='utf-8') as f:
            f.write(output_json)
        print(f"Content extracted to {args.output_file}")
        print(f"Output directory: {content['output_dir']}")
    else:
        print(output_json)
