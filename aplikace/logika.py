from browser import window, document, alert
from javascript import Date
sw_alert = window.Swal.fire

NAZEV_APLIKACE = "Brzděnka+"
VERZE = "verze 0.3 | 0.B.3 (\u03B2)"
AKTUALNI_ROK = Date.new().getFullYear()
AUTOR = f"\u00A9 {AKTUALNI_ROK}&nbsp;&nbsp;Martin TÁBOR"
UPOZORNENI = "!!! Všechny informace jsou bez záruky !!!".upper()
OBRAZEK_ZOB = "./obrazky/zob-popka.jpg"

barva_normal = "#0073d7" #  modrá
barva_pozor = "#D70000" #  červená

tabulka_rychlosti = False
potrebna_procenta = 0
skutecna_procenta = 0
chyby_procent = 0
max_rychlost = 0

titulek = document["titulek"]
podnadpis = document["podnadpis"]
radio_tabulka_ano = document["radio_tabulka_ano"]
radio_tabulka_ne = document["radio_tabulka_ne"]
div_formular_vypocet = document["formular_vypocet"]
input_potrebna = document["input_potrebna_procenta"]
input_skutecna = document["input_skutecna_procenta"]
input_chybejici = document["input_chybejici_procenta"]
label_chybejici = document["label_chybejici_procenta"]
input_max_rychlost = document["input_max_rychlost"]
button_vypocitat = document["button_vypocitat"]
button_reset = document["button_reset"]

def napoveda_vyplneni(ev):
    sw_alert({
        "title": "Jak na to ?",
        "text": "Jednoduše opište vyznačené údaje ze ZOB do formuláře\u2026",
        "icon": "question",
        "confirmButtonText": "Heuréka !",
        "confirmButtonColor": barva_normal,
        "showCloseButton": True,
        "imageUrl": OBRAZEK_ZOB,
        "imageWidth": 600,
        "imageHeight": 1200,
        "imageAlt": "Zpráva o brzdění"
    })

def zpracuj_vysledek(vstup):
    # alert(f"{vstup}\n\n{UPOZORNENI}\n\n{AUTOR}")
    sw_alert({
        "title": "Zpomal",
        "html": f"{vstup}",
        "icon": "warning",
        "confirmButtonText": "Budiž",
        "confirmButtonColor": barva_pozor,
        "footer": f"<div style='text-align: center;'><span style='color: {barva_pozor}'>{UPOZORNENI}</span><br>{AUTOR}</div>"
    })

