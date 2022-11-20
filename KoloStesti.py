# importy
import random
import time
import PySimpleGUI as grafika
from datetime import date

# absultni cesta k logum
cesta_logy = r"REPLACED_PATH\KoloStesti\Logs.txt"

def MakeAllVisible(list_konkretni, window):
    for hra in list_konkretni:
        window[hra.Get()].Update(visible = True)

def Vybel(list_konkretni):
    for hra_bila in list_konkretni:
        hra_bila.update(text_color='White')

def Toceni(list_konkretni, kc):

    Vybel(list_konkretni)

    interval = 0.01
    konecny_cas = kc
    vyherni_hra = random.choice(list(list_konkretni))
    hra_bila = list_konkretni[0]
    koncime = False

    while not koncime:
        for hra_zelena in list_konkretni:
            hra_zelena.update(text_color='Lime')
            if interval != 0.01:
                hra_bila.update(text_color='White')
            hra_bila = hra_zelena
            window.refresh()
            time.sleep(interval)
            if interval > konecny_cas and hra_bila == vyherni_hra:
                koncime = True
                break

            interval+=0.02    

    # vybrani viteze
    output.update("\nUžijte si " + vyherni_hra.Get())
    window.refresh()

    return vyherni_hra

# list her, ktere pripadaji v uvahu
# TODO tuples
list_her = ["Apex Legends", "PUBG: Battlegrounds", "Payday 2", "Counter Strike: Global Offensive", 
            "Fortnite", "Programovani kola stesti", "Lost Ark", "Fall Guys", "Overwatch", "League of Legends", "Grant Treft Auto V"]

# barvy
back = "Black"
front = "White"

# font
nas_font = ("Arial", 18)

# texty
output = grafika.Text("", text_color=front, background_color=back, font = nas_font)
minula_hra = grafika.Text("Jak dopadla minulá hra?", text_color=front, background_color=back, font = nas_font)

list_her_grafika = []

# vytvor list textu z listu her
for hra in list_her:
    list_her_grafika.append(grafika.Text(hra, text_color=front, font = nas_font, background_color=back, key=hra))

# buttony
zatoc = grafika.Button("ZATOČ", button_color = 'Green', font = nas_font , mouseover_colors='DarkGreen')
fanda = grafika.Button("FANDA", button_color = 'Green', font = nas_font, mouseover_colors='DarkGreen')
w = grafika.Button("W", button_color = 'Green', font = nas_font, mouseover_colors='DarkGreen')
l = grafika.Button("L", button_color = 'Green', font = nas_font, mouseover_colors='DarkGreen')


# vytvor layout z danych her
layout = []

for hra in list_her_grafika:
    layout.append([hra])

# pridej buttony
layout.append([output])
layout.append([zatoc,fanda])
layout.append([minula_hra])
layout.append([w,l])

# vlastnosti okna
window = grafika.Window(title="Gamerský kolo", layout=layout, margins=(500, 250), background_color="Black", use_default_focus=False)

# databaze
database = open(cesta_logy, "at")

# vyherce
konecna_vyherni_hra = list_her_grafika[0]

# beh kola
while True:
    # precteni okna
    event, values = window.read()

    # zmacknuti tlacitka ZATOC
    if event == "ZATOČ":
        MakeAllVisible(list_her_grafika, window)
        window["Grant Treft Auto V"].Update(visible = False)

        list_nas = list(list_her_grafika)
        list_nas.pop()

        konecna_vyherni_hra = Toceni(list_nas, random.uniform(0.3, 0.8))

    elif event == "FANDA":
        window["Grant Treft Auto V"].Update(visible = True)

        list_fanda = []
        jedemeListFanda = False

        for hra in list_her_grafika:
            if (jedemeListFanda or hra.Get() == "Fall Guys"):
                list_fanda.append(hra)
                jedemeListFanda = True
            else:
                window[hra.Get()].Update(visible = False)

        window.refresh()

        konecna_vyherni_hra = Toceni(list_fanda, random.uniform(0.3, 0.5))
    elif event == "W":
        database.write("W\n")
    elif event == "L":
        database.write("L\n")
    # zavreni okna
    elif event == grafika.WIN_CLOSED:
        database.write(date.today().strftime("%d.%m.%Y") + " " + konecna_vyherni_hra.Get() + " ")
        database.close()
        break

