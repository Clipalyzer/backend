import requests


def fetch_maps():
    url = "https://valorant-api.com/v1/maps"
    r = requests.get(url)
    maps = [x["displayName"] for x in r.json()["data"]]
    return maps
