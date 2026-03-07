---
name: tjupt-downloader
description: Download anime, movies, and TV shows from multiple BT/PT sources (TJUPT, 动漫花园) and add to qBittorrent. Use when user wants to download media content and add torrents to qBittorrent with specific category. Supports searching https://www.tjupt.org/torrents.php and https://share.dmhy.org/ with fallback logic.
---

# Multi-Source Downloader (TJUPT + 动漫花园)

自动化从多个 BT/PT 站点搜索资源并添加到 qBittorrent 下载。支持 TJUPT（北洋园 PT）和动漫花园，按优先级搜索。

## 支持站点

| 站点 | URL | 优先级 | 说明 |
|------|-----|--------|------|
| TJUPT | https://www.tjupt.org/torrents.php | 1 | 北洋园 PT，需要登录 |
| 动漫花园 | https://share.dmhy.org/ | 2 | 动漫资源专用站，无需登录 |

## 工作流程

1. **首选 TJUPT 搜索**: 访问 https://www.tjupt.org/torrents.php 搜索资源
2. **如果 TJUPT 无结果**: 自动切换到动漫花园 https://share.dmhy.org/ 搜索
3. **获取磁力链接**: 找到目标资源后提取磁力链接
4. **添加到 qBittorrent**: 通过 Web UI 添加到 http://docker.op1:9090/
5. **选择分类**: 根据用户要求选择对应分类 (Anime1, Movie3, TV1 等)

## qBittorrent 分类说明

分类名称中的数字代表下载到不同磁盘：

| 分类 | 用途 |
|------|------|
| Anime1 | 动漫资源 |
| Movie3 | 电影资源 |
| TV1 | 电视剧资源 |

**注意**: 分类名称必须完全匹配，包括大小写和数字。

## 使用示例

用户指令示例：
- "帮我下载《鬼灭之刃》到 Anime1"
- "搜索电影《沙丘》并添加到 Movie3"
- "找一下《三体》电视剧，下载到 TV1"

## 执行步骤

### TJUPT 搜索

1. 打开 TJUPT 种子页面: https://www.tjupt.org/torrents.php
2. 在搜索框 (ref=e303) 输入关键词并点击搜索 (ref=e319)
3. 检查搜索结果：
   - 如果有结果：找到匹配的资源，获取磁力链接
   - 如果显示"没有种子"：切换到动漫花园搜索

### 动漫花园搜索（TJUPT 无结果时）

1. 打开动漫花园首页: https://share.dmhy.org/
2. 在搜索框输入关键词并搜索
3. 从搜索结果中找到匹配的资源
4. 点击资源进入详情页获取磁力链接

### 添加到 qBittorrent

1. 打开 qBittorrent Web UI: http://docker.op1:9090/
2. 磁力链接位于表格的 "磁鏈" 列里的向下箭头上
3. 粘贴磁力链接
4. 设置分类（Anime1/Movie3/TV1 等）
5. 确认开始下载

## 搜索关键词策略

- **优先尝试完整名称**: 如"魔王的女儿过于温柔"
- **如果无结果，尝试简化**: 如"魔王的女儿"
- **可以尝试日文/英文原名**: 如果中文名无结果

## 注意事项

- **TJUPT 需要登录**: 确保浏览器已保存登录状态
- **动漫花园无需登录**: 可直接访问搜索
- **分类名称必须正确**: Anime1, Movie3, TV1 等
- **部分资源可能需要分享率**: TJUPT 部分资源有下载限制
- **优先 TJUPT**: 因为是 PT 站，资源质量通常更高
- **动漫花园作为备选**: 专门针对动漫资源，更新较快

## 站点选择逻辑

```
用户请求下载
    ↓
搜索 TJUPT
    ↓
有结果？───是───→ 获取磁力链接 → 添加到 qBittorrent
    ↓ 否
搜索动漫花园
    ↓
有结果？───是───→ 获取磁力链接 → 添加到 qBittorrent
    ↓ 否
告知用户无资源
```
