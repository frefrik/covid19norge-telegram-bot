from datetime import date
from telegram import ParseMode
from modules.utils import load_config
import modules.graphs as graphs
import modules.c19api as c19api

cfg = load_config()
settings = cfg["bot"]


def chatid(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=f"Chatid: {update.message.chat_id}",
        parse_mode=ParseMode.HTML,
    )


def help(update, context):
    menuitems = "<b>" + settings["commands"]["title"] + "</b>\n"

    for command in list(settings["commands"].items())[1:]:
        menuitems += command[1] + "\n"

    context.bot.send_message(
        chat_id=update.message.chat_id, text=menuitems, parse_mode=ParseMode.HTML
    )


def stats(update, context):
    today = date.today().strftime("%d.%m.%Y")

    # metadata
    population = 5391369
    tested = c19api.metadata("tested")
    confirmed = c19api.metadata("confirmed")
    dead = c19api.metadata("dead")
    admissions = c19api.metadata("admissions")
    icu = c19api.metadata("icu")
    respiratory = c19api.metadata("respiratory")
    vaccine_doses = c19api.timeseries("vaccine_doses")

    # totals
    tested_total = tested.get("total")
    confirmed_total = confirmed.get("total")
    dead_total = dead.get("total")
    admissions_total = admissions.get("total")
    icu_total = icu.get("total")
    respiratory_total = respiratory.get("total")

    # newToday
    tested_newToday = tested.get("newToday", 0)
    confirmed_newToday = confirmed.get("newToday", 0)
    dead_newToday = dead.get("newToday", 0)

    # newSince
    confirmed_newSince_d7 = confirmed.get("newSince_d7", 0)
    confirmed_newSince_d14 = confirmed.get("newSince_d14", 0)

    # percentages
    dead_pct = round(dead_total / confirmed_total * 100, 1)
    respiratory_pct = round(respiratory_total / admissions_total * 100, 1)
    icu_pct = round(icu_total / admissions_total * 100, 1)

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

    ret_str = f"🔢 <b>Nøkkeltall - {today}</b>"

    ret_str += f"\n\n🦠 Smittetilfeller i dag: <b>{confirmed_newToday:,}</b>"
    ret_str += f"\nSiste 7d: <b>{confirmed_newSince_d7:,}</b>"
    ret_str += f"\nSiste 14d: <b>{confirmed_newSince_d14:,}</b>"
    ret_str += f"\nTotalt: <b>{confirmed_total:,}</b>"

    ret_str += f"\n\n❗ Dødsfall i dag: <b>{dead_newToday:,}</b>"
    ret_str += f"\nTotalt: <b>{dead_total:,}</b> ({dead_pct}% av smittede)"

    ret_str += f"\n\n🔬 Testede i dag: <b>{tested_newToday:,}</b>"
    ret_str += f"\nTotalt: <b>{tested_total:,}</b>"

    # https://www.helsedirektoratet.no/statistikk/antall-innlagte-pasienter-pa-sykehus-med-pavist-covid-19
    # Fra 23. mars 2022 ble rapporteringen avsluttet og visningen blir derfor ikke lenger oppdatert etter denne datoen.
    #
    # ret_str += f"\n\n🏥 Innlagt på sykehus: <b>{admissions_total:,}</b>"
    # ret_str += f"\n🤒 Innlagt på intensivavdeling: <b>{icu_total:,}</b> ({icu_pct}% av innlagte)"
    # ret_str += f"\n😷 Tilkoblet respirator: <b>{respiratory_total:,}</b> ({respiratory_pct}% av innlagte)"

    ret_str += "\n\n💉 Andel av befolkningen vaksinert"
    ret_str += f"\nDose 1: <b>{vacc_total_dose_1_pct:,.02%}</b> ({vacc_total_dose_1:,} personer)"
    ret_str += f"\nDose 2: <b>{vacc_total_dose_2_pct:,.02%}</b> ({vacc_total_dose_2:,} personer)"
    ret_str += f"\nDose 3: <b>{vacc_total_dose_3_pct:,.02%}</b> ({vacc_total_dose_3:,} personer)"

    ret_str = ret_str.replace(",", " ")

    context.bot.send_message(
        chat_id=update.message.chat_id, text=ret_str, parse_mode=ParseMode.HTML
    )


def tested_graph(update, context):
    context.bot.send_photo(chat_id=update.message.chat_id, photo=graphs.tested())


def confirmed_graph(update, context):
    context.bot.send_photo(chat_id=update.message.chat_id, photo=graphs.confirmed())


def dead_graph(update, context):
    context.bot.send_photo(chat_id=update.message.chat_id, photo=graphs.dead())


def hospitalized_graph(update, context):
    context.bot.send_photo(chat_id=update.message.chat_id, photo=graphs.hospitalized())


def vaccine_doses_graph(update, context):
    context.bot.send_photo(chat_id=update.message.chat_id, photo=graphs.vaccine_doses())


def smittestopp_graph(update, context):
    try:
        if context.args[0] == "downloads":
            graph = graphs.smittestopp_downloads()
        if context.args[0] == "reported":
            graph = graphs.smittestopp_reported()
    except IndexError:
        graph = graphs.smittestopp()

    if graph:
        context.bot.send_photo(chat_id=update.message.chat_id, photo=graph)
    else:
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text="Usage: /smittestopp &lt;downloads/reported&gt;",
            parse_mode=ParseMode.HTML,
        )
