import json
import re

import requests
from bs4 import BeautifulSoup

def get_server_list():
    """Scrap server list from website"""
    servers = []

    # Get configured servers
    response = requests.get("https://iorestoacasa.work/hosts.json")
    for server in response.json():
        servers.append(server)


    # Get hardcoded server
    response = requests.get("https://iorestoacasa.work")
    soup = BeautifulSoup(response.text, 'html.parser')

    for script in soup.find_all("script"):
        if "fixed_hosts" in str(script):
            try:
                found = re.search('fixed_hosts([\s\S]+?)]', str(script)).group(1)
            except AttributeError:
                print("error")
                found = None
           
            t = '['
            
            for row in found[3:].split('\n'):
                row = row.strip()
                if ":" in row:
                    row = row.replace(': ', '": ')
                    row = '"' + row
                t += row
            t += ']'

            for server in json.loads(t):
                servers.append(server)

    return servers
