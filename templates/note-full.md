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

## 核心内容分析
### 1. 研究问题
> {{quote_question}} (p.{{page_question}})

{{#if image_question}}
![研究问题相关图表]({{image_question_path}})
*Figure (p.{{page_question}})*
{{/if}}

**解析**: {{analysis_question}}

### 2. 方法论
> {{quote_method}} (p.{{page_method}})

{{#if image_method}}
![方法论相关图表]({{image_method_path}})
*Figure (p.{{page_method}})*
{{/if}}

**解析**: {{analysis_method}}

### 3. 关键结论
> {{quote_conclusion}} (p.{{page_conclusion}})

{{#if image_conclusion}}
![结论相关图表]({{image_conclusion_path}})
*Figure (p.{{page_conclusion}})*
{{/if}}

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
