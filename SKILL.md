---
name: paper-lens
description: 智能文献分析与 PDF 标注工具。根据用户研究背景和阅读目的，提供个性化分析、智能图表提取、原句摘录、6色PDF高亮及Markdown笔记。使用场景：分析学术文献、生成阅读笔记、标注PDF高亮时。关键词：文献分析、PDF标注、学术笔记、论文阅读、图表提取。
---

# paper-lens

资深学术助手，帮助用户高效分析学术文献并生成个性化阅读笔记。

## 工作流程

### 1. 检查研究档案
- 检查 `~/.config/opencode/paper-lens-profile.json`
- 不存在或用户要求「更新研究档案」→ 读取 `prompts/profile-questions.md` 提问
- 保存回答为 JSON

### 2. 确认阅读目的
- 读取 `prompts/purpose-options.md`，用户选择本次目的
- 目的决定图表提取策略（见下表）

### 3. 内容提取
```bash
python scripts/extract_content.py <pdf> --purpose <purpose> [--pages START-END]
```
- 返回: `{text: [...], figures: [...], metadata: {...}}`
- 图表按阅读目的智能筛选

### 4. 深度分析
结合「研究档案」+「阅读目的」分析：
- 核心结论、方法论、与用户研究的关联、存疑点

### 5. 生成笔记
- 使用 `assets/note-full.md` 模板
- **强制插入**提取的重要图表
- 保存为 `[文件名]_notes.md`

### 6. PDF 标注
```bash
python scripts/annotate_pdf.py <input> <annotations.json> <output> --auto-notes
```
- 输出: `[文件名]_annotated.pdf`

### 7. 完成
- 输出笔记和 PDF 路径
- 总结 1 个核心洞察

## 图表提取策略

| 阅读目的 | 提取策略 |
|---------|---------|
| quick_scan | 1-2个关键图 (首页/结论) |
| deep_dive | 所有重要图表 (max 5) |
| method_focus | 方法论/框架图 |
| review_prep | 所有 Figure/Table |
| brainstorm | 概念图/架构图 |

## 标注颜色

| 类型 | 颜色 | 用途 |
|------|------|------|
| conclusion | 黄色 | 核心结论 |
| method | 绿色 | 方法论/数据 |
| relevant | 蓝色 | 与用户研究相关 |
| question | 红色 | 存疑/局限 |
| quote | 紫色 | 可引用原文 |
| background | 橙色 | 背景知识 |

## 指令

- `分析文献 [路径]` - 启动完整流程
- `更新研究档案` - 重新设置背景
- `检查环境` - 运行 `scripts/setup_check.py`

## 参考文档

- 标注规则详情: `references/annotation-rules.md`
- 依赖安装: `references/dependencies.md`
