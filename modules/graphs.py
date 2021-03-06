from datetime import date, timedelta
import pandas as pd
import altair as alt
from altair_saver import save
import os
import modules.c19api as c19api


def tested():
    filename = './graphs/no_tested.png'
    if os.path.exists(filename):
        os.remove(filename)

    data = c19api.timeseries('tested_lab')
    df = pd.DataFrame(data)

    mapping = {
        "new_neg": "Nye (Negative)",
        "new_pos": "Nye (Positive)",
        "new_total": "Nye",
        "pr100_pos": "Andel Positive",
        "total": "Akkumulert"
    }

    df = df.rename(columns=mapping)
    df['date'] = pd.to_datetime(df['date'])
    df["Andel Negative"] = 100 - df["Andel Positive"]
    df = df.melt(
        id_vars=['date', 'Andel Positive'],
        var_name='category',
        value_name='value')

    base = alt.Chart(
        df,
        title='Antall personer testet for covid-19 per dag og andel positive blant disse (Kilde: FHI)'
    ).encode(
        alt.X(
            'yearmonthdate(date):O',
            axis=alt.Axis(
                title=None,
                labelAngle=-40
            )
        )
    )

    andel = base.mark_line(
        color='red',
        opacity=0.8
    ).encode(
        y=alt.Y(
            'Andel Positive:Q',
            title='% Positive',
            axis=alt.Axis(grid=True)
        )
    )

    bar = base.transform_filter(
        (alt.datum.category == "Nye (Negative)") |
        (alt.datum.category == "Nye (Positive)")
    ).mark_bar().encode(
        y=alt.Y(
            'value:Q',
            title='Antall personer testet for covid-19 per dag'
        ),
        color=alt.Color(
            'category:N',
            scale=alt.Scale(
                    domain=['Nye (Positive)', 'Nye (Negative)', '% Positive'],
                    range=['#FF9622', '#6DA9FF', 'red']
            ),
            legend=alt.Legend(title=None)
        )
    )

    chart = alt.layer(
        bar,
        andel
    ).resolve_scale(
        y='independent'
    ).properties(
        width=1200,
        height=600
    ).configure_legend(
        strokeColor='gray',
        fillColor='#FFFFFF',
        labelFontSize=12,
        symbolStrokeWidth=2,
        symbolSize=160,
        padding=6,
        cornerRadius=5,
        direction='horizontal',
        orient='none',
        legendX=480,
        legendY=650
    )

    save(chart, filename)

    return open(filename, 'rb')


def confirmed():
    data = c19api.timeseries('confirmed')

    filename = './graphs/no_confirmed.png'
    if os.path.exists(filename):
        os.remove(filename)

    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    df = df.loc[df['source'] == 'fhi:git']
    df['new_sma7'] = df.new.rolling(window=7).mean().shift()

    df = df.melt(
        id_vars=['date'],
        value_vars=['new', 'new_sma7', 'total'],
        var_name='category',
        value_name='value'
    ).dropna()

    rename = {
        'new': 'Nye',
        'new_sma7': 'Snitt 7 d.',
        'total': 'Akkumulert'
    }

    df['category'] = df['category'].replace(rename)

    base = alt.Chart(
        df,
        title='Antall meldte COVID-19 tilfeller etter prøvetakingsdato (Kilde: FHI/MSIS)'
    ).encode(
        alt.X(
            'yearmonthdate(date):O',
            axis=alt.Axis(
                title=None,
                labelAngle=-40
            )
        )
    )

    bar = base.transform_filter(
        alt.datum.category == "Nye"
    ).mark_bar(
        color='#FFD1D1'
    ).encode(
        y=alt.Y(
            'value:Q',
            axis=alt.Axis(
                title='Nye per dag',
                grid=True
            )
        )
    )

    line = base.transform_filter(
        alt.datum.category == "Akkumulert"
    ).mark_line(
        color='#2E507B',
        strokeWidth=3
    ).encode(
        y=alt.Y(
            'value:Q',
            axis=alt.Axis(title='Akkumulert')
        ),
        color=alt.Color(
            'category:N',
            scale=alt.Scale(
                    domain=['Nye', 'Snitt 7 d.', 'Akkumulert'],
                    range=['#FFD1D1', 'red', '#2E507B']
            ),
            legend=alt.Legend(title=None)
        )
    )

    ma7 = base.transform_filter(
        alt.datum.category == "Snitt 7 d."
    ).mark_line(
        opacity=0.8
    ).encode(
        y=alt.Y('value:Q'),
        color=alt.Color('category:N')
    )

    chart = alt.layer(
        bar + ma7,
        line
    ).resolve_scale(
        y='independent'
    ).properties(
        width=1200,
        height=600
    ).configure_legend(
        strokeColor='gray',
        fillColor='#FFFFFF',
        labelFontSize=12,
        symbolStrokeWidth=2,
        symbolSize=160,
        padding=6,
        cornerRadius=5,
        direction='horizontal',
        orient='none',
        legendX=480,
        legendY=650
    )

    save(chart, filename)

    return open(filename, 'rb')


