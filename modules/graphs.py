import os
from datetime import date
from altair_saver import save
import altair as alt
import pandas as pd
import modules.c19api as c19api


def tested():
    filename = "./graphs/no_tested.png"
    if os.path.exists(filename):
        os.remove(filename)

    data = c19api.timeseries("tested_lab")
    df = pd.DataFrame(data)

    mapping = {
        "new_neg": "Nye (Negative)",
        "new_pos": "Nye (Positive)",
        "new_total": "Nye",
        "pr100_pos": "Andel Positive",
        "total": "Akkumulert",
    }

    df = df.rename(columns=mapping)
    df["date"] = pd.to_datetime(df["date"])
    df["Andel Negative"] = 100 - df["Andel Positive"]
    df = df.melt(
        id_vars=["date", "Andel Positive"], var_name="category", value_name="value"
    )

    base = alt.Chart(
        df,
        title="Antall personer testet for covid-19 per dag og andel positive blant disse (Kilde: FHI)",
    ).encode(alt.X("yearmonthdate(date):O", axis=alt.Axis(title=None, labelAngle=-40)))

    andel = base.mark_line(color="red", opacity=0.8).encode(
        y=alt.Y("Andel Positive:Q", title="% Positive", axis=alt.Axis(grid=True))
    )

    bar = (
        base.transform_filter(
            (alt.datum.category == "Nye (Negative)")
            | (alt.datum.category == "Nye (Positive)")
        )
        .mark_bar()
        .encode(
            y=alt.Y("value:Q", title="Antall personer testet for covid-19 per dag"),
            color=alt.Color(
                "category:N",
                scale=alt.Scale(
                    domain=["Nye (Positive)", "Nye (Negative)", "% Positive"],
                    range=["#FF9622", "#6DA9FF", "red"],
                ),
                legend=alt.Legend(title=None),
            ),
        )
    )

    chart = (
        alt.layer(bar, andel)
        .resolve_scale(y="independent")
        .properties(width=1200, height=600)
        .configure_legend(
            strokeColor="gray",
            fillColor="#FFFFFF",
            labelFontSize=12,
            symbolStrokeWidth=2,
            symbolSize=160,
            padding=6,
            cornerRadius=5,
            direction="horizontal",
            orient="none",
            legendX=480,
            legendY=650,
        )
    )

    save(chart, filename)

    return open(filename, "rb")


def confirmed():
    data = c19api.timeseries("confirmed")

    filename = "./graphs/no_confirmed.png"
    if os.path.exists(filename):
        os.remove(filename)

    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"])
    df = df.loc[df["source"] == "fhi:git"]
    df["new_sma7"] = df.new.rolling(window=7).mean().shift()

    df = df.melt(
        id_vars=["date"],
        value_vars=["new", "new_sma7", "total"],
        var_name="category",
        value_name="value",
    ).dropna()

    rename = {"new": "Nye", "new_sma7": "Snitt 7 d.", "total": "Akkumulert"}

    df["category"] = df["category"].replace(rename)

    base = alt.Chart(
        df,
        title="Antall meldte COVID-19 tilfeller etter prøvetakingsdato (Kilde: FHI/MSIS)",
    ).encode(alt.X("yearmonthdate(date):O", axis=alt.Axis(title=None, labelAngle=-40)))

    bar = (
        base.transform_filter(alt.datum.category == "Nye")
        .mark_bar(color="#FFD1D1")
        .encode(y=alt.Y("value:Q", axis=alt.Axis(title="Nye per dag", grid=True)))
    )

    line = (
        base.transform_filter(alt.datum.category == "Akkumulert")
        .mark_line(color="#2E507B", strokeWidth=3)
        .encode(
            y=alt.Y("value:Q", axis=alt.Axis(title="Akkumulert")),
            color=alt.Color(
                "category:N",
                scale=alt.Scale(
                    domain=["Nye", "Snitt 7 d.", "Akkumulert"],
                    range=["#FFD1D1", "red", "#2E507B"],
                ),
                legend=alt.Legend(title=None),
            ),
        )
    )

    ma7 = (
        base.transform_filter(alt.datum.category == "Snitt 7 d.")
        .mark_line(opacity=0.8)
        .encode(y=alt.Y("value:Q"), color=alt.Color("category:N"))
    )

    chart = (
        alt.layer(bar + ma7, line)
        .resolve_scale(y="independent")
        .properties(width=1200, height=600)
        .configure_legend(
            strokeColor="gray",
            fillColor="#FFFFFF",
            labelFontSize=12,
            symbolStrokeWidth=2,
            symbolSize=160,
            padding=6,
            cornerRadius=5,
            direction="horizontal",
            orient="none",
            legendX=480,
            legendY=650,
        )
    )

    save(chart, filename)

    return open(filename, "rb")


