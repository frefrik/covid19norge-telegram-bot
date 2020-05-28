import pandas as pd
import altair as alt
import requests
import json
import datetime
from vg import VG

vg = VG()

def tested():
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

    chart.save('./graphs/no_tested.png')

    return(
        open('./graphs/no_tested.png', 'rb')
    )

def confirmed():
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

    chart.save('./graphs/no_confirmed.png')

    return(
        open('./graphs/no_confirmed.png', 'rb')
    )

def dead():
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

    chart.save('./graphs/no_dead.png')

    return(
        open('./graphs/no_dead.png', 'rb')
    )

def hospitalized():
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

    chart.save('./graphs/no_hospitalized.png')

    return(
        open('./graphs/no_hospitalized.png', 'rb')
    )


if __name__ == "__main__":
    dead()