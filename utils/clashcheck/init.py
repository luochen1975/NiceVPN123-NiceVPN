import re
import os
import yaml
import shutil
import requests
from clash import filter
from yaml import SafeLoader

def init():
    if not os.path.exists('./temp'):
        os.mkdir('temp')

    config = 'config/config.yaml'
    # read from config file
    with open(config, 'r') as reader:
        config = yaml.load(reader, Loader=SafeLoader)
        http_port = config['http-port']
        api_port = config['api-port']
        threads = config['threads']
        source = str(config['source'])
        timeout = config['timeout']
        testurl = config['test-url']
        outfile = config['outfile']
    
    # get clash config file
    headers = {
        'User-Agent': 'ClashforWindows/0.20.39',
        'Accept': 'text/yaml,application/yaml,*/*',
    }
    
    if source.startswith('http://'):
        response = requests.get(source, headers=headers, timeout=30)
        response.raise_for_status()
        raw_text = response.text
        if '<html' in raw_text.lower() or '<!doctype' in raw_text.lower():
            raise ValueError(
                f"Source returned HTML instead of YAML.\n"
                f"URL: {source}\n"
                f"Response preview:\n{raw_text[:500]}"
            )
        proxyconfig = yaml.load(raw_text, Loader=SafeLoader)
        
    elif source.startswith('https://'):
        response = requests.get(source, headers=headers, timeout=30)
        response.raise_for_status()
        raw_text = response.text
        if '<html' in raw_text.lower() or '<!doctype' in raw_text.lower():
            raise ValueError(
                f"Source returned HTML instead of YAML.\n"
                f"URL: {source}\n"
                f"可能原因: ghproxy 服务异常，请尝试更换代理或直接访问 GitHub\n"
                f"Response preview:\n{raw_text[:500]}"
            )
        clean_text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F-\x9F]', '', raw_text)
        proxyconfig = yaml.load(clean_text, Loader=SafeLoader)
        
    else:
        with open(source, 'r') as reader:
            proxyconfig = yaml.load(reader, Loader=SafeLoader)

    # set clash api url
    baseurl = '127.0.0.1:' + str(api_port)
    apiurl = 'http://' + baseurl

    # filter config files
    proxyconfig = filter(proxyconfig)

    config = {'port': http_port, 'external-controller': baseurl, 'mode': 'global',
              'log-level': 'silent', 'proxies': proxyconfig['proxies']}

    with open('./temp/working.yaml', 'w') as file:
        file = yaml.dump(config, file)

    # return all variables
    return http_port, api_port, threads, source, timeout, outfile, proxyconfig, apiurl, testurl, config

def clean(clash):
    shutil.rmtree('./temp')
    clash.terminate()
    exit(0)
