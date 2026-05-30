#!/usr/bin/env python3
"""
AI Prompt Hub 站点生成器 v2.0
支持中英双语、来源标注、原文/译文切换
"""

import os
import re
import json
import yaml
import markdown
from pathlib import Path
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

BASE_DIR = Path(__file__).parent.parent
CONTENT_DIR = BASE_DIR / "content"
TEMPLATE_DIR = BASE_DIR / "templates"
OUTPUT_DIR = BASE_DIR / "docs"

def load_config():
    """加载站点配置"""
    with open(BASE_DIR / "config.yml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def parse_markdown_file(filepath):
    """解析Markdown文件，提取frontmatter和内容，支持中英分段"""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 提取frontmatter
    match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)
    if not match:
        return None, None, None
    
    frontmatter = yaml.safe_load(match.group(1))
    body = match.group(2).strip()
    
    # 按语言标记分割中英内容
    # 文件结构可能是：
    # 1) ## English Version → 英文, ## 中文版 → 中文
    # 2) ## 中文版 → 中文, ## English Version → 英文
    # 3) 无标记 → 全部作为body
    body_zh = None
    body_en = None
    
    # 查找所有 ## 标题位置（包括body开头的标题）
    headings = list(re.finditer(r'(?:^|\n)##\s+(.+?)\s*\n', body))
    
    en_start = None
    zh_start = None
    
    for h in headings:
        title = h.group(1).strip().lower()
        if 'english' in title or '英文' in title:
            en_start = h.end()
        elif '中文' in title or 'chinese' in title:
            zh_start = h.end()
    
    if en_start and zh_start:
        # 两个都有，按位置分割
        en_heading = next(h for h in headings if 'english' in h.group(1).lower() or '英文' in h.group(1).lower())
        zh_heading = next(h for h in headings if '中文' in h.group(1).lower() or 'chinese' in h.group(1).lower())
        
        if en_heading.start() < zh_heading.start():
            # 英文在前，中文在后
            body_en = body[en_start:zh_heading.start()].strip()
            body_zh = body[zh_start:].strip()
        else:
            # 中文在前，英文在后
            body_zh = body[zh_start:en_heading.start()].strip()
            body_en = body[en_start:].strip()
        
        # 去掉分隔线（---）和翻译标记
        body_en = re.sub(r'^---\s*\n', '', body_en)
        body_zh = re.sub(r'^---\s*\n', '', body_zh)
        body_zh = re.sub(r'^> 以下为英文原文的中文翻译.*?\n\n?', '', body_zh)
        body_en = re.sub(r'^\[Translation\]\s*', '', body_en)
    elif en_start:
        # 只有英文版标记
        en_heading = next(h for h in headings if 'english' in h.group(1).lower() or '英文' in h.group(1).lower())
        body_en = body[en_start:].strip()
        body_zh = body[:en_heading.start()].strip()
        # 如果中文部分为空，说明英文版就是全部
        if not body_zh:
            body_zh = None
    elif zh_start:
        # 只有中文版标记
        zh_heading = next(h for h in headings if '中文' in h.group(1).lower() or 'chinese' in h.group(1).lower())
        body_zh = body[zh_start:].strip()
        body_en = body[:zh_heading.start()].strip()
        if not body_en:
            body_en = None
    else:
        # 无语言标记，根据language字段判断
        lang = frontmatter.get('language', 'zh')
        if lang == 'en':
            body_en = body
        else:
            body_zh = body
    
    frontmatter["body_zh"] = body_zh
    frontmatter["body_en"] = body_en
    frontmatter["body"] = body
    
    return frontmatter, body_zh, body_en

def load_all_content():
    """加载所有内容文件"""
    prompts = []
    agents = []
    
    # 加载提示词
    prompts_dir = CONTENT_DIR / "prompts"
    if prompts_dir.exists():
        for file in sorted(prompts_dir.glob("*.md")):
            meta, body_zh, body_en = parse_markdown_file(file)
            if meta:
                meta["slug"] = file.stem
                prompts.append(meta)
    
    # 加载人格设定
    agents_dir = CONTENT_DIR / "agents"
    if agents_dir.exists():
        for file in sorted(agents_dir.glob("*.md")):
            meta, body_zh, body_en = parse_markdown_file(file)
            if meta:
                meta["slug"] = file.stem
                agents.append(meta)
    
    # 按热度排序
    prompts.sort(key=lambda x: x.get("hot_score", 0), reverse=True)
    agents.sort(key=lambda x: x.get("hot_score", 0), reverse=True)
    
    return prompts, agents

