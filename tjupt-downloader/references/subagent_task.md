# 子代理人任务指令

## 任务描述模板

当主代理人创建子代理人时，使用以下任务指令：

### 标准下载任务

```
任务：从 TJUPT 下载资源到 qBittorrent

资源名称：{resource_name}
目标分类：{category}

执行步骤：

1. **搜索资源**
   - 打开浏览器访问 https://www.tjupt.org/torrents.php
   - 在搜索框输入"{resource_name}"
   - 点击"给我搜"按钮

2. **分析搜索结果**
   - 查看所有匹配的种子
   - 注意集数、字幕组、格式等信息
   - 确定需要下载的种子列表

3. **获取磁力链接**
   对每个要下载的种子：
   a. 点击种子标题进入详情页
   b. 找到"种子名称"下方的"行为"一行
   c. 点击"复制种子直链"获取磁力链接
   d. 记录磁力链接（格式：https://tjupt.org/download.php?id=xxx&passkey=...）

4. **添加到 qBittorrent**
   对每个磁力链接执行：
   ```bash
   curl -X POST "http://docker.op1:9090/api/v2/torrents/add" \
     -F "urls=磁力链接" \
     -F "category={category}" \
     -F "autoTMM=false"
   ```
   - 成功时 API 返回 "Ok" 或空字符串

5. **验证下载**
   - 查询 qBittorrent 确认种子已添加：
   ```bash
   curl "http://docker.op1:9090/api/v2/torrents/info?category={category}"
   ```
   - 检查新添加的种子状态

6. **返回结果**
   向主代理人报告：
   - 成功添加的种子数量
   - 失败的种子（如有）
   - 每个种子的名称和状态
   - 总大小估计

注意事项：
- TJUPT 需要登录状态，使用当前浏览器会话
- 如果搜索无结果，尝试简化关键词
- 连载动漫可能没有全集，需要逐集下载
- 磁力链接包含 passkey，不要泄露
```

## 返回格式

子代理人完成任务后，返回以下格式的报告：

```json
{
  "status": "success|partial|failed",
  "resource_name": "资源名称",
  "category": "分类名",
  "total_found": 6,
  "success_count": 5,
  "failed_count": 1,
  "torrents": [
    {
      "name": "种子名称",
      "episode": "第几集",
      "size": "大小",
      "status": "added|failed",
      "message": "状态信息"
    }
  ],
  "notes": "额外说明（如连载状态、缺失集数等）"
}
```
