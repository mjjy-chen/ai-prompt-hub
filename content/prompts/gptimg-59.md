---
title: "主题海报版式设计"
title_en: ""
description: "GPT Image 2.0 海报/排版风格提示词 - 主题海报版式设计"
description_en: "GPT Image 2.0 Posters & Typography prompt - 主题海报版式设计"
category: "海报/排版"
tags: []
type: IMAGE
source: "awesome-gpt-image-2"
source_url: "https://github.com/freestylefly/awesome-gpt-image-2"
language: "en"
verified: true
verified_type: "community"
hot_score: 144
image_url: "https://gh-proxy.com/https://raw.githubusercontent.com/freestylefly/awesome-gpt-image-2/main/data/images/case59.jpg"
---

## English Prompt

```
{
  "type": "cinematic promotional poster",
  "style": "3D CGI animation style, highly detailed, dramatic lighting, caricature characters",
  "characters": [
    { "id": "char1", "description": "large shirtless man with long black hair, beard, and glasses" },
    { "id": "char2", "description": "elderly woman in a kimono with white hair tied up" },
    { "id": "char3", "description": "small man with a topknot, glasses, mustache, wearing a bright green sweater" }
  ],
  "layout": {
    "panels": [
      {
        "position": "top",
        "scene": "wide shot of a town street with buildings and a city skyline in the background",
        "characters_present": ["char1", "char2", "char3"],
        "text_overlays": [
          "{argument name=\"intro text\" default=\"ある日ーー\"}",
          "いつもの日常がーー",
          "こんばんは"
        ]
      },
      {
        "position": "middle left",
        "scene": "close-up of char1 looking shocked against a dark fiery background",
        "text_overlays": [
          "{argument name=\"shocked text\" default=\"私が出禁？\"}"
        ]
      },
      {
        "position": "middle right",
        "scene": "close-up of char2 looking angry and pointing against a stormy sea background",
        "text_overlays": [
          "{argument name=\"angry text\" default=\"海を荒らすな！\"}"
        ]
      },
      {
        "position": "bottom",
        "scene": "char3 pointing, char1 screaming, a second instance of char3 falling backwards, and char2 sitting angrily against a fiery chaotic background",
        "text_overlays": [
          "全然出ない！"
        ],
        "bottom_titles": [
          "{argument name=\"main title\" default=\"パチンコ軍団親のイメチェン\"}",
          "{argument name=\"subtitle\" default=\"LINEスタンプ販売中\"}"
        ]
      }
    ]
  }
}
```

**Author:** @X64zzotSKCGtYmt ([source](https://x.com/X64zzotSKCGtYmt))
