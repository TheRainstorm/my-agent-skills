#!/usr/bin/env python3
"""
Add torrent to qBittorrent via Web API
Usage: python add_to_qb.py <magnet_link_or_torrent_url> <category>
"""

import sys
import requests
import urllib.parse

QBITTORRENT_URL = "http://docker.op1:9090"


def add_torrent(link: str, category: str):
    """Add torrent to qBittorrent with specified category"""

    # Login to qBittorrent (cookie-based auth)
    session = requests.Session()

    # Try to add torrent
    add_url = f"{QBITTORRENT_URL}/api/v2/torrents/add"

    data = {
        "urls": link,
        "category": category,
        "autoTMM": "false",
    }

    # Check if it's a magnet link or torrent file URL
    if link.startswith("magnet:"):
        # Magnet link - use urls parameter
        response = session.post(add_url, data=data)
    elif link.endswith(".torrent") or "/download.php" in link:
        # Torrent file - need to download first
        torrent_response = session.get(link)
        if torrent_response.status_code == 200:
            files = {"torrents": ("file.torrent", torrent_response.content)}
            data.pop("urls", None)
            response = session.post(add_url, data=data, files=files)
        else:
            print(f"Failed to download torrent file: {torrent_response.status_code}")
            sys.exit(1)
    else:
        # Try as URL
        response = session.post(add_url, data=data)

    if response.status_code == 200:
        if "Ok" in response.text or response.text == "":
            print(f"✓ Successfully added to category '{category}'")
        else:
            print(f"Response: {response.text}")
    elif response.status_code == 403:
        print("✗ Authentication required. Please ensure you're logged into qBittorrent Web UI.")
        sys.exit(1)
    else:
        print(f"✗ Failed to add torrent: HTTP {response.status_code}")
        print(f"Response: {response.text}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python add_to_qb.py <magnet_link_or_url> <category>")
        print("Example: python add_to_qb.py 'magnet:?xt=...' Anime1")
        sys.exit(1)

    link = sys.argv[1]
    category = sys.argv[2]

    add_torrent(link, category)
