#!/usr/bin/env python3
"""
PDF 标注模块 v2
- 支持术语注释开关（默认开启）
- 术语注释内容为学术术语解释
- 注释位置定位到术语附近
"""

import fitz
import json
import sys
import os
import re

# 高亮颜色配置
COLORS = {
    "conclusion": (1, 1, 0),       # Yellow - 核心结论
    "method": (0.6, 1, 0.6),       # Green - 方法论
    "relevant": (0.6, 0.8, 1),     # Blue - 相关内容
    "question": (1, 0.6, 0.6),     # Red - 存疑点
    "quote": (0.9, 0.7, 1),        # Purple - 可引用
    "background": (1, 0.8, 0.5),   # Orange - 背景
    "term": (0.7, 0.9, 1),         # Light Blue - 术语
}

# 内置术语库（简明版）
ACADEMIC_TERMS = {
    "TAM": "Technology Acceptance Model，技术接受模型，解释用户如何接受新技术",
    "PLS-SEM": "偏最小二乘结构方程建模，适用于小样本的因果关系分析",
    "SEM": "Structural Equation Modeling，结构方程建模，验证变量间因果关系",
    "R²": "决定系数，表示模型解释变量变异的比例，范围0-1",
    "R-squared": "决定系数，表示模型解释变量变异的比例，范围0-1",
    "p-value": "统计显著性指标，<0.05通常认为结果显著",
    "p<0.05": "统计显著，表示结果不太可能由随机因素导致",
    "p<0.01": "高度统计显著，结果更可靠",
    "Cronbach's α": "克朗巴赫系数，衡量量表内部一致性信度",
    "AVE": "平均变异抽取量，衡量收敛效度，>0.5可接受",
    "VIF": "方差膨胀因子，检测多重共线性，<3无问题",
    "UTAUT": "整合技术接受与使用理论，TAM的扩展版",
    "TPB": "Theory of Planned Behavior，计划行为理论",
    "mediation": "中介效应，A通过B间接影响C",
    "moderation": "调节效应，B改变A对C的影响强度",
    "perceived usefulness": "感知有用性，用户认为技术能提升工作效率的程度",
    "perceived ease of use": "感知易用性，用户认为技术容易使用的程度",
    "social influence": "社会影响，他人意见对用户采纳决策的影响",
    "facilitating conditions": "促进条件，支持技术使用的组织和技术环境",
    "behavioral intention": "行为意图，用户计划使用某技术的倾向",
}


def highlight_text(page, text_to_highlight, ann_type):
    """在 PDF 页面中高亮指定文本"""
    color = COLORS.get(ann_type, COLORS["background"])
    text_instances = page.search_for(text_to_highlight)
    
    for inst in text_instances:
        highlight = page.add_highlight_annot(inst)
        highlight.set_colors(stroke=color)
        highlight.update()
    
    return len(text_instances)


def add_term_annotation(page, term, definition, rect):
    """
    在术语位置添加注释
    rect: 术语的边界框
    """
    # 在术语右侧或下方添加注释
    point = fitz.Point(rect.x1 + 5, rect.y0)
    
    note_text = f"{term}: {definition}"
    annot = page.add_text_annot(point, note_text)
    annot.set_colors(stroke=COLORS["term"])
    annot.update()
    
    return annot


def generate_term_annotations(doc, enable_terms=True):
    """
    扫描 PDF 并生成术语注释
    每个术语只在首次出现时添加注释
    """
    if not enable_terms:
        return 0
    
    annotated_terms = set()
    annotation_count = 0
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        page_text = page.get_text()
        
        for term, definition in ACADEMIC_TERMS.items():
            if term in annotated_terms:
                continue
            
            # 搜索术语（大小写不敏感）
            rects = page.search_for(term, quads=False)
            
            if rects:
                # 只在首次出现时添加注释
                rect = rects[0]
                add_term_annotation(page, term, definition, rect)
                annotated_terms.add(term)
                annotation_count += 1
    
    return annotation_count


def annotate_pdf(input_path, annotations_json, output_path, enable_terms=True, cleanup_json=True):
    """
    标注 PDF
    
    Args:
        input_path: 输入 PDF 路径
        annotations_json: 标注 JSON 文件路径或 JSON 字符串
        output_path: 输出 PDF 路径
        enable_terms: 是否启用术语注释（默认开启）
    """
    try:
        doc = fitz.open(input_path)
        
        # 加载标注
        if os.path.exists(annotations_json):
            with open(annotations_json, 'r', encoding='utf-8') as f:
                annotations = json.load(f)
        else:
            try:
                annotations = json.loads(annotations_json)
            except:
                annotations = []
        
        # 处理高亮标注
        highlight_count = 0
        for ann in annotations:
            page_num = ann.get("page", 1) - 1
            if page_num < 0 or page_num >= len(doc):
                continue
            
            page = doc[page_num]
            ann_type = ann.get("type", "background")
            text_to_highlight = ann.get("text", "")
            
            if text_to_highlight and ann_type != "text_note":
                count = highlight_text(page, text_to_highlight, ann_type)
                highlight_count += count
        
        # 生成术语注释
        term_count = 0
        if enable_terms:
            term_count = generate_term_annotations(doc, enable_terms)
        
        # 保存 PDF
        doc.save(output_path)
        doc.close()

        # 默认清理临时 JSON
        if cleanup_json and os.path.exists(annotations_json):
            try:
                os.remove(annotations_json)
            except:
                pass
        
        print(f"[paper-lens] 高亮标注: {highlight_count} 处", file=sys.stderr)
        if enable_terms:
            print(f"[paper-lens] 术语注释: {term_count} 个", file=sys.stderr)
        
        return True
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python annotate_pdf.py <input.pdf> <annotations.json> <output.pdf> [--no-terms] [--keep-json]")
        print("  --no-terms: 关闭术语注释")
        print("  --keep-json: 保留 annotations.json")
        sys.exit(1)
    
    input_pdf = sys.argv[1]
    ann_json = sys.argv[2]
    output_pdf = sys.argv[3]
    enable_terms = '--no-terms' not in sys.argv
    cleanup_json = '--keep-json' not in sys.argv
    
    if annotate_pdf(input_pdf, ann_json, output_pdf, enable_terms=enable_terms, cleanup_json=cleanup_json):
        print(f"Success: {output_pdf}")
    else:
        sys.exit(1)
