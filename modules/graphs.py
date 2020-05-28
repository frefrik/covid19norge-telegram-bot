import pandas as pd
import altair as alt
import requests
import json
import datetime
import os
from vg import VG

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

    chart.save(filename)

    return(
        open(filename, 'rb')
    )

def confirmed():
    filename = './graphs/no_confirmed.png'
    if os.path.exists(filename):
        os.remove(filename)

    nordic_ts = vg.get_json('nordic_ts')
    timeseries = nordic_ts['countries']['no']
    df = pd.DataFrame(timeseries)
    
    base = alt.Chart(df).encode(
        alt.X('monthdate(date):O', axis=alt.Axis(title=None))
    )

    bar = base.mark_bar(color='steelblue', opacity=0.5).encode(
        y=alt.Y('newInfected:Q',
            axis=alt.Axis(title='Antall smittede per dag'))
    )

    line = base.mark_line(color='red').encode(
        y=alt.Y('cumulativeInfected:Q',
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

    nordic_ts = vg.get_json('nordic_ts')
    timeseries = nordic_ts['countries']['no']
    df = pd.DataFrame(timeseries)

    base = alt.Chart(df).encode(
        alt.X('monthdate(date):O', axis=alt.Axis(title=None))
    )

    bar = base.mark_bar(color='purple', opacity=0.3).encode(
        y=alt.Y('newDeaths:Q',
            axis=alt.Axis(title='Antall dødsfall per dag'))
    )

    line = base.mark_line(color='red').encode(
        y=alt.Y('cumulativeDeaths:Q',
            axis=alt.Axis(title='Antall dødsfall totalt'))
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

    chart.save(filename)

    return(
        open(filename, 'rb')
    )

def nordic_confirmed():
    filename = './graphs/nordic_confirmed.png'
    if os.path.exists(filename):
        os.remove(filename)

    nordic_ts = vg.get_json('nordic_ts')
    ts_se = nordic_ts['countries']['se']
    ts_dk = nordic_ts['countries']['dk']
    ts_no = nordic_ts['countries']['no']

    df_se = pd.DataFrame(ts_se)
    df_dk = pd.DataFrame(ts_dk)
    df_no = pd.DataFrame(ts_no).replace('Norway', 'Norge')

    frames = [df_se, df_dk, df_no]

    df = pd.concat(frames).reset_index(drop=True)
    df = df.rename(columns={'area': 'Land'})
    df['date'] = pd.to_datetime(df['date'])
    df = df[df.date >= '2020-03-01']

    df['newInfected_per100k'] = df['newInfected']/(df['population']/100000)
    df['cumulativeInfected_per100k'] = df['cumulativeInfected']/(df['population']/100000)

    chart = alt.Chart(df).mark_line().encode(
        x=alt.X('monthdate(date):O', title='Dato'),
        y=alt.Y('cumulativeInfected_per100k:Q', title='Antall smittede per 100k innbygger'),
        color='Land'
    ).properties(
        width=1000,
        height=600
    )

    chart.save(filename)

    return(
        open(filename, 'rb')
    )

if __name__ == "__main__":
    nordic_confirmed()