def dead():
    data = c19api.timeseries("dead")

    today = date.today()
    filename = "./graphs/no_dead.png"
    if os.path.exists(filename):
        os.remove(filename)

    df = pd.DataFrame(data)

    idx = pd.date_range("2020-03-07", df["date"].max())
    df.index = pd.DatetimeIndex(df["date"])
    df = df.reindex(idx)
    df["date"] = df.index
    df = df.reset_index(drop=True)
    df = df[df.date <= str(today)]

    df["new"] = df["new"].fillna(0).astype(int)
    df["total"] = df["total"].fillna(method="bfill").astype(int)
    df["new_sma7"] = df.new.rolling(window=7).mean()

    df = df.melt(
        id_vars=["date"],
        value_vars=["new", "new_sma7", "total"],
        var_name="category",
        value_name="value",
    ).dropna()

    rename = {"new": "Nye", "new_sma7": "Snitt 7 d.", "total": "Akkumulert"}
    df["category"] = df["category"].replace(rename)

    base = alt.Chart(df, title="COVID-19 dødsfall (Kilde: FHI)").encode(
        alt.X("yearmonthdate(date):O", axis=alt.Axis(title=None, labelAngle=-40))
    )

    bar = (
        base.transform_filter(alt.datum.category == "Nye")
        .mark_bar(color="#FFD1D1")
        .encode(y=alt.Y("value:Q", axis=alt.Axis(title="Nye per dag", grid=True)))
    )

    line = (
        base.transform_filter(alt.datum.category == "Akkumulert")
        .mark_line(color="#2E507B", strokeWidth=3)
        .encode(
            y=alt.Y("value:Q", axis=alt.Axis(title="Akkumulert")),
            color=alt.Color(
                "category:N",
                scale=alt.Scale(
                    domain=["Nye", "Snitt 7 d.", "Akkumulert"],
                    range=["#FFD1D1", "red", "#2E507B"],
                ),
                legend=alt.Legend(title=None),
            ),
        )
    )

    ma7 = (
        base.transform_filter(alt.datum.category == "Snitt 7 d.")
        .mark_line(opacity=0.8)
        .encode(y=alt.Y("value:Q"), color=alt.Color("category:N"))
    )

    chart = (
        alt.layer(bar + ma7, line)
        .resolve_scale(y="independent")
        .properties(width=1200, height=600)
        .configure_legend(
            strokeColor="gray",
            fillColor="#FFFFFF",
            labelFontSize=12,
            symbolStrokeWidth=2,
            symbolSize=160,
            padding=6,
            cornerRadius=5,
            direction="horizontal",
            orient="none",
            legendX=480,
            legendY=650,
        )
    )

    save(chart, filename)

    return open(filename, "rb")


def hospitalized():
    data = c19api.timeseries("hospitalized")
    today = date.today()
    filename = "./graphs/no_hospitalized.png"
    if os.path.exists(filename):
        os.remove(filename)

    df = pd.DataFrame(data)

    idx = pd.date_range("2020-03-08", today)
    df.index = pd.DatetimeIndex(df["date"])
    df = df.reindex(idx)
    df["date"] = df.index
    df = df.reset_index(drop=True)

    df["admissions"] = df["admissions"].fillna(method="ffill").astype(int)
    df["respiratory"] = df["respiratory"].fillna(method="ffill").astype(int)

    df_melt = pd.melt(
        df,
        id_vars=["date"],
        value_vars=["admissions", "respiratory"],
        value_name="value",
    ).replace({"admissions": "Innlagt", "respiratory": "På respirator"})

    chart = (
        alt.Chart(df_melt, title="Innlagt på sykehus (Kilde: Helsedirektoratet)")
        .mark_area(line={}, opacity=0.3)
        .encode(
            x=alt.X("yearmonthdate(date):O", axis=alt.Axis(title=None, labelAngle=-40)),
            y=alt.Y(
                "value:Q",
                stack=None,
                title="Antall innlagte med påvist COVID-19 i Norge",
            ),
            color=alt.Color(
                "variable:N",
                scale=alt.Scale(
                    domain=["Innlagt", "På respirator"], range=["#5A9DFF", "#FF8B1B"]
                ),
                legend=alt.Legend(title=None),
            ),
        )
        .properties(width=1200, height=600)
        .configure_legend(
            strokeColor="gray",
            fillColor="#FFFFFF",
            labelFontSize=12,
            symbolStrokeWidth=2,
            symbolSize=160,
            padding=6,
            cornerRadius=5,
            direction="horizontal",
            orient="none",
            legendX=480,
            legendY=650,
        )
    )

    save(chart, filename)

    return open(filename, "rb")


