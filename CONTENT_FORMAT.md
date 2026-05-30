---
# AI Prompt Hub 内容格式规范 v2.0
# 支持中英双语 + 来源标注 + 原文/译文切换
---

## 提示词 (content/prompts/*.md)

```yaml
---
# === 基础信息 ===
title: "中文标题"
title_en: "English Title"
category: writing|coding|drawing|data|chat|other
description: "中文简短描述"
description_en: "English description"

# === 来源信息（新增）===
source: "AiShort"              # 来源平台：AiShort, Awesome-ChatGPT-Prompts, FlowGPT, SnackPrompt, 小红书, 知乎, Reddit, Twitter, 其他
source_url: "https://..."      # 原始链接（可选，有就填）
author: "原作者名"              # 原作者（可选）
author_en: "Original Author"

# === 语言信息（新增）===
language: zh|en|zh-en          # 原文语言：zh=中文, en=英文, zh-en=中英双语
translated_by: "AI|人工|原文"   # 翻译方式：AI=AI翻译, 人工=人工翻译, 原文=无需翻译

# === 热度与标签 ===
hot_score: 50                  # 热度 0-100
created_at: "2024-05-09"
tags: [标签1, 标签2]
tags_en: [tag1, tag2]
models: [gpt-4, claude, kimi]  # 适用模型

# === 验证信息（新增）===
verified: true                 # 是否经过验证
verified_type: "高赞|高收藏|效果反馈|博主推荐"  # 验证类型
---

# 提示词内容

## 中文版（如果是翻译的，标注"【译文】"）
[提示词正文...]

## English Version (mark as "[Translation]" if translated)
[Prompt content...]
```

## 人格设定 (content/agents/*.md)

```yaml
---
# === 基础信息 ===
title: "中文标题"
title_en: "English Title"
category: professional|creative|entertainment
description: "中文简短描述"
description_en: "English description"
personality: "性格特点"
personality_en: "Personality traits"

# === 来源信息（新增）===
source: "AiShort"
source_url: "https://..."
author: "原作者名"
author_en: "Original Author"

# === 语言信息（新增）===
language: zh|en|zh-en
translated_by: "AI|人工|原文"

# === 热度与标签 ===
hot_score: 50
created_at: "2024-05-09"
tags: [标签1, 标签2]
tags_en: [tag1, tag2]
models: [gpt-4, claude]

# === 验证信息（新增）===
verified: true
verified_type: "高赞|高收藏|效果反馈|博主推荐"
---

# 人格设定内容

## 中文版
[人格设定正文...]

## English Version
[Persona content...]
```

## 字段说明

### 新增字段（必填）

| 字段 | 说明 | 示例值 |
|------|------|--------|
| `source` | 来源平台 | AiShort, Awesome-ChatGPT-Prompts, FlowGPT, 小红书, 知乎 |
| `language` | 原文语言 | zh, en, zh-en |
| `translated_by` | 翻译方式 | AI, 人工, 原文 |
| `verified` | 是否验证 | true, false |
| `verified_type` | 验证类型 | 高赞, 高收藏, 效果反馈, 博主推荐 |

### 新增字段（可选）

| 字段 | 说明 | 示例值 |
|------|------|--------|
| `source_url` | 原始链接 | https://aishort.com/prompt/xxx |
| `author` | 原作者 | 张三 |

## 内容组织规范

### 双语内容格式

**方式一：分段式（推荐）**
```markdown
## 中文版
【译文】
你是一位专业的代码审查工程师...

## English Version
[Translation]
You are a professional code review engineer...
```

**方式二：对照式（适合短内容）**
```markdown
你是一位专业的代码审查工程师 / You are a professional code review engineer
```

### 来源标注规范

- **AiShort**: 国内最大中文提示词社区，热度排序
- **Awesome-ChatGPT-Prompts**: GitHub 12万+ stars 英文库
- **FlowGPT**: 英文社区，有用户投票
- **小红书/知乎**: 散装中文，需筛选
- **Reddit/Twitter**: 英文社区，需筛选

### 验证标准

- **高赞**: 点赞数 > 100（AiShort热度 > 50）
- **高收藏**: 收藏数 > 50
- **效果反馈**: 有用户评论说"好用"/"效果不错"
- **博主推荐**: 知名博主/大V推荐过
