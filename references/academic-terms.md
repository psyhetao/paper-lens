# 学术术语库

常见学术术语及其简明解释，用于 PDF 术语注释和初学者模式笔记。

## 研究方法类

| 术语 | 英文 | 解释 | 常见场景 |
|------|------|------|----------|
| TAM | Technology Acceptance Model | 技术接受模型，解释用户如何接受和使用新技术 | 信息系统、人机交互研究 |
| PLS-SEM | Partial Least Squares Structural Equation Modeling | 偏最小二乘结构方程建模，适用于小样本的因果分析 | 管理学、心理学量化研究 |
| SEM | Structural Equation Modeling | 结构方程建模，验证变量间因果关系 | 社会科学统计分析 |
| R² | R-squared | 决定系数，表示模型解释变量变异的比例 (0-1) | 回归分析 |
| p-value | p值 | 统计显著性指标，<0.05 通常认为显著 | 假设检验 |
| β (Beta) | Beta coefficient | 回归系数，表示自变量对因变量的影响强度 | 回归分析 |
| Cronbach's α | 克朗巴赫系数 | 量表内部一致性信度指标 (>0.7 可接受) | 问卷研究 |
| AVE | Average Variance Extracted | 平均变异抽取量，衡量收敛效度 (>0.5 可接受) | SEM 分析 |
| CR | Composite Reliability | 组合信度，衡量构念信度 (>0.7 可接受) | SEM 分析 |
| VIF | Variance Inflation Factor | 方差膨胀因子，检测多重共线性 (<3 无问题) | 回归分析 |

## 理论框架类

| 术语 | 英文 | 解释 | 常见场景 |
|------|------|------|----------|
| UTAUT | Unified Theory of Acceptance and Use of Technology | 整合技术接受与使用理论，TAM 的扩展版 | 技术采纳研究 |
| TPB | Theory of Planned Behavior | 计划行为理论，态度-意图-行为模型 | 行为预测研究 |
| DOI | Diffusion of Innovation | 创新扩散理论，解释新技术如何传播 | 技术传播研究 |

## 统计概念类

| 术语 | 英文 | 解释 | 常见场景 |
|------|------|------|----------|
| 中介效应 | Mediation Effect | A 通过 B 影响 C 的间接效应 | 路径分析 |
| 调节效应 | Moderation Effect | B 改变 A 对 C 影响强度的效应 | 交互作用分析 |
| 显著性 | Significance | 统计结果不太可能由随机因素导致 | 假设检验 |
| 效应量 | Effect Size | 变量间关联的实际强度 (f²: 0.02小/0.15中/0.35大) | 结果解读 |

## 使用说明

在 `annotate_pdf.py` 中：
1. 扫描 PDF 文本，匹配术语库中的术语
2. 在术语首次出现的位置添加注释
3. 注释内容格式：`术语名: 解释 (场景)`