def smittestopp_downloads():
    data = c19api.timeseries("smittestopp")

    filename = "./graphs/no_smittestopp.png"
    if os.path.exists(filename):
        os.remove(filename)

    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"])

    df = df.melt(
        id_vars=["date"],
        value_vars=["new_downloads", "total_downloads"],
        var_name="category",
        value_name="value",
    ).dropna()

    rename = {
        "new_downloads": "Nye",
        "total_downloads": "Akkumulert",
    }

    df["category"] = df["category"].replace(rename)

    base = alt.Chart(
        df, title="Antall nedlastinger av appen Smittestopp (Kilde: FHI)"
    ).encode(alt.X("yearmonthdate(date):O", axis=alt.Axis(title=None, labelAngle=-40)))

    bar = (
        base.transform_filter(alt.datum.category == "Nye")
        .mark_bar(color="#5BC1FF")
        .encode(y=alt.Y("value:Q", axis=alt.Axis(title="Nye per dag", grid=True)))
    )

    line = (
        base.transform_filter(alt.datum.category == "Akkumulert")
        .mark_line(color="#00008b", strokeWidth=3)
        .encode(
            y=alt.Y("value:Q", axis=alt.Axis(title="Akkumulert")),
            color=alt.Color(
                "category:N",
                scale=alt.Scale(
                    domain=["Nye", "Akkumulert"],
                    range=["#5BC1FF", "#00008b"],
                ),
                legend=alt.Legend(title=None),
            ),
        )
    )

    chart = (
        alt.layer(bar, line)
        .resolve_scale(y="independent")
        .properties(width=1200, height=600)
        .configure_legend(
            strokeColor="gray",
            fillColor="#FFFFFF",
            labelFontSize=12,
            symbolStrokeWidth=2,
            symbolSize=160,
            padding=6,
            cornerRadius=5,
            direction="horizontal",
            orient="none",
            legendX=480,
            legendY=650,
        )
    )

    save(chart, filename)

    return open(filename, "rb")


def smittestopp_reported():
    data = c19api.timeseries("smittestopp")

    filename = "./graphs/no_smittestopp.png"
    if os.path.exists(filename):
        os.remove(filename)

    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"])

    df = df.melt(
        id_vars=["date"],
        value_vars=["new_reported", "total_reported"],
        var_name="category",
        value_name="value",
    ).dropna()

    rename = {
        "new_reported": "Nye",
        "total_reported": "Akkumulert",
    }

    df["category"] = df["category"].replace(rename)

    base = alt.Chart(
        df, title="Antall meldt smittet gjennom appen Smittestopp (Kilde: FHI)"
    ).encode(alt.X("yearmonthdate(date):O", axis=alt.Axis(title=None, labelAngle=-40)))

    bar = (
        base.transform_filter(alt.datum.category == "Nye")
        .mark_bar(color="#FFA57E")
        .encode(y=alt.Y("value:Q", axis=alt.Axis(title="Nye per dag", grid=True)))
    )

    line = (
        base.transform_filter(alt.datum.category == "Akkumulert")
        .mark_line(color="#FF2B2B", strokeWidth=3)
        .encode(
            y=alt.Y("value:Q", axis=alt.Axis(title="Akkumulert")),
            color=alt.Color(
                "category:N",
                scale=alt.Scale(
                    domain=["Nye", "Akkumulert"],
                    range=["#FFA57E", "#FF2B2B"],
                ),
                legend=alt.Legend(title=None),
            ),
        )
    )

    chart = (
        alt.layer(bar, line)
        .resolve_scale(y="independent")
        .properties(width=1200, height=600)
        .configure_legend(
            strokeColor="gray",
            fillColor="#FFFFFF",
            labelFontSize=12,
            symbolStrokeWidth=2,
            symbolSize=160,
            padding=6,
            cornerRadius=5,
            direction="horizontal",
            orient="none",
            legendX=480,
            legendY=650,
        )
    )

    save(chart, filename)

    return open(filename, "rb")


