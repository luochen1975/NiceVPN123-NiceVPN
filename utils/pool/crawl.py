import requests
import json
import yaml
import time

def get_file_list():
    try:
        start = time.time()
        url = 'https://api.github.com/repos/changfengoss/pub/git/trees/main?recursive=1'
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        rawdata = response.json()
        data = rawdata['tree']
        dirlist = []
        count = 0
        for x in data:
            dirlist.append(data[count]['path'])
            count = count + 1
        end = time.time()
        return dirlist, count
    except Exception as e:
        print(f"ERROR: Failed to fetch file list from changfengoss/pub: {e}")
        return [], 0

def get_proxies(date, file):
    baseurl = 'https://raw.githubusercontent.com/changfengoss/pub/main/data/'
    response = requests.get(baseurl + date + '/' + file, timeout=30)
    response.raise_for_status()
    working = yaml.safe_load(response.text)
    data_out = []
    for x in working['proxies']:
        data_out.append(x)
    return data_out
