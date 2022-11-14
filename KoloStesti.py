# importy
import random
import time
import PySimpleGUI as grafika

# list her, ktere pripadaji v uvahu
list_her = ["Apex Legends", "Overwatch", "PUBG: Battlegrounds", "Payday 2", "League of Legends",
            "Counter Strike: Global Offensive", "Fortnite", "Programovani kola stesti", "Lost Ark", "Fall guys"]

list_her_fanda = ["Overwatch", "Payday 2", "Counter Strike: Global Offensive", "Grant Treft Auto V", "Fall guys", "League of Legends"]

back = "Black"
front = "White"

# menici se text
output=grafika.Text("", text_color=front, background_color=back, font = ("Arial", 18))

apex = grafika.Text(list_her[0], text_color=front, font = ("Arial", 18), background_color=back)
ow = grafika.Text(list_her[1], text_color=front, font = ("Arial", 18), background_color=back)
pubg = grafika.Text(list_her[2], text_color=front, font = ("Arial", 18), background_color=back)
payday2 = grafika.Text(list_her[3], text_color=front, font = ("Arial", 18), background_color=back)
lol = grafika.Text(list_her[4], text_color=front, font = ("Arial", 18), background_color=back)
csgo = grafika.Text(list_her[5], text_color=front, font = ("Arial", 18), background_color=back)
fortnite = grafika.Text(list_her[6], text_color=front, font = ("Arial", 18), background_color=back)
programovani = grafika.Text(list_her[7], text_color=front, font = ("Arial", 18), background_color=back)
lost_ark = grafika.Text(list_her[8], text_color=front, font = ("Arial", 18), background_color=back)
fall_guys = grafika.Text(list_her[9], text_color=front, font = ("Arial", 18), background_color=back)

list_her_grafika = [apex, ow, pubg, payday2, lol, csgo, fortnite, programovani, lost_ark, fall_guys]

# rozlozeni okna
layout = [[grafika.Text("Roztočte kolo štestí:")], [grafika.Button("ZATOČ")],[grafika.Button("FANDA")], [apex], [ow], [pubg], [payday2], [lol], [csgo], [fortnite], [programovani], [lost_ark], [fall_guys], [output]]

# vlastnosti okna
window = grafika.Window(title="Gamerský kolo", layout=layout, margins=(500, 250), background_color="Black")


# beh kola
while True:
    # precteni okna
    event, values = window.read()

    # zmacknuti tlacitka ZATOC
    if event == "ZATOČ":

        interval = 0.01
        konecny_cas = 0.5
        vyherni_hra = random.choice(list_her_grafika)
        hra_cervena = apex
        koncime = False

        while not koncime:
            for hra_zelena in list_her_grafika:
                hra_zelena.update(text_color='Green')
                if interval != 0.1:
                    hra_cervena.update(text_color='White')
                hra_cervena = hra_zelena
                window.refresh()
                time.sleep(interval)
                if interval > konecny_cas and hra_cervena == vyherni_hra:
                    koncime = True
                    break

            interval*=2    

        # vybrani viteze
        output.update("\nUžijte si " + vyherni_hra.Get())
        window.refresh()
    elif event == "FANDA":
        #odpocet
        for i in range(3,0, -1):
            output.update(i)
            window.refresh()
            time.sleep(1)

        # napeti
        output.update("Hra pro dnesni den je...")
        window.refresh()
        time.sleep(3)

        # vybrani viteze
        output.update(random.choice(list_her_fanda))
    # zavreni okna
    if event == grafika.WIN_CLOSED:
        break

