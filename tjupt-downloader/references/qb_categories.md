# qBittorrent 分类配置

## 可用分类

| 分类名称 | 用途 | 存储位置 |
|---------|------|---------|
| Anime1 | 动漫/动画资源 | 磁盘1 |
| Movie3 | 电影资源 | 磁盘3 |
| TV1 | 电视剧资源 | 磁盘1 |

## 使用说明

- 分类名称区分大小写，必须完全匹配
- 数字后缀表示目标磁盘编号
- 添加 torrent 时必须指定正确的分类，否则可能下载到错误位置

## 添加 Torrent 的 API

```
POST /api/v2/torrents/add

Parameters:
- urls: 磁力链接或 HTTP URL (多个用换行分隔)
- category: 分类名称 (如 Anime1, Movie3, TV1)
- autoTMM: 是否使用自动种子管理 (true/false)
```
