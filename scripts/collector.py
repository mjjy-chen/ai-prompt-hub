#!/usr/bin/env python3
"""
AI Prompt Hub 内容采集器
支持半自动和全自动模式
"""

import os
import re
import yaml
import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent.parent
CONTENT_DIR = BASE_DIR / "content"
CONFIG_FILE = BASE_DIR / "config.yml"

class ContentCollector:
    def __init__(self):
        self.config = self._load_config()
        
    def _load_config(self):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    
    def _generate_slug(self, title):
        """生成URL友好的slug"""
        slug = re.sub(r'[^\w\s-]', '', title).strip().lower()
        slug = re.sub(r'[-\s]+', '-', slug)
        return slug[:50]
    
    def _get_next_id(self, content_type):
        """获取下一个ID编号"""
        content_dir = CONTENT_DIR / content_type
        if not content_dir.exists():
            return 1
        
        existing = list(content_dir.glob("*.md"))
        if not existing:
            return 1
        
        numbers = []
        for f in existing:
            match = re.search(r'-?(\d+)\.md$', f.name)
            if match:
                numbers.append(int(match.group(1)))
        
        return max(numbers) + 1 if numbers else 1
    
    def create_prompt(self, title, category, description, content, 
                      models=None, tags=None, hot_score=50):
        """创建新的提示词文件"""
        
        slug = f"{category}-{self._get_next_id('prompts'):03d}"
        filepath = CONTENT_DIR / "prompts" / f"{slug}.md"
        
        frontmatter = {
            "title": title,
            "category": category,
            "description": description,
            "models": models or ["gpt-4"],
            "author": "自动采集",
            "hot_score": hot_score,
            "created_at": datetime.now().strftime("%Y-%m-%d"),
            "tags": tags or []
        }
        
        # 构建markdown内容
        md_content = f"""---
{yaml.dump(frontmatter, allow_unicode=True)}---

{content}
"""
        
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(md_content)
        
        print(f"✅ 已创建提示词: {filepath}")
        return filepath
    
    def create_agent(self, title, category, description, personality,
                     content, models=None, tags=None, hot_score=50):
        """创建新的Agent人格文件"""
        
        slug = f"{category}-{self._get_next_id('agents'):03d}"
        filepath = CONTENT_DIR / "agents" / f"{slug}.md"
        
        frontmatter = {
            "title": title,
            "category": category,
            "description": description,
            "personality": personality,
            "models": models or ["gpt-4"],
            "author": "自动采集",
            "hot_score": hot_score,
            "created_at": datetime.now().strftime("%Y-%m-%d"),
            "tags": tags or []
        }
        
        md_content = f"""---
{yaml.dump(frontmatter, allow_unicode=True)}---

{content}
"""
        
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(md_content)
        
        print(f"✅ 已创建Agent: {filepath}")
        return filepath
    
    def batch_import(self, json_file):
        """从JSON文件批量导入内容"""
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        for item in data.get("prompts", []):
            self.create_prompt(**item)
        
        for item in data.get("agents", []):
            self.create_agent(**item)
        
        print(f"✅ 批量导入完成: {len(data.get('prompts', []))} 个提示词, {len(data.get('agents', []))} 个Agent")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="AI Prompt Hub 内容采集器")
    parser.add_argument("--batch", help="从JSON文件批量导入")
    parser.add_argument("--prompt", action="store_true", help="创建单个提示词")
    parser.add_argument("--agent", action="store_true", help="创建单个Agent")
    
    args = parser.parse_args()
    
    collector = ContentCollector()
    
    if args.batch:
        collector.batch_import(args.batch)
    else:
        print("使用 --batch <json文件> 批量导入")
        print("或使用 --prompt/--agent 创建单个内容")
