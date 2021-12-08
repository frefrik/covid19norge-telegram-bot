from datetime import datetime, date, timedelta
from telegram import ParseMode
from modules.utils import load_config, get_messagetext
from modules.utils import file_open_json, file_write_json
import modules.rss as rss
import modules.graphs as graphs
import modules.c19api as c19api

cfg = load_config()
bot = cfg["bot"]
jobs = bot["autopost"]["jobs"]


def stats(context):
    yesterday = (date.today() - timedelta(days=1)).strftime("%d.%m.%Y")

    # metadata
    population = 5391369
    tested = c19api.metadata("tested")
    confirmed = c19api.metadata("confirmed")
    dead = c19api.metadata("dead")
    admissions = c19api.metadata("admissions")
    respiratory = c19api.metadata("respiratory")
    vaccine_doses = c19api.timeseries("vaccine_doses")

    # totals
    tested_total = tested.get("total")
    confirmed_total = confirmed.get("total")
    dead_total = dead.get("total")
    admissions_total = admissions.get("total")
    respiratory_total = respiratory.get("total")

    # newYesterday
    tested_newYesterday = tested.get("newYesterday", 0)
    confirmed_newYesterday = confirmed.get("newYesterday", 0)
    dead_newYesterday = dead.get("newYesterday", 0)

    # newSince
    confirmed_newSince_d7 = confirmed.get("newSince_d8", 0)
    confirmed_newSince_d14 = confirmed.get("newSince_d15", 0)

    # percentages
    dead_pct = round(dead_total / confirmed_total * 100, 1)
    respiratory_pct = round(respiratory_total / admissions_total * 100, 1)

    # vaccine data
    vaccine_data = list(
        filter(lambda x: x["granularity_geo"] == "nation", vaccine_doses)
    )[-1]
    vacc_total_dose_1 = vaccine_data.get("total_dose_1")
    vacc_total_dose_2 = vaccine_data.get("total_dose_2")
    vacc_total_dose_3 = vaccine_data.get("total_dose_3")
    vacc_total_dose_1_pct = vacc_total_dose_1 / population
    vacc_total_dose_2_pct = vacc_total_dose_2 / population
    vacc_total_dose_3_pct = vacc_total_dose_3 / population

    ret_str = f"🔢 <b>Nøkkeltall - {yesterday}</b>"

    ret_str += f"\n\n🦠 Smittetilfeller siste døgn: <b>{confirmed_newYesterday:,}</b>"
    ret_str += f"\nSiste 7d: <b>{confirmed_newSince_d7:,}</b>"
    ret_str += f"\nSiste 14d: <b>{confirmed_newSince_d14:,}</b>"
    ret_str += f"\nTotalt: <b>{confirmed_total:,}</b>"

    ret_str += f"\n\n❗ Dødsfall siste døgn: <b>{dead_newYesterday:,}</b>"
    ret_str += f"\nTotalt: <b>{dead_total:,}</b> ({dead_pct}% av smittede)"

    ret_str += f"\n\n🔬 Testede siste døgn: <b>{tested_newYesterday:,}</b>"
    ret_str += f"\nTotalt: <b>{tested_total:,}</b>"

    ret_str += f"\n\n🏥 Innlagt på sykehus: <b>{admissions_total:,}</b>"
    ret_str += f"\n😷 Tilkoblet respirator: <b>{respiratory_total:,}</b> ({respiratory_pct}% av innlagte)"

    ret_str += "\n\n💉 Andel av befolkningen vaksinert"
    ret_str += f"\nDose 1: <b>{vacc_total_dose_1_pct:,.02%}</b> (<b>{vacc_total_dose_1:,}</b> personer)"
    ret_str += f"\nDose 2: <b>{vacc_total_dose_2_pct:,.02%}</b> (<b>{vacc_total_dose_2:,}</b> personer)"
    ret_str += f"\nDose 3: <b>{vacc_total_dose_3_pct:,.02%}</b> (<b>{vacc_total_dose_3:,}</b> personer)"

    ret_str = ret_str.replace(",", " ")

    context.bot.send_message(
        chat_id=bot["autopost"]["chatid"], text=ret_str, parse_mode=ParseMode.HTML
    )