def vypocitat(ev):
    if potrebna_procenta > 0 and skutecna_procenta > 0 and max_rychlost > 0:
    
        potrebna_p = potrebna_procenta
        skutecna_p = skutecna_procenta
        rychlost_vlaku = max_rychlost
        
        zprava = "Maximální rychlost vlaku je {} km/h!"
        zprava2 = "\nV úrovni návěsti Výstraha však max. {} km/h!"
        nelze_rozklad = "\nNELZE použít rozklad."

        # Vstupní parametry
        prc_mensi_45 = False
        rych_120_a_vice = False
        prc_chybejici = potrebna_p - skutecna_p
        if skutecna_p <= 45:
            prc_mensi_45 = True
        if rychlost_vlaku >= 120:
            rych_120_a_vice = True
        
        if potrebna_p == skutecna_p:
            zpracuj_vysledek("""Rychlost není třeba přepočítávat.
Brzděte již v dostatečné vzdálenosti před výstrahou!

(Skutečná brzdící procenta jsou stejná jako potřebná.)""")
        
        elif 0 < (skutecna_p - potrebna_p) <= 10:
            zpracuj_vysledek(f"""Rychlost není třeba přepočítávat.
Brzděte však v dostatečné vzdálenosti před výstrahou!

(Máte jen {skutecna_p - potrebna_p} % navíc.)""")

        elif (skutecna_p - potrebna_p) > 10:
            zpracuj_vysledek("Máte dostatek brzdících procent.")
        
        else:
            # Výpočet
            if prc_mensi_45 is False and rych_120_a_vice is False:  # ani <= 45 % A ZÁROVEŇ ani >= 120 km/h
                nova_rychlost = rychlost_vlaku - prc_chybejici
                zpracuj_vysledek(zprava.format(nova_rychlost))
                # print("((debug: 1))")  # debug

            elif prc_mensi_45 and rych_120_a_vice is False:
                nova_rychlost = rychlost_vlaku - (2 * prc_chybejici)
                zpracuj_vysledek(zprava.format(nova_rychlost) + "\n\n(Skutečná % jsou <= 45.)")
                # print("((debug: 2))")  # debug

            elif prc_mensi_45 is False and rych_120_a_vice:
                nova_rychlost = rychlost_vlaku - prc_chybejici
                if 120 < (nova_rychlost - 20):
                    zpracuj_vysledek(zprava.format(nova_rychlost) + zprava2.format(nova_rychlost - 20))
                    # print("((debug: 3a))")  # debug
                else:
                    nova_rychlost -= 20
                    zpracuj_vysledek(zprava.format(nova_rychlost) + nelze_rozklad)
                    # print("((debug: 3b))")  # debug

            elif prc_mensi_45 and rych_120_a_vice:
                nova_rychlost = rychlost_vlaku - (2 * prc_chybejici)
                if 120 < (nova_rychlost - 20):
                    zpracuj_vysledek(zprava.format(nova_rychlost) + zprava2.format(nova_rychlost - 20) +
                                "\n\n(Skutečná % jsou <= 45.)")
                    # print("((debug: 4a))")  # debug
                else:
                    nova_rychlost -= 20
                    zpracuj_vysledek(zprava.format(nova_rychlost) + nelze_rozklad + "\n\n(Skutečná % jsou <= 45.)")
                    # print("((debug: 4b))")  # debug
            else:
                print("((debug: 5 | toto else nemělo nastat = nějaká varianta je nedořešena))")  # debug
                pass
    else:
        napoveda_vyplneni(ev)


def input_zmena(ev):
    # alert(ev.srcElement.id)  # debug

    if input_potrebna.value.isnumeric():
        global potrebna_procenta
        potrebna_procenta = int(input_potrebna.value)
        
    if input_skutecna.value.isnumeric():
        global skutecna_procenta
        skutecna_procenta = int(input_skutecna.value)
        
    global chyby_procent
    chyby_procent = potrebna_procenta - skutecna_procenta
    if chyby_procent <= 0:
        chyby_procent = 0
        input_chybejici.style.color = barva_normal
        label_chybejici.style.color = barva_normal
    else:
        input_chybejici.style.color = barva_pozor
        label_chybejici.style.color = barva_pozor
    input_chybejici.value = str(chyby_procent)
    
    if input_max_rychlost.value.isnumeric():
        global max_rychlost
        max_rychlost = int(input_max_rychlost.value)

    if radio_tabulka_ano.checked:
        div_formular_vypocet.style.display = "none"
        sw_alert({
            "icon": "info",
            "title": "Existuje tabulka ?",
            "text": "Při určení maximální rychlosti se řiďte danou tabulkou !",
            "confirmButtonColor": barva_normal
        })
    else:
        div_formular_vypocet.style.display = "unset"

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

    global chyby_procent
    chyby_procent = 0
    input_chybejici.value = "0"

    global max_rychlost
    max_rychlost = 0
    input_max_rychlost.value = ""
    
    label_chybejici.style.color = barva_normal
    input_chybejici.style.color = barva_normal


document.title = NAZEV_APLIKACE
titulek.textContent = NAZEV_APLIKACE
podnadpis.textContent = VERZE

button_vypocitat.bind("click", vypocitat)
button_reset.bind("click", reset)
for input in document.select("input"):
    input.bind("change", input_zmena)