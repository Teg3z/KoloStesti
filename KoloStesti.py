# importy
import random
import time

# list her, ktere pripadaji v uvahu
list_her = ["Apex Legends", "Overwatch", "PUBG: Battlegrounds", "Payday 2", "League of Legends",
            "Counter Strike: Global Offensive", "Fortnite", "Programovani kola stesti", "Grant Treft Auto V", "Lost Ark"]

#odpocet
for i in range(3,0, -1):
    print(i)
    time.sleep(1)

print("Hra pro dnesni den je...")  
time.sleep(1)
  
# vybrani viteze
print(random.choice(list_her))