def tested(context):
    source_name = jobs["tested"]["source"]["name"]
    source_url = jobs["tested"]["source"]["url"]

    curr_data = c19api.timeseries("tested")[-1]
    curr_total = curr_data.get("total")

    last_data = file_open_json("tested")
    last_total = last_data.get("total")

    diff_tested = curr_total - last_total

    if diff_tested > 0:
        messagetext = get_messagetext("tested", diff_tested)
        curr_new_today = curr_data.get("new")

        ret_str = f"🔬 <b>{diff_tested:,}</b> {messagetext}"
        ret_str += (
            f"\nTotalt: <b>{last_total:,}</b> (Nye i dag: <b>{curr_new_today:,}</b>)"
        )
        ret_str += f"\n\nKilde: <a href='{source_url}'>{source_name}</a>"

        file_write_json("tested", curr_data)

        ret_str = ret_str.replace(",", " ")
        print(ret_str, "\n")

        context.bot.send_message(
            chat_id=bot["autopost"]["chatid"], text=ret_str, parse_mode=ParseMode.HTML
        )
    else:
        return None


def tested_lab(context):
    source_name = jobs["tested_lab"]["source"]["name"]
    source_url = jobs["tested_lab"]["source"]["url"]

    curr_data = c19api.timeseries("tested_lab")[-1]
    curr_total = curr_data.get("total")

    last_data = file_open_json("tested_lab")
    last_total = last_data.get("total")

    if curr_total - last_total > 0:
        ret_str = "🔬 <b>Antall testet (Laboratoriedata)</b>"
        ret_str += "\nAntall personer testet og andelen positive blant disse i Norge siden epidemiens start."
        ret_str += "\nEn ny test på en person defineres som en test utført minst 7 dager etter forrige test av samme person."
        ret_str += f"\n\nKilde: <a href='{source_url}'>{source_name}</a>"

        file_write_json("tested_lab", curr_data)

        print(ret_str, "\n")

        context.bot.send_photo(
            bot["autopost"]["chatid"],
            graphs.tested(),
            parse_mode=ParseMode.HTML,
            caption=ret_str,
        )
    else:
        return None


def confirmed(context):
    source_name = jobs["confirmed"]["source"]["name"]
    source_url = jobs["confirmed"]["source"]["url"]

    curr_data = c19api.timeseries("confirmed")[-1]
    curr_total = curr_data.get("total")

    last_data = file_open_json("confirmed")
    last_total = last_data.get("total")

    diff_confirmed = curr_total - last_total

    if diff_confirmed > 0:
        messagetext = get_messagetext("confirmed", diff_confirmed)
        ret_str = f"🦠 <b>{diff_confirmed}</b> {messagetext}"

        if datetime.now().hour in range(0, 2):
            yesterday_data = c19api.timeseries("confirmed")[-2]
            yesterday_new = yesterday_data.get("new")
            ret_str += f"\nTotalt: <b>{last_total:,}</b> (Nye siste døgn: <b>{yesterday_new:,}</b>)"
        else:
            newToday = curr_data.get("new")
            ret_str += (
                f"\nTotalt: <b>{curr_total:,}</b> (Nye i dag: <b>{newToday:,}</b>)"
            )

        ret_str += f"\n\nKilde: <a href='{source_url}'>{source_name}</a>"

        file_write_json("confirmed", curr_data)

        ret_str = ret_str.replace(",", " ")
        print(ret_str, "\n")

        context.bot.send_message(
            chat_id=bot["autopost"]["chatid"], text=ret_str, parse_mode=ParseMode.HTML
        )
    else:
        return None


def confirmed_by_testdate(context):
    source_name = jobs["confirmed_by_testdate"]["source"]["name"]
    source_url = jobs["confirmed_by_testdate"]["source"]["url"]
    data = c19api.timeseries("confirmed")

    curr_data = list(filter(lambda x: x["source"] == "fhi:git", data))[-1]
    curr_total = curr_data.get("total")

    last_data = file_open_json("confirmed_by_testdate")
    last_total = last_data.get("total")

    if curr_total - last_total > 0:
        ret_str = "🦠 <b>Antall meldte smittetilfeller</b>"

        ret_str += "\nAntall meldte COVID-19 tilfeller etter prøvetakingsdato."
        ret_str += "\nDet er 1-2 dagers forsinkelse i tiden fra diagnose til registrering i MSIS."
        ret_str += f"\n\nKilde: <a href='{source_url}'>{source_name}</a>"

        file_write_json("confirmed_by_testdate", curr_data)

        print(ret_str, "\n")

        context.bot.send_photo(
            bot["autopost"]["chatid"],
            graphs.confirmed(),
            parse_mode=ParseMode.HTML,
            caption=ret_str,
        )
    else:
        return None


