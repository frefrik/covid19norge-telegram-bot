import pandas as pd
import altair as alt
from altair_saver import save
import requests
import json
import datetime
import os
from vg import VG
from utils import get_nordic_df, get_timeseries_df

vg = VG()

def tested():
    filename = './graphs/no_tested.png'
    if os.path.exists(filename):
        os.remove(filename)

    fhi = vg.get_json('fhi')
    fhi = fhi['tested']['timeseries']

    df_fhi = pd.json_normalize(fhi)
    df_fhi = df_fhi[['date', 'count', 'new']].dropna(subset=['count']).fillna(0)
    df_fhi['date'] = pd.to_datetime(df_fhi['date'])

    idx = pd.date_range(df_fhi['date'].min(), df_fhi['date'].max())

    df_fhi.index = pd.DatetimeIndex(df_fhi['date'])
    df_fhi = df_fhi.reindex(idx)
    df_fhi['date'] = df_fhi.index
    df_fhi['new'] = df_fhi['new'].fillna(0)
    df_fhi['count'] = df_fhi['count'].fillna(method='ffill')
    df_fhi = df_fhi.reset_index(drop=True)

    base = alt.Chart(df_fhi).encode(
        alt.X('monthdate(date):O', axis=alt.Axis(title=None))
    )

    bar = base.mark_bar(color='green', opacity=0.3).encode(
        y=alt.Y('new:Q',
            axis=alt.Axis(title='Antall testet per dag'))
    )

    line = base.mark_line(color='red').encode(
        y=alt.Y('count:Q',
            axis=alt.Axis(title='Antall testet totalt'))
    )

    chart = alt.layer(bar, line).resolve_scale(
        y = 'independent'
    ).properties(
        width=1200,
        height=600
    )

    save(chart, filename)

    return(
        open(filename, 'rb')
    )

def confirmed():
    filename = './graphs/no_confirmed.png'
    if os.path.exists(filename):
        os.remove(filename)

    df = get_timeseries_df()
    
    base = alt.Chart(df).encode(
        alt.X('monthdate(date):O', axis=alt.Axis(title=None))
    )

    bar = base.mark_bar(color='steelblue', opacity=0.5).encode(
        y=alt.Y('new_confirmed:Q',
            axis=alt.Axis(title='Antall smittede per dag'))
    )

    line = base.mark_line(color='red').encode(
        y=alt.Y('total_confirmed:Q',
            axis=alt.Axis(title='Antall smittede totalt'))
    )

    chart = alt.layer(bar, line).resolve_scale(
        y = 'independent'
    ).properties(
        width=1200,
        height=600
    )

    chart.save(filename)

    return(
        open(filename, 'rb')
    )

def dead():
    filename = './graphs/no_dead.png'
    if os.path.exists(filename):
        os.remove(filename)

    df = get_timeseries_df()
    df = df[df.date >= '2020-02-25']

    base = alt.Chart(df).encode(
        alt.X('monthdate(date):O', axis=alt.Axis(title=None))
    )

    bar = base.mark_bar(color='purple', opacity=0.3).encode(
        y=alt.Y('new_dead:Q',
            axis=alt.Axis(title='Antall dødsfall per dag'))
    )

    line = base.mark_line(color='red').encode(
        y=alt.Y('total_dead:Q',
            axis=alt.Axis(title='Antall dødsfall totalt'))
    )

    chart = alt.layer(bar, line).resolve_scale(
        y = 'independent'
    ).properties(
        width=1200,
        height=600
    )

    save(chart, filename)

    return(
        open(filename, 'rb')
    )

def hospitalized():
    filename = './graphs/no_hospitalized.png'
    if os.path.exists(filename):
        os.remove(filename)

    reports = vg.get_json('reports')
    ts = reports['hospitals']['timeseries']['total']

    df = pd.DataFrame(ts)
    df = df[df.date >= '2020-03-09'].fillna(0)

    df_melt = pd.melt(df, id_vars=['date'], value_vars=['hospitalized', 'respiratory', 'intensiveCare'], value_name='value').replace({'hospitalized': 'Innlagt', 'respiratory': 'På respirator', 'intensiveCare': 'Intensiv'})

    chart = alt.Chart(df_melt).mark_area(line={}, opacity=0.3).encode(
        x=alt.X('monthdate(date):O', title='Dato'),
        y=alt.Y('value:Q', stack=None, title='Antall'),
        color=alt.Color('variable:N', title=None)
    ).properties(
        width=1200,
        height=600
    )

    save(chart, filename)

    return(
        open(filename, 'rb')
    )

def nordic_confirmed():
    filename = './graphs/nordic_confirmed.png'
    if os.path.exists(filename):
        os.remove(filename)

    df = get_nordic_df()
    df = df[df.date >= '2020-03-01']

    df['cumulativeInfected_per100k'] = df['cumulativeInfected']/(df['population']/100000)

    chart = alt.Chart(df).mark_line().encode(
        x=alt.X('monthdate(date):O', title='Dato'),
        y=alt.Y('cumulativeInfected_per100k:Q', title='Antall smittede per 100k innbygger'),
        color='Land'
    ).properties(
        width=1000,
        height=600
    )

    save(chart, filename)

    return(
        open(filename, 'rb')
    )

def nordic_dead():
    filename = './graphs/nordic_dead.png'
    if os.path.exists(filename):
        os.remove(filename)
    
    df = get_nordic_df()

    df = df[['date', 'Land', 'population', 'cumulativeDeaths', 'newDeaths']]

    df['cumulativeDeaths_per100k'] = df['cumulativeDeaths']/(df['population']/100000)
    df = df[df.date >= '2020-03-14']

    chart = alt.Chart(df).mark_line().encode(
        x=alt.X('monthdate(date):O', title='Dato'),
        y=alt.Y('cumulativeDeaths_per100k:Q', title='Antall døde per 100k innbygger'),
        color='Land'
    ).properties(
        width=1000,
        height=600
    )

    save(chart, filename)

    return(
        open(filename, 'rb')
    )

def nordic_hospitalized():
    filename = './graphs/nordic_hospitalized.png'
    if os.path.exists(filename):
        os.remove(filename)
    
    df = get_nordic_df()

    df = df[['date', 'Land', 'population', 'currentTotalHospitalised']]

    df['currentTotalHospitalised_per100k'] = df['currentTotalHospitalised']/(df['population']/100000)
    df = df[df.date >= '2020-03-09']

    chart = alt.Chart(df).mark_line().encode(
        x=alt.X('monthdate(date):O', title='Dato'),
        y=alt.Y('currentTotalHospitalised_per100k:Q', title='Antall innlagte per 100k innbygger'),
        color='Land'
    ).properties(
        width=1200,
        height=600
    )

    save(chart, filename)

    return(
        open(filename, 'rb')
    )