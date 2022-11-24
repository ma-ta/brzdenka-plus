# externí knihovny, třídy atd.
from browser import window, document, alert, console
from javascript import Date
sw_alert = window.Swal.fire

# globální konstanty
NAZEV_APLIKACE = "Brzděnka+"
VERZE = "verze 0.1.0 | 2022-11"
JMENO_AUTORA = "Martin TÁBOR"

AKTUALNI_ROK = Date.new().getFullYear()
AUTOR = f"\u00A9 2020\u2013{str(AKTUALNI_ROK)[2:]}&nbsp;&nbsp;{JMENO_AUTORA}"
UPOZORNENI = "!!! Všechny informace jsou bez záruky !!!".upper()
OBRAZEK_ZOB = "./obrazky/zob-txtgrafika-cerna.png"

BARVA_NORMAL = "#faf200"  # žlutá
BARVA_NORMAL_SWA_IKONA = "#f2f274"  # světle žlutá
BARVA_POZOR = "#db4437"  # červená
BARVA_OK = "#81c995"  # zelená
BARVA_MODRA = "8ab4f8"  # modrá
# tmavé téma
BARVA_PISMA = "#e8eaed"  # téměř bílá
BARVA_POZADI = "#202124"  # téměř černá

# deklarace globálních proměnných
tabulka_rychlosti = False
potrebna_procenta = 0
skutecna_procenta = 0
chybi_procent = 0
max_rychlost = 0

# přístup k objektům DOM
titulek = document["titulek"]
podnadpis = document["podnadpis"]
radio_tabulka_ano = document["radio_tabulka_ano"]
radio_tabulka_ne = document["radio_tabulka_ne"]
div_formular_skryt = document["skryt"]
input_potrebna = document["input_potrebna_procenta"]
input_skutecna = document["input_skutecna_procenta"]
label_chybejici = document["label_chybejici_procenta"]
input_chybejici = document["input_chybejici_procenta"]
input_max_rychlost = document["input_max_rychlost"]
button_vypocitat = document["button_vypocitat"]
button_reset = document["button_reset"]


def zobraz_zpravu(zprava, footer=True):
    if footer:
        zprava["footer"] = f"<div style='text-align: center;'><span style='font-weight: bold;'>{UPOZORNENI}</span><br>{AUTOR}</div>"

    sw_alert(zprava)


def chybne_vyplneni(ev, title, text):
    zobraz_zpravu(
        {
            "title": "- - -\n" + title,
            "text": text,
            "icon": "question",
            "confirmButtonText": "Heuréka",
            "confirmButtonColor": BARVA_MODRA,
            "imageUrl": OBRAZEK_ZOB,
            "imageAlt": "Zpráva o brzdění z POP",
            "imageHeight": 160
        },
        footer=False
    )


