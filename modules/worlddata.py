import requests
import json
import pandas as pd

def fetch_newdata():
    url = 'https://pomber.github.io/covid19/timeseries.json'
    res = requests.get(url).json()

    return res

def timeseries_country(country):
    df_newdata = pd.DataFrame(fetch_newdata())

    df = pd.DataFrame(columns=['date', 'confirmed', 'deaths', 'recovered', 'country', 'country_lower'])

    for c in df_newdata.columns.unique().tolist():
        country_data =  pd.json_normalize(df_newdata[c]).set_index('date').reset_index()
        country_data['country'] = c
        country_data['country_lower'] = c.lower()

        df = pd.concat([df, country_data])

    df.reset_index(drop=True, inplace=True)
    df['date'] = pd.to_datetime(df['date'])
    try:
        df = df.loc[df['country_lower'] == country.lower()]

        return df
    except KeyError:
        print('Couldnt find country:', country)

def timeseries_all():
    df_newdata = pd.DataFrame(fetch_newdata())

    df = pd.DataFrame(columns=['date', 'confirmed', 'deaths', 'recovered', 'country', 'country_lower'])

    for country in df_newdata.columns.unique().tolist():
        country_data =  pd.json_normalize(df_newdata[country]).set_index('date').reset_index()

        country_data['country'] = country
        country_data['country_lower'] = country.lower()
        df = pd.concat([df, country_data])

    df.reset_index(drop=True, inplace=True)
    df['date'] = pd.to_datetime(df['date'])

    print(df.loc[df['country_lower'] == 'united kingdom'])

def get_current(country):
    data = fetch_newdata()

    for key, value in data.items():
        if key.upper() == country.upper():
            current = data[key][-1]

            return key, current
