# AI Prompt Hub

精选AI提示词与Agent人格设定库

## 快速开始

```bash
# 1. 克隆仓库
git clone <your-repo>
cd ai-prompt-hub

# 2. 安装依赖
pip install pyyaml markdown jinja2

# 3. 生成站点
python scripts/generate.py

# 4. 查看结果
# 输出在 dist/ 目录
```

## 内容格式

### 提示词 (content/prompts/)

```yaml
---
title: "标题"
category: writing|coding|drawing|data|chat|other
description: "简短描述"
models: [gpt-4, claude, kimi]
author: "作者"
hot_score: 50  # 热度 0-100
created_at: "2024-05-09"
tags: [标签1, 标签2]
---

# 提示词内容...
```

### 人格设定 (content/agents/)

```yaml
---
title: "标题"
category: professional|creative|entertainment
description: "简短描述"
personality: "性格特点"
models: [gpt-4, claude]
author: "作者"
hot_score: 50
created_at: "2024-05-09"
tags: [标签1, 标签2]
---

# 人格设定内容...
```

## 批量导入

```bash
# 使用 collector.py 批量导入
python scripts/collector.py --batch examples/batch-import.json
```

## 自动部署

GitHub Actions 配置在 `.github/workflows/deploy.yml`

- 每次 push 到 main 分支自动部署
- 每6小时检查是否有内容更新
- 部署到 GitHub Pages

## 目录结构

```
ai-prompt-hub/
├── config.yml          # 站点配置
├── content/            # 内容目录
│   ├── prompts/        # 提示词
│   └── agents/         # 人格设定
├── scripts/            # 脚本
│   ├── generate.py     # 站点生成
│   └── collector.py    # 内容采集
├── templates/          # HTML模板
├── assets/             # 静态资源
└── .github/workflows/  # CI/CD
```

## 追热点策略

1. **监控渠道** (config.yml 中配置)
   - 国内：知乎、即刻、小红书、微信公众号
   - 国际：Twitter、Reddit、GitHub Trending

2. **采集流程**
   - 半自动：我抓取 → 你审核 → 批量导入
   - 全自动：定时抓取 → AI筛选 → 自动发布

3. **热度算法**
   - 来源平台热度
   - 点赞/转发数
   - 时效性加权

## 会员功能 (后期)

- 免费用户：每日查看10条
- 会员(¥9.9永久)：无限制访问

## License

MIT
