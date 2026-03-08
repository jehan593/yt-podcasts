import os
import requests
from xml.etree.ElementTree import Element, SubElement, tostring

# CONFIGURATION
REPO_OWNER = "jehan593"
REPO_NAME = "yt-podcasts"

# 1. Setup RSS structure
rss = Element('rss', version='2.0', attrib={'xmlns:itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd'})
channel = SubElement(rss, 'channel')

SubElement(channel, 'title').text = "My Termux Podcast"
SubElement(channel, 'description').text = "YouTube audio archived via Termux"
SubElement(channel, 'link').text = f"https://github.com/{REPO_OWNER}/{REPO_NAME}"
SubElement(channel, 'language').text = 'en-us'

# 2. Fetch releases from GitHub API
url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases"
response = requests.get(url)
releases = response.json()

# 3. Build items from assets
for release in releases:
    for asset in release.get('assets', []):
        if asset['name'].endswith('.mp3'):
            item = SubElement(channel, 'item')
            SubElement(item, 'title').text = release.get('name', 'Untitled Episode')
            SubElement(item, 'pubDate').text = release.get('published_at')
            SubElement(item, 'enclosure', {
                'url': asset['browser_download_url'],
                'type': 'audio/mpeg',
                'length': str(asset['size'])
            })
            SubElement(item, 'guid').text = asset['browser_download_url']

# 4. Save the file with the correct 'tostring' call
with open('podcast.xml', 'wb') as f:
    f.write(b'<?xml version="1.0" encoding="UTF-8"?>' + tostring(rss))
