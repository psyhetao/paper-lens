# paper-lens

智能文献分析与 PDF 标注工具。根据用户研究背景和阅读目的，提供个性化分析、智能图表提取、原句摘录、6色PDF高亮及Markdown笔记。

## 功能特性

- **个性化分析**: 基于用户研究档案定制分析视角
- **智能图表提取**: 根据阅读目的自动筛选重要图表
- **6色PDF标注**: 结论/方法/相关/存疑/引用/背景 分类高亮
- **Markdown笔记**: 自动生成结构化阅读笔记
- **APA引用**: 自动生成标准格式引用

## 安装

```bash
pip install pymupdf
```

验证安装：

```bash
python scripts/setup_check.py
```

## 快速开始

### 1. 提取内容

```bash
# 快速扫描模式 (提取1-2个关键图表)
python scripts/extract_content.py paper.pdf --purpose quick_scan

# 深度阅读模式 (提取所有重要图表)
python scripts/extract_content.py paper.pdf --purpose deep_dive

# 方法学习模式 (聚焦方法论图表)
python scripts/extract_content.py paper.pdf --purpose method_focus

# 初学者入门模式 (解释学术概念)
python scripts/extract_content.py paper.pdf --purpose beginner
```

输出目录：会在 `paper.pdf` 同目录下创建同名文件夹 `paper/`，并将 `figures/` 写入其中。

### 2. 标注 PDF

```bash
python scripts/annotate_pdf.py input.pdf annotations.json output.pdf

# 关闭术语注释
python scripts/annotate_pdf.py input.pdf annotations.json output.pdf --no-terms
```

标注 JSON 格式：

```json
[
  {"text": "核心结论文本", "page": 1, "type": "conclusion"},
  {"text": "方法描述", "page": 3, "type": "method"}
]
```

## 阅读目的与图表策略

| 目的 | 说明 | 图表数量 |
|------|------|---------|
| `quick_scan` | 快速评估价值 | 1-2个 |
| `deep_dive` | 详尽记录 | 最多5个 |
| `method_focus` | 钻研方法细节 | 最多4个 |
| `review_prep` | 综述准备 | 最多10个 |
| `brainstorm` | 寻找创新点 | 最多3个 |
| `beginner` | 初学者入门 | 最多3个 |

## 标注颜色规范

| 类型 | 颜色 | 用途 |
|------|------|------|
| `conclusion` | 黄色 | 核心结论 |
| `method` | 绿色 | 方法论/数据 |
| `relevant` | 蓝色 | 与研究相关 |
| `question` | 红色 | 存疑/局限 |
| `quote` | 紫色 | 可引用原文 |
| `background` | 橙色 | 背景知识 |
| `term` | 浅蓝 | 学术术语注释 |

## 目录结构

```
paper-lens/
├── SKILL.md              # 技能定义文件
├── scripts/
│   ├── extract_content.py    # 统一内容提取
│   ├── extract_figures.py    # 智能图表提取
│   ├── annotate_pdf.py       # PDF 标注
│   └── setup_check.py        # 环境检查
├── references/
│   ├── annotation-rules.md   # 标注规则详解
│   └── dependencies.md       # 依赖说明
├── assets/
│   └── note-full.md          # 笔记模板
└── prompts/
    ├── profile-questions.md  # 研究档案问题
    └── purpose-options.md    # 阅读目的选项
```

## 作为 OpenCode Skill 使用

将此仓库克隆到 `~/.config/opencode/skills/` 目录：

```bash
cd ~/.config/opencode/skills/
git clone https://github.com/psyhetao/paper-lens.git
```

然后在 OpenCode 中使用指令：

- `分析文献 [路径]` - 启动完整分析流程
- `更新研究档案` - 重新设置研究背景
- `检查环境` - 验证依赖安装

## 依赖

| 包名 | 用途 |
|------|------|
| pymupdf | PDF 标注和高亮 |
| pdfplumber | 文本提取 (备用) |
| pypdfium2 | 快速文本提取和渲染 |
| Pillow | 图像处理 |

## License

MIT
