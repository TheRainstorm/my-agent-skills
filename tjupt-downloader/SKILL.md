---
name: tjupt-downloader
description: Download anime, movies, and TV shows from TJUPT PT station and add to qBittorrent. Use when user wants to download media content from TJUPT (北洋园PT) and add torrents to qBittorrent with specific category. Supports searching https://www.tjupt.org/torrents.php and adding to http://docker.op1:9090/ with categories like Anime1, Movie3, TV1, etc.
---

# TJUPT Downloader

自动化从北洋园 PT 站 (TJUPT) 搜索资源并添加到 qBittorrent 下载。

## 架构设计

本 skill 采用**主从代理架构**：

1. **主代理人 (Main Agent)**：负责与用户交流，确认需求，报告状态
2. **子代理人 (Sub-agent)**：负责执行实际的浏览器操作和下载任务

### 工作流程

```
用户请求 → 主代理人确认 → 创建子代理人执行 → 子代理人汇报 → 主代理人反馈用户
```

## 执行步骤

### 阶段1：需求确认（主代理人执行）

1. 理解用户下载需求（资源名称、目标分类）
2. 确认 qBittorrent 分类（Anime1, Movie3, TV1 等）
3. 向用户确认下载计划

### 阶段2：创建子代理人执行任务

使用 `sessions_spawn` 创建子代理人：

```
runtime: "subagent"
mode: "run"
task: "在 TJUPT 搜索《资源名》，找到所有相关种子，获取磁力链接，添加到 qBittorrent 的《分类》"
```

### 阶段3：监控和汇报（主代理人执行）

1. 等待子代理人完成
2. 获取 qBittorrent 下载状态
3. 向用户汇报结果

## 获取磁力链接的方法

在 TJUPT 种子详情页：
1. 找到"种子名称"下面的"行为"一行
2. "下载种子"右边有"复制种子直链"
3. 点击获取磁力链接（格式：`https://tjupt.org/download.php?id=xxx&passkey=...`）

## qBittorrent API 使用

添加种子：
```bash
curl -X POST "http://docker.op1:9090/api/v2/torrents/add" \
  -F "urls=磁力链接" \
  -F "category=分类名" \
  -F "autoTMM=false"
```

查询状态：
```bash
curl "http://docker.op1:9090/api/v2/torrents/info?category=分类名"
```

## qBittorrent 分类说明

| 分类 | 用途 |
|------|------|
| Anime1 | 动漫资源 |
| Movie3 | 电影资源 |
| TV1 | 电视剧资源 |

## 子代理人任务指令模板

当创建子代理人时，使用以下任务描述：

```
任务：从 TJUPT 下载《资源名》到 qBittorrent 分类《分类名》

步骤：
1. 打开浏览器访问 https://www.tjupt.org/torrents.php
2. 搜索《资源名》
3. 找到所有相关种子（注意集数/版本）
4. 对每个种子：
   a. 打开详情页
   b. 点击"复制种子直链"获取磁力链接
   c. 使用 curl 添加到 qBittorrent:
      curl -X POST "http://docker.op1:9090/api/v2/torrents/add" \
        -F "urls=磁力链接" \
        -F "category=分类名" \
        -F "autoTMM=false"
5. 验证所有种子已添加成功
6. 返回下载结果（成功数量、失败数量、种子列表）

注意：
- TJUPT 需要登录，使用当前浏览器会话
- 磁力链接格式：https://tjupt.org/download.php?id=xxx&passkey=...
- 添加成功后 API 返回 "Ok"
```

## 注意事项

- TJUPT 需要登录才能访问，确保浏览器已保存登录状态
- 分类名称区分大小写，必须完全匹配
- 部分资源可能需要一定的分享率才能下载
- 连载动漫可能没有完整全集，需要逐集下载