def zpracuj_vysledek(vysledek):

    # přiřazení hodnot z argumentu fce
    stav_prc = vysledek["stav_prc"]  # (+/-) x %
    vmax_nova  = vysledek["vmax_nova"]
    vmax_vystraha = vysledek["vmax_vystraha"]
    rozklad = vysledek["rozklad"]  # False = nelze rozložit
    prc_45_a_mensi = vysledek["prc_45_a_mensi"]


    # seznam zpráv:
    zpr_dostatek = {
        "zpr": "Rychlost není třeba přepočítávat.",
        "dostatek": "(Máte dostatek brzdících procent.)",
        "navic_jen": f"(Máte ale pouze {stav_prc}&nbsp;% navíc!)",
        "zadna_navic": "(Nemáte však žádná brzdící % navíc!)"
    }
    zpr_nedostatek = {
        "zpr": f"Maximální rychlost vlaku je <strong>{vmax_nova}&nbsp;km/h</strong>!",
        "u_vystrahy": f"V úrovni návěsti <strong>Výstraha</strong> však max. <strong>{vmax_vystraha}&nbsp;km/h</strong>!",
        "rozklad_nelze": "(Nelze použít rozklad.)",
        "nepojede": "Vlak nemůže odjet!<br><em>(Vypočítaná rychlost je 0&nbsp;km/h&nbsp;\u2026)</em>",
        "oznam": "Nezapomeňte informovat dispečera osobní dopravy!"
    }
    zpr_opatrne = "<em>Začněte brzdit v dostatečné vzdálenosti před Výstrahou!</em>"
    zpr_prc_45_a_mensi = "(Skutečná brzdící % jsou 45 či méně.)"


    swa_zpr_dostatek = {
        "title": "Bez omezení\u2026",
        "html": zpr_dostatek['zpr'],
        "icon": "success",
        "confirmButtonText": "OK",
        "confirmButtonColor": BARVA_OK
    }
    swa_zpr_nedostatek = {
        "title": "Zpomal!",

        "html": zpr_nedostatek['zpr'] +
                "{uvystrahy_ci_rozklad}<br><br>" +
                zpr_opatrne + "<br><br>" +
                zpr_nedostatek['oznam'],

        "icon": "warning",
        "iconColor": BARVA_NORMAL_SWA_IKONA,
        "confirmButtonText": "Budiž",
        "confirmButtonColor": BARVA_NORMAL
    }


    # VYHODNOCENÍ:

    # a) Dostatek skutečných procent:
    KONSTANTA_OBEZRETNOSTI = 20  # hodnotí, zda přebývá více než 20 %
    zpr = swa_zpr_dostatek

    if stav_prc > KONSTANTA_OBEZRETNOSTI:  # DOSTATEK
        zpr["html"] += f"<br>{zpr_dostatek['dostatek']}"

    elif 0 < stav_prc <= KONSTANTA_OBEZRETNOSTI:  # JEN x % NAVÍC
        zpr["html"] += f"<br>{zpr_dostatek['navic_jen']}<br><br>{zpr_opatrne}"

    elif stav_prc == 0:  # ŽÁDNÁ % NAVÍC
        zpr["html"] += f"<br>{zpr_dostatek['zadna_navic']}<br><br>{zpr_opatrne}"

    # b) Nedostatek skutečných procent:
    elif vmax_nova <= 0:  # rychlost <= 0 km/h
        zpr = {
            "title": "Stůj!",

            "html": zpr_nedostatek["nepojede"],

            "icon": "error",
            "confirmButtonText": "Bohužel",
            "confirmButtonColor": BARVA_POZOR
        }

    else:
        zpr = swa_zpr_nedostatek
        if rozklad is None:  # pro rychlost < 120 km/h
            zpr["html"] = zpr["html"].format(
                uvystrahy_ci_rozklad=""
            )

        elif rozklad is True:  # u Výstrahy o 20 km/h méně
            zpr["html"] = zpr["html"].format(
                uvystrahy_ci_rozklad=f"<br>{zpr_nedostatek['u_vystrahy']}"
            )

        elif rozklad is False:  # nelze použít rozklad
            zpr["html"] = zpr["html"].format(
                uvystrahy_ci_rozklad=f"<br>{zpr_nedostatek['rozklad_nelze']}"
            )

    zobraz_zpravu(zpr)


