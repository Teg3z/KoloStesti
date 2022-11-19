# importy
import random
import time
import PySimpleGUI as grafika

def Toceni(list_konkretni, kc):
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

# list her, ktere pripadaji v uvahu
list_her = ["Apex Legends", "Overwatch", "PUBG: Battlegrounds", "Payday 2", "Counter Strike: Global Offensive", 
            "Fortnite", "Programovani kola stesti", "Lost Ark", "Fall Guys", "League of Legends", "Grant Treft Auto V"]

# barvy
back = "Black"
front = "White"

# font
nas_font = ("Arial", 18)

# texty
output=grafika.Text("", text_color=front, background_color=back, font = nas_font)

list_her_grafika = []

# vytvor list textu z listu her
for hra in list_her:
    list_her_grafika.append(grafika.Text(hra, text_color=front, font = nas_font, background_color=back, key=hra))

# buttony
zatoc = grafika.Button("ZATOČ", button_color = 'Green', font = nas_font , mouseover_colors='DarkGreen')
fanda = grafika.Button("FANDA", button_color = 'Green', font = nas_font, mouseover_colors='DarkGreen')


# vytvor layout z danych her
layout = []

for hra in list_her_grafika:
    layout.append([hra])


# pridej buttony
layout.append([output])
layout.append([zatoc,fanda])

# vlastnosti okna
window = grafika.Window(title="Gamerský kolo", layout=layout, margins=(500, 250), background_color="Black", use_default_focus=False)

# beh kola
while True:
    # precteni okna
    event, values = window.read()

    # zmacknuti tlacitka ZATOC
    if event == "ZATOČ":
        list_nas = list_her_grafika
        list_nas.pop()

        window["Grant Treft Auto V"].Update(visible = False)

        Toceni(list_nas, random.uniform(0.3, 0.8))   

    elif event == "FANDA":
        list_fanda = []
        jedemeListFanda = False

        for hra in list_her_grafika:
            if (jedemeListFanda or hra.Get() == "Fall Guys"):
                list_fanda.append(hra)
                jedemeListFanda = True
            else:
                window[hra.Get()].Update(visible = False)

        window.refresh()

        Toceni(list_fanda, random.uniform(0.3, 0.5))

    # zavreni okna
    elif event == grafika.WIN_CLOSED:
        break

