# importy
import random
import time
import PySimpleGUI as grafika

# list her, ktere pripadaji v uvahu
list_her = ["Apex Legends", "Overwatch", "PUBG: Battlegrounds", "Payday 2", "League of Legends",
            "Counter Strike: Global Offensive", "Fortnite", "Programovani kola stesti", "Grant Treft Auto V", "Lost Ark"]

# menici se text
output=grafika.Text("\nDefault")

# rozlozeni okna
layout = [[grafika.Text("Roztočte kolo štestí:")], [grafika.Button("ZATOČ")], [output]]

# vlastnosti okna
window = grafika.Window(title="Gamerský kolo", layout=layout, margins=(500, 250))


# beh kola
while True:
    # precteni okna
    event, values = window.read()

    # zmacknuti tlacitka ZATOC
    if event == "ZATOČ":
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
        output.update(random.choice(list_her))

    # zavreni okna
    if event == grafika.WIN_CLOSED:
        break    
