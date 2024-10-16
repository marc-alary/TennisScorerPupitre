# Boot Afficheur

import ugit
import network
import time
from machine import Pin

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

f = open("update.txt", "r")
testUpdate = f.read()
f.close()
if testUpdate is "True":
    wlan.connect("Marcus","cf08cfa03572")
    essais = 0
    time.sleep(2)
    while not wlan.isconnected() and essais < 10:
        time.sleep(2)
        print("Connecting ...")
        essais = essais + 1
    if essais < 10:
        try:
            ugit.pull_all()
        except:
            print("Erreur de mise à jour !")
    else :
        print("Connexion impossible !")
else :
    print("Run sans OTA")