def dead(context):
    source_name = jobs["dead"]["source"]["name"]
    source_url = jobs["dead"]["source"]["url"]

    curr_data = c19api.timeseries("dead")[-1]
    curr_total = curr_data.get("total")

    last_data = file_open_json("dead")
    last_total = last_data.get("total")

    diff_dead = curr_total - last_total

    if diff_dead > 0:
        messagetext = get_messagetext("dead", diff_dead)
        curr_new_today = curr_data.get("new")

        ret_str = "❗ <b>COVID-19 assosierte dødsfall</b>"
        ret_str += f"\n<b>{diff_dead}</b> {messagetext}"

        ret_str += (
            f"\nTotalt: <b>{curr_total:,}</b> (Nye i dag: <b>{curr_new_today:,}</b>)"
        )
        ret_str += f"\n\nKilde: <a href='{source_url}'>{source_name}</a>"

        file_write_json("dead", curr_data)

        ret_str = ret_str.replace(",", " ")
        print(ret_str, "\n")

        context.bot.send_photo(
            bot["autopost"]["chatid"],
            graphs.dead(),
            parse_mode=ParseMode.HTML,
            caption=ret_str,
        )
    else:
        return None


def hospitalized(context):
    source_name = jobs["hospitalized"]["source"]["name"]
    source_url = jobs["hospitalized"]["source"]["url"]

    curr_data = c19api.timeseries("hospitalized")[-1]
    curr_respiratory = int(curr_data.get("respiratory"))
    curr_admissions = int(curr_data.get("admissions"))

    last_data = file_open_json("hospitalized")
    last_respiratory = int(last_data.get("respiratory"))
    last_admissions = int(last_data.get("admissions"))

    if curr_admissions != last_admissions or curr_respiratory != last_respiratory:
        diff_admissions = curr_admissions - last_admissions
        diff_respiratory = curr_respiratory - last_respiratory
        respiratory_pct = curr_respiratory / curr_admissions

        ret_str = "🏥 <b>Innlagte pasienter på sykehus</b>"

        if diff_admissions != 0:
            ret_str += f"\nEndring i antall innlagte: <b>{diff_admissions:+,}</b>"

        if diff_respiratory != 0:
            ret_str += f"\nEndring i antall på respirator: <b>{diff_respiratory:+,}</b>"

        ret_str += f"\n\n<b>{curr_admissions:,}</b> personer er innlagt på sykehus"
        ret_str += f"\n<b>{curr_respiratory:,}</b> personer er på respirator ({respiratory_pct:.01%})"

        ret_str += f"\n\nKilde: <a href='{source_url}'>{source_name}</a>"

        ret_str = ret_str.replace(",", " ")

        print(ret_str, "\n")
        file_write_json("hospitalized", curr_data)

        context.bot.send_photo(
            bot["autopost"]["chatid"],
            graphs.hospitalized(),
            parse_mode=ParseMode.HTML,
            caption=ret_str,
        )

    else:
        return None


