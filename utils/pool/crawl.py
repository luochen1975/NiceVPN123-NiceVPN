import requests
import json
import yaml
import time
import os

def get_file_list():
    try:
        start = time.time()
        url = 'https://api.github.com/repos/changfengoss/pub/git/trees/main?recursive=1'
        headers = {}
        if 'GITHUB_TOKEN' in os.environ:
            headers['Authorization'] = f'token {os.environ["GITHUB_TOKEN"]}'
        
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        rawdata = response.json()
        data = rawdata['tree']
        dirlist = []
        count = 0
        for x in data:
            dirlist.append(data[count]['path'])
            count = count + 1
        end = time.time()
        print(f"Fetch succeeded in {end-start:.2f} seconds, {count} files")
        return dirlist, count
    except Exception as e:
        print(f"ERROR: Failed to fetch file list: {e}")
        return [], 0

def get_proxies(date, file):
    baseurl = 'https://raw.githubusercontent.com/changfengoss/pub/main/data/'
    try:
        response = requests.get(baseurl + date + '/' + file, timeout=30)
        response.raise_for_status()
        working = yaml.safe_load(response.text)
        data_out = []
        for x in working['proxies']:
            data_out.append(x)
        return data_out
    except Exception as e:
        print(f"Error fetching {date}/{file}: {e}")
        return []