def btn_vypocitat(ev):
    global potrebna_procenta
    global skutecna_procenta
    global chybi_procent
    global max_rychlost

    if input_potrebna.value.isnumeric() \
        and input_skutecna.value.isnumeric() \
            and input_max_rychlost.value.isnumeric():

        if potrebna_procenta > 0 \
            and skutecna_procenta > 0 \
                and max_rychlost > 0:

            # načtení vstupních hodnot
            potrebna_procenta = int(input_potrebna.value)
            skutecna_procenta = int(input_skutecna.value)

            chybi_procent = potrebna_procenta - skutecna_procenta
            if chybi_procent < 0: chybi_procent = 0

            max_rychlost = int(input_max_rychlost.value)

            # lokální pojmenování globálních proměnných
            potrebna_p = potrebna_procenta
            skutecna_p = skutecna_procenta
            vmax_puvodni = max_rychlost

            # zjištění dalších vstupních parametrů:
            # a) skutečná procenta <= 45 ?
            if skutecna_p <= 45:
                prc_45_a_mensi = True
            else:
                prc_45_a_mensi = False
            # b) původní max. rychlost >= 120 km/h ?
            if vmax_puvodni >= 120:
                rych_120_a_vetsi = True
            else:
                rych_120_a_vetsi = False


            # VÝPOČET:
            vysledek = {
                "stav_prc": None,  # (+/-) x %
                "vmax_nova": None,
                "vmax_vystraha": None,
                "rozklad": None,  # False = nelze rozložit
                "prc_45_a_mensi": False
            }

            # chybějící procenta ?
            chybi_p = potrebna_p - skutecna_p  # záporné číslo = přebývá
            vysledek["stav_prc"] = chybi_p * (-1)

            # a) Dostatek skutečných procent:
            if chybi_p <= 0:
                pass

            # b) Nedostatek skutečných procent (výpočet):
            else:  # chybi_p > 0

                if prc_45_a_mensi:
                    chybi_p *= 2
                    vysledek["prc_45_a_mensi"] = True

                vmax_nova = vmax_puvodni - chybi_p
                vysledek["vmax_nova"] = vmax_nova

                if rych_120_a_vetsi:
                    if (vmax_nova - 20) > 120:  # ROZKLAD ano
                        vmax_vystraha = vmax_nova - 20

                        vysledek["vmax_vystraha"] = vmax_vystraha
                        vysledek["rozklad"] = True

                    else:  # ROZKLAD ne
                        vmax_nova -= 20

                        vysledek["vmax_nova"] = vmax_nova
                        vysledek["rozklad"] = False


            zpracuj_vysledek(vysledek)


        else:
            # některé políčko formuláře obsahuje hodnotu <= 0
            chybne_vyplneni(ev,
            title="Překlep ?",
            text="Všechny údaje v(e) ZOB by měly být větší než nula\u2026")
    else:
        # některé políčko formuláře neobsahuje číslo
        chybne_vyplneni(ev,
            title="Jak na to ?",
            text="Jednoduše opište všechny vyznačené údaje ze ZOB do formuláře\u2026")


def input_zmena(ev):
    # alert(ev.srcElement.id)  # debug

    if input_potrebna.value.isnumeric() \
        and input_skutecna.value.isnumeric():

        global potrebna_procenta
        potrebna_procenta = int(input_potrebna.value)

        global skutecna_procenta
        skutecna_procenta = int(input_skutecna.value)

        global chybi_procent
        chybi_procent = potrebna_procenta - skutecna_procenta
        if chybi_procent < 0: chybi_procent = 0

        # změna DOM - mění hodnotu a vzhled zobrazení Chybí
        input_chybejici.value = str(chybi_procent)
        if chybi_procent <= 0:
            chybi_procent = 0
            input_chybejici.style.color = BARVA_NORMAL
            label_chybejici.style.color = BARVA_NORMAL
        else:
            input_chybejici.style.color = BARVA_POZOR
            label_chybejici.style.color = BARVA_POZOR
    else:
        # spustí se vždy, když nejsou vyplněna všechna políčka
        # => znemožňuje vyplnění formuláře
        pass

    if input_max_rychlost.value.isnumeric():
        global max_rychlost
        max_rychlost = int(input_max_rychlost.value)

    # změna DOM - skryje či zobrazí formulář - existuje tabulka ano/ne
    if radio_tabulka_ano.checked:
        div_formular_skryt.style.display = "none"
        zobraz_zpravu({
            "icon": "info",
            "title": "Existuje jiné opatření ?",
            "text": "Při určení maximální rychlosti tedy postupujte v souladu s ním!",
            "confirmButtonColor": BARVA_NORMAL,
            "iconColor": BARVA_NORMAL_SWA_IKONA
        })
    else:
        div_formular_skryt.style.display = "inherit"


# změna DOM - smaže formulář
def reset(ev):
    global tabulka_rychlosti
    tabulka_rychlosti = False
    radio_tabulka_ne.checked = True

    global potrebna_procenta
    potrebna_procenta = 0
    input_potrebna.value = ""

    global skutecna_procenta
    skutecna_procenta = 0
    input_skutecna.value = ""

    global chybi_procent
    chybi_procent = 0
    input_chybejici.value = "0"

    global max_rychlost
    max_rychlost = 0
    input_max_rychlost.value = ""

    label_chybejici.style.color = BARVA_NORMAL
    input_chybejici.style.color = BARVA_NORMAL


# změna DOM - zobrazení dle konstant
document.title = NAZEV_APLIKACE
titulek.textContent = NAZEV_APLIKACE
podnadpis.textContent = VERZE

# přiřazení funkcí k událostem
button_vypocitat.bind("click", btn_vypocitat)
button_reset.bind("click", reset)
for input in document.select("input"):
    input.bind("change", input_zmena)