def vaccine(context):
    population = 5391369
    source_name = jobs["vaccine"]["source"]["name"]
    source_url = jobs["vaccine"]["source"]["url"]
    data = c19api.timeseries("vaccine_doses")

    curr_data = list(filter(lambda x: x["granularity_geo"] == "nation", data))[-1]
    curr_total_doses = curr_data.get("total_doses")

    last_data = file_open_json("vaccine_doses")
    last_total_doses = last_data.get("total_doses")

    diff_total_doses = curr_total_doses - last_total_doses

    if diff_total_doses > 0:
        curr_total_dose_1 = curr_data.get("total_dose_1")
        curr_total_dose_2 = curr_data.get("total_dose_2")
        curr_total_dose_3 = curr_data.get("total_dose_3")
        curr_total_dose_1_pct = curr_total_dose_1 / population
        curr_total_dose_2_pct = curr_total_dose_2 / population
        curr_total_dose_3_pct = curr_total_dose_3 / population

        last_total_dose_1 = last_data.get("total_dose_1")
        last_total_dose_2 = last_data.get("total_dose_2")
        last_total_dose_3 = last_data.get("total_dose_3")

        diff_total_dose_1 = curr_total_dose_1 - last_total_dose_1
        diff_total_dose_2 = curr_total_dose_2 - last_total_dose_2
        diff_total_dose_3 = curr_total_dose_3 - last_total_dose_3

        ret_str = "💉 <b>Antall vaksinerte</b>"

        if diff_total_dose_1 != 0:
            ret_str += (
                f"\n<b>{diff_total_dose_1:,}</b> nye personer vaksinert med 1. dose"
            )

        if diff_total_dose_2 != 0:
            ret_str += f"\n<b>{diff_total_dose_2:,}</b> nye personer fullvaksinert"

        if diff_total_dose_3 != 0:
            ret_str += (
                f"\n<b>{diff_total_dose_3:,}</b> nye personer vaksinert med 3. dose"
            )

        ret_str += "\n\n<b>Total andel av befolkningen</b>"
        ret_str += f"\nDose 1: <b>{curr_total_dose_1_pct:,.02%}</b> ({curr_total_dose_1:,} personer)"
        ret_str += f"\nDose 2: <b>{curr_total_dose_2_pct:,.02%}</b> ({curr_total_dose_2:,} personer)"
        ret_str += f"\nDose 3: <b>{curr_total_dose_3_pct:,.02%}</b> ({curr_total_dose_3:,} personer)"
        ret_str += f"\n\nKilde: <a href='{source_url}'>{source_name}</a>"

        file_write_json("vaccine_doses", curr_data)

        ret_str = ret_str.replace(",", " ")
        print(ret_str, "\n")

        context.bot.send_photo(
            bot["autopost"]["chatid"],
            graphs.vaccine_doses(),
            parse_mode=ParseMode.HTML,
            caption=ret_str,
        )

    else:
        return None


def smittestopp(context):
    source_name = jobs["smittestopp"]["source"]["name"]
    source_url = jobs["smittestopp"]["source"]["url"]

    curr_data = c19api.timeseries("smittestopp")[-1]
    curr_total_downloads = int(curr_data.get("total_downloads"))
    curr_total_reported = int(curr_data.get("total_reported"))

    last_data = file_open_json("smittestopp")
    last_total_downloads = int(last_data.get("total_downloads"))
    last_total_reported = int(last_data.get("total_reported"))

    if (
        curr_total_downloads != last_total_downloads
        or curr_total_reported != last_total_reported
    ):
        new_downloads = int(curr_data.get("new_downloads"))
        new_reported = int(curr_data.get("new_reported"))

        if new_downloads == 1:
            new_downloads_text = "ny nedlasting av appen Smittestopp"
        else:
            new_downloads_text = "nye nedlastinger av appen Smittestopp"

        if new_reported == 1:
            new_reported_text = "ny person meldt smittet gjennom appen Smittestopp"
        else:
            new_reported_text = "nye personer meldt smittet gjennom appen Smittestopp"

        ret_str = "📱 <b>Smittestopp</b>"

        if new_downloads != 0:
            ret_str += f"\n<b>{new_downloads:,}</b> {new_downloads_text}"

        if new_reported != 0:
            ret_str += f"\n<b>{new_reported:,}</b> {new_reported_text}"

        ret_str += f"\n\nTotalt antall nedlastinger: <b>{curr_total_downloads:,}</b>"
        ret_str += f"\nTotalt <b>{curr_total_reported:,}</b> personer er meldt smittet gjennom appen"
        ret_str += f"\n\nKilde: <a href='{source_url}'>{source_name}</a>"

        file_write_json("smittestopp", curr_data)

        ret_str = ret_str.replace(",", " ")
        print(ret_str, "\n")

        context.bot.send_photo(
            bot["autopost"]["chatid"],
            graphs.smittestopp(),
            parse_mode=ParseMode.HTML,
            caption=ret_str,
        )

    else:
        return None


def rss_feed(context):
    res = rss.fetch_feed()

    if res is not None:
        context.bot.send_message(
            chat_id=bot["autopost"]["chatid"], text=res, parse_mode=ParseMode.HTML
        )