def smittestopp():
    data = c19api.timeseries("smittestopp")

    filename = "./graphs/no_smittestopp.png"
    if os.path.exists(filename):
        os.remove(filename)

    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"])

    df = df.melt(
        id_vars=["date"],
        value_vars=["new_reported", "total_downloads"],
        var_name="category",
        value_name="value",
    ).dropna()

    rename = {
        "new_reported": "Antall meldt smittet i Smittestopp",
        "total_downloads": "Antall nedlastinger av Smittestopp",
    }

    df["category"] = df["category"].replace(rename)

    base = alt.Chart(
        df,
        title="Antall nedlastinger av Smittestopp og antall som har meldt gjennom appen at de er smittet (Kilde: FHI)",
    ).encode(alt.X("yearmonthdate(date):O", axis=alt.Axis(title=None, labelAngle=-40)))

    downloads = (
        base.transform_filter(
            alt.datum.category == "Antall nedlastinger av Smittestopp"
        )
        .mark_area(line={}, color="#5BC1FF", opacity=0.2)
        .encode(
            y=alt.Y(
                "value:Q",
                axis=alt.Axis(title="Antall nedlastinger av Smittestopp", grid=True),
            )
        )
    )

    reported = (
        base.transform_filter(
            alt.datum.category == "Antall meldt smittet i Smittestopp"
        )
        .mark_bar(color="#FFA57E")
        .encode(
            y=alt.Y(
                "value:Q", axis=alt.Axis(title="Antall meldt smittet i Smittestopp")
            ),
            color=alt.Color(
                "category:N",
                scale=alt.Scale(
                    domain=[
                        "Antall nedlastinger av Smittestopp",
                        "Antall meldt smittet i Smittestopp",
                    ],
                    range=["#5BC1FF", "#FFA57E"],
                ),
                legend=alt.Legend(title=None),
            ),
        )
    )

    chart = (
        alt.layer(reported, downloads)
        .resolve_scale(y="independent")
        .properties(width=1200, height=600)
        .configure_legend(
            strokeColor="gray",
            fillColor="#FFFFFF",
            labelFontSize=12,
            symbolStrokeWidth=2,
            symbolSize=160,
            labelLimit=200,
            padding=6,
            cornerRadius=5,
            direction="horizontal",
            orient="none",
            legendX=390,
            legendY=660,
        )
    )

    save(chart, filename)

    return open(filename, "rb")


def vaccine_doses():
    data = c19api.timeseries("vaccine_doses")

    filename = "./graphs/no_vaccine_doses.png"
    if os.path.exists(filename):
        os.remove(filename)

    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"])
    df = df[df["granularity_geo"] == "nation"]
    df["new_sma7"] = df.new_doses.rolling(window=7).mean().shift()

    df = df.melt(
        id_vars=["date"],
        value_vars=["total_dose_1", "total_dose_2"],
        var_name="category",
        value_name="value",
    ).dropna()

    rename = {
        "total_dose_1": "Har fått minst én dose",
        "total_dose_2": "Fullvaksinert",
    }

    df["category"] = df["category"].replace(rename)

    chart = (
        alt.Chart(
            df,
            title="Antall personer vaksinert med 1. og 2. dose av vaksine mot COVID-19 i Norge (Kilde: FHI)",
        )
        .mark_area(line={}, opacity=0.3)
        .encode(
            x=alt.X("yearmonthdate(date):O", axis=alt.Axis(title=None, labelAngle=-40)),
            y=alt.Y(
                "value:Q",
                stack=None,
                title="Antall",
            ),
            color=alt.Color(
                "category:N",
                scale=alt.Scale(
                    domain=["Har fått minst én dose", "Fullvaksinert"],
                    range=["#5dade2", " #2ecc71"],
                ),
                legend=alt.Legend(title=None),
            ),
        )
        .properties(width=1200, height=600)
        .configure_legend(
            strokeColor="gray",
            fillColor="#FFFFFF",
            labelFontSize=12,
            symbolStrokeWidth=2,
            symbolSize=160,
            padding=6,
            cornerRadius=5,
            direction="horizontal",
            orient="none",
            legendX=480,
            legendY=660,
        )
    )

    save(chart, filename)

    return open(filename, "rb")
