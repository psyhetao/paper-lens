---
name: paper-lens
description: 智能文献分析与 PDF 标注工具。根据用户研究背景和本次阅读目的，生成个性化阅读笔记（含关键术语解释、强制图表插入/失败提示）并输出带高亮/术语注释的标注 PDF。适用：论文阅读、做笔记、学习学术概念、复现方法、写综述。
---

# paper-lens

## 工作流程 (STRICT)

### 1) 检查研究档案
- 检查 `~/.config/opencode/paper-lens-profile.json`
- 不存在或用户要求「更新研究档案」: 读取 `prompts/profile-questions.md` 提问并保存为 JSON

### 2) 确认本次阅读目的 (必问)
- 读取 `prompts/purpose-options.md` 让用户选择
- 支持新增目的: `beginner`（初学者入门，重点解释学术概念）
- 同时询问是否开启“术语注释”（默认开启；可用 `--no-terms` 关闭）

### 3) 在目标 PDF 同目录创建输出文件夹
输出目录固定为：`<PDF同目录>/<PDF文件名(无扩展名)>/`

需要最终保留的文件：
- `<原名>_notes.md`
- `<原名>_annotated.pdf`
- `figures/`

### 4) 提取内容与图表
```bash
python scripts/extract_content.py <pdf> --purpose <purpose>
```
- 自动创建输出目录与 `figures/`
- 图表提取规则：只导出图/表本体；若无法单独提取（矢量/无嵌入图像），返回 `extractable=false` 与提示信息

### 5) 深度分析并生成笔记
- 使用 `assets/note-full.md` 模板生成笔记
- **强制插入重要图表**（不可提取则插入提示文本，不插整页截图）
- `beginner` 模式必须生成“核心概念解释 (初学者必读)”并从初学者角度解释文中专有名词
- 保存到输出目录：`<原名>_notes.md`

### 6) 生成标注 PDF
准备标注 JSON（只做高亮用，生成后可删除）：
`[{"text":"...","page":1,"type":"conclusion|method|relevant|question|quote|background"}]`

执行标注：
```bash
python scripts/annotate_pdf.py <input.pdf> <annotations.json> <output.pdf> [--no-terms] [--keep-json]
```
- 默认开启术语注释（term notes），内容为学术术语的解释
- 默认删除 `annotations.json`；需要保留时使用 `--keep-json`
- 输出到输出目录：`<原名>_annotated.pdf`

### 7) 完成
- 告知用户输出目录路径
- 总结 1 个最关键洞察

## 阅读目的

| purpose | 侧重点 |
|---|---|
| quick_scan | 快速判断是否值得读 |
| deep_dive | 详尽记录与复用 |
| method_focus | 钻研方法/实验/框架 |
| review_prep | 综述写作与对比 |
| brainstorm | 交叉与创新启发 |
| beginner | 初学者入门：解释学术概念 |

## 标注颜色

| type | 颜色 | 含义 |
|---|---|---|
| conclusion | 黄色 | 核心结论 |
| method | 绿色 | 方法/数据 |
| relevant | 蓝色 | 与用户研究相关 |
| question | 红色 | 局限/存疑 |
| quote | 紫色 | 值得引用的原文 |
| background | 橙色 | 背景/铺垫 |
| term | 浅蓝 | 学术术语注释 |

## 指令

- `分析文献 [路径]`
- `更新研究档案`
- `检查环境`（运行 `scripts/setup_check.py`）

## 参考

- 标注规则: `references/annotation-rules.md`
- 术语库: `references/academic-terms.md`
- 依赖: `references/dependencies.md`