def dead():
    data = c19api.timeseries('dead')

    yesterday = date.today() - timedelta(days=1)
    filename = './graphs/no_dead.png'
    if os.path.exists(filename):
        os.remove(filename)

    df = pd.DataFrame(data)

    idx = pd.date_range('2020-03-07', df['date'].max())
    df.index = pd.DatetimeIndex(df['date'])
    df = df.reindex(idx)
    df['date'] = df.index
    df = df.reset_index(drop=True)
    df = df[df.date <= str(yesterday)]

    df['new'] = df['new'].fillna(0).astype(int)
    df['total'] = df['total'].fillna(method='bfill').astype(int)

    df['new_sma7'] = df.new.rolling(window=7).mean()

    df = df.melt(
        id_vars=['date'],
        value_vars=['new', 'new_sma7', 'total'],
        var_name='category',
        value_name='value'
    ).dropna()

    rename = {
        'new': 'Nye',
        'new_sma7': 'Snitt 7 d.',
        'total': 'Akkumulert'
    }

    df['category'] = df['category'].replace(rename)

    base = alt.Chart(
        df,
        title='COVID-19 dødsfall (Kilde: FHI)'
    ).encode(
        alt.X(
            'yearmonthdate(date):O',
            axis=alt.Axis(
                title=None,
                labelAngle=-40
            )
        )
    )

    bar = base.transform_filter(
        alt.datum.category == "Nye"
    ).mark_bar(
        color='#FFD1D1'
    ).encode(
        y=alt.Y(
            'value:Q',
            axis=alt.Axis(
                title='Nye per dag',
                grid=True
            )
        )
    )

    line = base.transform_filter(
        alt.datum.category == "Akkumulert"
    ).mark_line(
        color='#2E507B',
        strokeWidth=3
    ).encode(
        y=alt.Y(
            'value:Q',
            axis=alt.Axis(title='Akkumulert')
        ),
        color=alt.Color(
            'category:N',
            scale=alt.Scale(
                    domain=['Nye', 'Snitt 7 d.', 'Akkumulert'],
                    range=['#FFD1D1', 'red', '#2E507B']
            ),
            legend=alt.Legend(title=None)
        )
    )

    ma7 = base.transform_filter(
        alt.datum.category == "Snitt 7 d."
    ).mark_line(
        opacity=0.8
    ).encode(
        y=alt.Y('value:Q'),
        color=alt.Color('category:N')
    )

    chart = alt.layer(
        bar + ma7,
        line
    ).resolve_scale(
        y='independent'
    ).properties(
        width=1200,
        height=600
    ).configure_legend(
        strokeColor='gray',
        fillColor='#FFFFFF',
        labelFontSize=12,
        symbolStrokeWidth=2,
        symbolSize=160,
        padding=6,
        cornerRadius=5,
        direction='horizontal',
        orient='none',
        legendX=480,
        legendY=650
    )

    save(chart, filename)

    return open(filename, 'rb')


def hospitalized():
    data = c19api.timeseries('hospitalized')
    yesterday = date.today() - timedelta(days=1)
    filename = './graphs/no_hospitalized.png'
    if os.path.exists(filename):
        os.remove(filename)

    df = pd.DataFrame(data)

    idx = pd.date_range('2020-03-08', yesterday)
    df.index = pd.DatetimeIndex(df['date'])
    df = df.reindex(idx)
    df['date'] = df.index
    df = df.reset_index(drop=True)

    df['admissions'] = df['admissions'].fillna(method='ffill').astype(int)
    df['respiratory'] = df['respiratory'].fillna(method='ffill').astype(int)

    df_melt = pd.melt(
        df,
        id_vars=['date'],
        value_vars=['admissions', 'respiratory'],
        value_name='value'
    ).replace({'admissions': 'Innlagt', 'respiratory': 'På respirator'})

    chart = alt.Chart(
        df_melt,
        title='Innlagt på sykehus (Kilde: Helsedirektoratet)'
    ).mark_area(
        line={},
        opacity=0.3
    ).encode(
        x=alt.X(
            'yearmonthdate(date):O',
            axis=alt.Axis(
                title=None,
                labelAngle=-40
            )
        ),
        y=alt.Y(
            'value:Q',
            stack=None,
            title='Antall innlagte med påvist COVID-19 i Norge'
        ),
        color=alt.Color(
            'variable:N',
            scale=alt.Scale(
                    domain=['Innlagt', 'På respirator'],
                    range=['#5A9DFF', '#FF8B1B']
            ),
            legend=alt.Legend(title=None)
        )
    ).properties(
        width=1200,
        height=600
    ).configure_legend(
        strokeColor='gray',
        fillColor='#FFFFFF',
        labelFontSize=12,
        symbolStrokeWidth=2,
        symbolSize=160,
        padding=6,
        cornerRadius=5,
        direction='horizontal',
        orient='none',
        legendX=480,
        legendY=650
    )

    save(chart, filename)

    return open(filename, 'rb')
