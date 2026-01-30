# 依赖安装指南

## 必需依赖

```bash
pip install pymupdf
```

### 各依赖用途

| 包名 | 用途 |
|------|------|
| pymupdf (fitz) | PDF 标注、高亮、添加注释 |
| (可选) camelot-py | 表格提取（需要额外依赖） |

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

### 中文 PDF 乱码/搜索不到文本
部分 PDF 为扫描件或字体编码特殊，文本层不可用。此时：
- 术语注释/高亮可能无法定位
- 图表也可能无法单独导出（矢量或无嵌入图像）

paper-lens 会提示“无法提取/无法定位”，不会强行插入整页截图。