def generate_site():
    """生成静态站点"""
    config = load_config()
    prompts, agents = load_all_content()
    
    # 创建输出目录
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # 设置模板环境
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    md = markdown.Markdown(extensions=['fenced_code', 'tables'])
    
    # 生成首页
    template = env.get_template("index.html")
    html = template.render(
        config=config,
        prompts=prompts[:12],
        agents=agents[:6],
        now=datetime.now(),
        base_path=""
    )
    with open(OUTPUT_DIR / "index.html", "w", encoding="utf-8") as f:
        f.write(html)
    
    # 生成提示词列表页
    template = env.get_template("prompts.html")
    html = template.render(
        config=config,
        prompts=prompts,
        categories=config["categories"]["prompts"],
        base_path="../"
    )
    (OUTPUT_DIR / "prompts").mkdir(exist_ok=True)
    with open(OUTPUT_DIR / "prompts" / "index.html", "w", encoding="utf-8") as f:
        f.write(html)
    
    # 生成人格设定列表页
    template = env.get_template("agents.html")
    html = template.render(
        config=config,
        agents=agents,
        categories=config["categories"]["agents"],
        base_path="../"
    )
    (OUTPUT_DIR / "agents").mkdir(exist_ok=True)
    with open(OUTPUT_DIR / "agents" / "index.html", "w", encoding="utf-8") as f:
        f.write(html)
    
    # 生成详情页
    template = env.get_template("detail.html")
    
    for item in prompts + agents:
        # 渲染中文内容
        content_zh = md.convert(item.get("body_zh", item.get("body", "")))
        md.reset()
        
        # 渲染英文内容
        content_en = None
        if item.get("body_en"):
            content_en = md.convert(item["body_en"])
            md.reset()
        
        # 通用content（兼容旧模板）
        content = md.convert(item.get("body", ""))
        md.reset()
        
        html = template.render(
            config=config,
            item=item,
            content=content,
            content_zh=content_zh,
            content_en=content_en,
            type="prompt" if item in prompts else "agent",
            base_path="../../"
        )
        
        subdir = "prompts" if item in prompts else "agents"
        (OUTPUT_DIR / subdir / item["slug"]).mkdir(parents=True, exist_ok=True)
        with open(OUTPUT_DIR / subdir / item["slug"] / "index.html", "w", encoding="utf-8") as f:
            f.write(html)
    
    # 复制静态资源
    os.system(f"cp -r {BASE_DIR}/assets/* {OUTPUT_DIR}/")
    
    # 生成搜索数据
    generate_search_data(prompts, agents)
    
    print(f"✅ 站点生成完成！共 {len(prompts)} 个提示词，{len(agents)} 个人格设定")
    print(f"📁 输出目录: {OUTPUT_DIR}")

def generate_search_data(prompts, agents):
    """生成搜索数据JSON（含双语+来源）"""
    search_data = []
    
    for item in prompts:
        search_data.append({
            "title": item.get("title", ""),
            "title_en": item.get("title_en", ""),
            "description": item.get("description", ""),
            "description_en": item.get("description_en", ""),
            "tags": item.get("tags", []),
            "tags_en": item.get("tags_en", []),
            "url": f"/prompts/{item['slug']}/",
            "type": "prompt",
            "category": item.get("category", ""),
            "source": item.get("source", ""),
            "language": item.get("language", "zh"),
            "verified": item.get("verified", False)
        })
    
    for item in agents:
        search_data.append({
            "title": item.get("title", ""),
            "title_en": item.get("title_en", ""),
            "description": item.get("description", ""),
            "description_en": item.get("description_en", ""),
            "tags": item.get("tags", []),
            "tags_en": item.get("tags_en", []),
            "url": f"/agents/{item['slug']}/",
            "type": "agent",
            "category": item.get("category", ""),
            "source": item.get("source", ""),
            "language": item.get("language", "zh"),
            "verified": item.get("verified", False)
        })
    
    with open(OUTPUT_DIR / "search.json", "w", encoding="utf-8") as f:
        json.dump(search_data, f, ensure_ascii=False, indent=2)
    
    print(f"🔍 搜索数据已生成: {len(search_data)} 条记录")

if __name__ == "__main__":
    generate_site()
