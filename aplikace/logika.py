# externí knihovny, třídy atd.
from browser import window, document, alert
from javascript import Date
sw_alert = window.Swal.fire

# globální konstanty
NAZEV_APLIKACE = "Brzděnka+"
VERZE = "verze 0.3 | 0.B.3 (\u03B2)"
AKTUALNI_ROK = Date.new().getFullYear()
AUTOR = f"\u00A9 {AKTUALNI_ROK}&nbsp;&nbsp;Martin TÁBOR"
UPOZORNENI = "!!! Všechny informace jsou bez záruky !!!".upper()
OBRAZEK_ZOB = "./obrazky/zob-popka.webp"  # případně *.jpg

BARVA_NORMAL = "#0073d7"  # modrá
BARVA_POZOR = "#D70000"  # červená

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
div_formular_vypocet = document["formular_vypocet"]
input_potrebna = document["input_potrebna_procenta"]
input_skutecna = document["input_skutecna_procenta"]
label_chybejici = document["label_chybejici_procenta"]
input_chybejici = document["input_chybejici_procenta"]
input_max_rychlost = document["input_max_rychlost"]
button_vypocitat = document["button_vypocitat"]
button_reset = document["button_reset"]


def chybne_vyplneni(ev, title, text):
    sw_alert({
        "title": title,
        "text": text,
        "icon": "question",
        "confirmButtonText": "Heuréka !",
        "confirmButtonColor": BARVA_NORMAL,
        "showCloseButton": True,
        "imageUrl": OBRAZEK_ZOB,
        "imageWidth": 600,
        "imageHeight": 1200,
        "imageAlt": "Zpráva o brzdění z POP"
    })

def zpracuj_vysledek(vstup):
    # alert(f"{vstup}\n\n{UPOZORNENI}\n\n{AUTOR}")

    zprava_max_rychlost = "Maximální rychlost vlaku je {} km/h!"
    zprava_u_vystrahy = "\nV úrovni návěsti Výstraha však max. {} km/h!"
    zprava_nelze_rozklad = "\nNELZE použít rozklad."
    
    sw_alert({
        "title": "Zpomal",
        "html": f"{vstup}",
        "icon": "warning",
        "confirmButtonText": "Budiž",
        "confirmButtonColor": BARVA_POZOR,
        "footer": f"<div style='text-align: center;'><span style='color: {BARVA_POZOR}'>{UPOZORNENI}</span><br>{AUTOR}</div>"
    })

def vypocitat(ev):
    if input_potrebna.value.isnumeric() \
        and input_skutecna.value.isnumeric() \
            and input_max_rychlost.value.isnumeric():

        if potrebna_procenta > 0 \
            and skutecna_procenta > 0 \
                and max_rychlost > 0:

            # načtení vstupních hodnot
            global potrebna_procenta
            potrebna_procenta = int(input_potrebna.value)
            global skutecna_procenta
            skutecna_procenta = int(input_skutecna.value)
            global chybi_procent
            chybi_procent = potrebna_procenta - skutecna_procenta
            if chybi_procent < 0: chybi_procent = 0
            global max_rychlost
            max_rychlost = int(input_max_rychlost.value)
            # lokální pojmenování globálních proměnných
            potrebna_p = potrebna_procenta
            skutecna_p = skutecna_procenta
            rychlost_vlaku = max_rychlost
            
            zprava = "Maximální rychlost vlaku je {} km/h!"
            zprava2 = "\nV úrovni návěsti Výstraha však max. {} km/h!"
            nelze_rozklad = "\nNELZE použít rozklad."

            # zjištění dalších vstupních parametrů
            # skutečná procenta <= 45 ?
            if skutecna_p <= 45:
                prc_mensi_45 = True
            else:
                prc_mensi_45 = False
            # původní max. rychlost >= 120 km/h ?
            if rychlost_vlaku >= 120:
                rych_120_a_vice = True
            else:
                rych_120_a_vice = False
            # chybějící procenta ?
            prc_chybejici = potrebna_p - skutecna_p
            
            
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
            # některé políčko formuláře obsahuje hodnotu <= 0
            chybne_vyplneni(ev,
            title="Překlep ?",
            text="Všechny údaje v(e) ZOB by měly být větší než nula\u2026")
    else:
        # některé políčko formuláře neobsahuje číslo
        chybne_vyplneni(ev,
            title="Jak na to ?",
            text="Jednoduše přepište všechny vyznačené údaje ze ZOB do formuláře\u2026")


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
        div_formular_vypocet.style.display = "none"
        sw_alert({
            "icon": "info",
            "title": "Existuje tabulka ?",
            "text": "Při určení maximální rychlosti se tedy řiďte jejími údaji !",
            "confirmButtonColor": BARVA_NORMAL
        })
    else:
        div_formular_vypocet.style.display = "unset"


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
button_vypocitat.bind("click", vypocitat)
button_reset.bind("click", reset)
for input in document.select("input"):
    input.bind("change", input_zmena)