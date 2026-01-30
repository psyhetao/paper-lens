# 标注规则详解

## 颜色规范

paper-lens 使用 6 色标注系统，每种颜色对应特定的内容类型：

| 类型 | 颜色 | RGB 值 | 使用场景 |
|------|------|--------|---------|
| conclusion | 黄色 | (1, 1, 0) | 核心结论、主要发现 |
| method | 绿色 | (0.6, 1, 0.6) | 方法论、实验设计、数据处理 |
| relevant | 蓝色 | (0.6, 0.8, 1) | 与用户研究方向相关的内容 |
| question | 红色 | (1, 0.6, 0.6) | 存疑点、局限性、需验证内容 |
| quote | 紫色 | (0.9, 0.7, 1) | 值得直接引用的原文 |
| background | 橙色 | (1, 0.8, 0.5) | 背景知识、文献综述 |

## 自动注释规则

系统基于关键词自动在 PDF 中添加文本注释：

### 研究问题关键词
- research question, objective, aim, purpose
- 研究问题, 研究目的, 研究目标

### 方法论关键词
- method, methodology, approach, framework
- 方法, 方法论, 框架

### 结论关键词
- conclusion, finding, result, key result
- 结论, 发现, 结果

## 标注 JSON 格式

```json
[
  {
    "text": "要高亮的文本",
    "page": 1,
    "type": "conclusion"
  },
  {
    "text": "注释内容",
    "page": 2,
    "type": "text_note",
    "x": 100,
    "y": 150
  }
]
```

## 标注优先级

1. **conclusion** - 最重要，通常出现在 Abstract 和 Conclusion 部分
2. **method** - 重要，集中在 Methods/Methodology 部分
3. **relevant** - 需要结合用户研究档案判断
4. **quote** - 语言优美或概念精准的原文
5. **question** - 存疑内容，需要进一步验证
6. **background** - 信息性内容，非核心但有价值
