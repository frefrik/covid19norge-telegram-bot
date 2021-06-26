import requests

API_URL = "https://covid19norge.no/api/v1"


def metadata(category, subcategory=None):
    res = requests.get(f"{API_URL}/current").json()
    meta = res["data"]

    if subcategory:
        data = meta.get(category, {}).get(subcategory)
    else:
        data = meta.get(category)

    return data


def timeseries(category):
    res = requests.get(f"{API_URL}/timeseries/{category}").json()
    data = res[category]

    return data
