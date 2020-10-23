import requests

API_URL = 'https://c19norge.no/api/v1'


def metadata(category, subcategory=None):
    res = requests.get(f'{API_URL}/metadata').json()
    meta = res['metadata']

    if subcategory:
        data = meta.get(category, {}).get(subcategory)
    else:
        data = meta.get(category)

    return data


def timeseries(category):
    res = requests.get(f'{API_URL}/timeseries').json()
    meta = res['timeseries']

    data = meta.get(category)

    return data
