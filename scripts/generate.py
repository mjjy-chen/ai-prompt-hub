#!/usr/bin/env python3
"""
AI Prompt Hub 站点生成器
将Markdown内容转换为静态HTML站点
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
OUTPUT_DIR = BASE_DIR / "dist"

def load_config():
    """加载站点配置"""
    with open(BASE_DIR / "config.yml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def parse_markdown_file(filepath):
    """解析Markdown文件，提取frontmatter和内容"""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 提取frontmatter
    match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)
    if not match:
        return None, None
    
    frontmatter = yaml.safe_load(match.group(1))
    body = match.group(2).strip()
    
    return frontmatter, body

def load_all_content():
    """加载所有内容文件"""
    prompts = []
    agents = []
    
    # 加载提示词
    prompts_dir = CONTENT_DIR / "prompts"
    if prompts_dir.exists():
        for file in prompts_dir.glob("*.md"):
            meta, body = parse_markdown_file(file)
            if meta:
                meta["body"] = body
                meta["slug"] = file.stem
                prompts.append(meta)
    
    # 加载人格设定
    agents_dir = CONTENT_DIR / "agents"
    if agents_dir.exists():
        for file in agents_dir.glob("*.md"):
            meta, body = parse_markdown_file(file)
            if meta:
                meta["body"] = body
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
    
    # 生成首页 - 根目录，路径前缀为 ""
    template = env.get_template("index.html")
    html = template.render(
        config=config,
        prompts=prompts[:10],
        agents=agents[:6],
        now=datetime.now(),
        base_path=""  # 根目录
    )
    with open(OUTPUT_DIR / "index.html", "w", encoding="utf-8") as f:
        f.write(html)
    
    # 生成提示词列表页 - 在prompts/目录下，路径前缀为 "../"
    template = env.get_template("prompts.html")
    html = template.render(
        config=config,
        prompts=prompts,
        categories=config["categories"]["prompts"],
        base_path="../"  # 上一级目录
    )
    (OUTPUT_DIR / "prompts").mkdir(exist_ok=True)
    with open(OUTPUT_DIR / "prompts" / "index.html", "w", encoding="utf-8") as f:
        f.write(html)
    
    # 生成人格设定列表页 - 在agents/目录下，路径前缀为 "../"
    template = env.get_template("agents.html")
    html = template.render(
        config=config,
        agents=agents,
        categories=config["categories"]["agents"],
        base_path="../"  # 上一级目录
    )
    (OUTPUT_DIR / "agents").mkdir(exist_ok=True)
    with open(OUTPUT_DIR / "agents" / "index.html", "w", encoding="utf-8") as f:
        f.write(html)
    
    # 生成详情页
    template = env.get_template("detail.html")
    md = markdown.Markdown(extensions=['fenced_code', 'tables'])
    
    for item in prompts + agents:
        html_content = md.convert(item["body"])
        html = template.render(
            config=config,
            item=item,
            content=html_content,
            type="prompt" if item in prompts else "agent",
            base_path="../../"  # 上两级目录
        )
        
        subdir = "prompts" if item in prompts else "agents"
        (OUTPUT_DIR / subdir / item["slug"]).mkdir(parents=True, exist_ok=True)
        with open(OUTPUT_DIR / subdir / item["slug"] / "index.html", "w", encoding="utf-8") as f:
            f.write(html)
        md.reset()
    
    # 复制静态资源
    os.system(f"cp -r {BASE_DIR}/assets/* {OUTPUT_DIR}/")
    
    # 生成搜索数据
    generate_search_data(prompts, agents)
    
    print(f"✅ 站点生成完成！共 {len(prompts)} 个提示词，{len(agents)} 个人格设定")
    print(f"📁 输出目录: {OUTPUT_DIR}")

def generate_search_data(prompts, agents):
    """生成搜索数据JSON"""
    search_data = []
    
    for item in prompts:
        search_data.append({
            "title": item.get("title", ""),
            "description": item.get("description", ""),
            "tags": item.get("tags", []),
            "url": f"/prompts/{item['slug']}/",
            "type": "prompt",
            "category": item.get("category", "")
        })
    
    for item in agents:
        search_data.append({
            "title": item.get("title", ""),
            "description": item.get("description", ""),
            "tags": item.get("tags", []),
            "url": f"/agents/{item['slug']}/",
            "type": "agent",
            "category": item.get("category", "")
        })
    
    with open(OUTPUT_DIR / "search.json", "w", encoding="utf-8") as f:
        json.dump(search_data, f, ensure_ascii=False, indent=2)
    
    print(f"🔍 搜索数据已生成: {len(search_data)} 条记录")

if __name__ == "__main__":
    generate_site()
