import requests


def get_server_list():
    """Scrap server list from website"""
    servers = []

    # Get configured servers
    response = requests.get("https://iorestoacasa.work/hosts.json")
    for server in response.json()['instances']:
        servers.append(server)

    return servers
