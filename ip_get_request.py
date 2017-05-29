import requests

def ip_get_request():
    client = requests.session()
    template = "http://139.59.22.225:5002/get-ip"
    resp = client.request("GET", template)
    return resp.json()


if __name__ == '__main__':
    print(ip_get_request())
