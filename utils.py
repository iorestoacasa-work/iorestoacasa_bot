import requests


def get_server_list():
    """Scrap server list from website"""
    servers = []

    # Get configured servers
    response = requests.get("https://iorestoacasa.work/hosts.json")
    for server in response.json()['instances']:
        for key in server:
            # Sanitize names
            if key == "by" or key == "name":
                server[key] = server[key].replace('[', '(')
                server[key] = server[key].replace(']', ')')

        servers.append(server)

    return servers
