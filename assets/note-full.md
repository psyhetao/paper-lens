---
title: "{{title}}"
authors: {{authors}}
year: {{year}}
journal: "{{journal}}"
doi: {{doi}}
tags: [paper-lens, {{tags}}]
read_date: {{read_date}}
purpose: {{purpose}}
---

# {{title}}

## APA Citation
> {{apa_citation}}

## 快速评估
- **相关度**: {{relevance_score}}/5
- **核心贡献**: {{contribution_summary}}
- **是否深读**: {{should_read_deeply}}

---

## 核心图表

{{#if figures}}
{{#each figures}}
### {{this.caption}}
![{{this.caption}}]({{this.path}})
*{{this.caption}} (p.{{this.page}}) - 重要性评分: {{this.importance}}*

{{/each}}
{{else}}
*本文献未检测到与阅读目的高度相关的图表*
{{/if}}

---

## 核心内容分析

### 1. 研究问题
> {{quote_question}} (p.{{page_question}})

**解析**: {{analysis_question}}

### 2. 方法论
> {{quote_method}} (p.{{page_method}})

**解析**: {{analysis_method}}

### 3. 关键结论
> {{quote_conclusion}} (p.{{page_conclusion}})

**解析**: {{analysis_conclusion}}

---

## 与我的研究关联 ({{user_field}})
- **启发点**: {{inspiration}}
- **可应用之处**: {{application}}
- **批判性思考**: {{critique}}

---

## 重要原句摘录
| 页码 | 原句 | 类别 | 备注 |
|-----|------|------|------|
{{quote_table_rows}}

---

## 后续行动
- [ ] {{todo_1}}
- [ ] {{todo_2}}
