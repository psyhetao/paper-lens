# 依赖安装指南

## 必需依赖

```bash
pip install pymupdf pdfplumber pypdfium2 Pillow
```

### 各依赖用途

| 包名 | 用途 |
|------|------|
| pymupdf (fitz) | PDF 标注、高亮、添加注释 |
| pdfplumber | PDF 文本提取 (备用方案) |
| pypdfium2 | 快速 PDF 文本提取和页面渲染 |
| Pillow | 图像处理、图表导出 |

## 可选依赖

```bash
pip install camelot-py[cv]  # 表格提取 (需要 ghostscript)
```

## 环境检查

运行以下命令验证安装：

```bash
python scripts/setup_check.py
```

## 常见问题

### PyMuPDF 安装失败
Windows 用户可能需要先安装 Visual C++ Build Tools：
```bash
pip install pymupdf --upgrade
```

### pypdfium2 渲染问题
确保 Pillow 版本 >= 9.0：
```bash
pip install Pillow --upgrade
```

### 中文 PDF 乱码
pypdfium2 默认支持中文，如果出现乱码，尝试使用 pdfplumber：
```python
from extract_content import extract_text
# 内部会自动回退到 pdfplumber
```
