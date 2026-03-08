import os
import json
import datetime
from xml.etree.ElementTree import Element, SubElement, TOString, ElementTree

# CONFIGURATION
REPO_OWNER = "jehan593"
REPO_NAME = "yt-podcasts"
BASE_URL = f"https://github.com/{REPO_OWNER}/{REPO_NAME}/releases/download"

rss = Element('rss', version='2.0', attrib={'xmlns:itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd'})
channel = SubElement(rss, 'channel')

SubElement(channel, 'title').text = "My Termux Podcast"
SubElement(channel, 'description').text = "YouTube audio archived via Termux"
SubElement(channel, 'link').text = f"https://github.com/{REPO_OWNER}/{REPO_NAME}"
SubElement(channel, 'language').text = 'en-us'

# Fetch releases from GitHub API (or use a local cache)
# For simplicity, we'll assume the action provides a list of releases
import requests
url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases"
releases = requests.get(url).json()

for release in releases:
    for asset in release['assets']:
        if asset['name'].endswith('.mp3'):
            item = SubElement(channel, 'item')
            SubElement(item, 'title').text = release['name']
            SubElement(item, 'pubDate').text = release['published_at']
            SubElement(item, 'enclosure', url=asset['browser_download_url'], type='audio/mpeg', length=str(asset['size']))
            SubElement(item, 'guid').text = asset['browser_download_url']

# Save the file
with open('podcast.xml', 'wb') as f:
    f.write(b'<?xml version="1.0" encoding="UTF-8"?>' + TOString(rss))