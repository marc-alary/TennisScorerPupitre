# Boot Pupitre

import ugit
import network
import time
from machine import Pin

BP_RESET_SCORE = Pin(19, Pin.IN, Pin.PULL_DOWN)

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

if BP_RESET_SCORE.value() == True:
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
            f = open("update.txt", "w")
            f.write("True")
            f.close()
        except:
            print("Erreur de mise à jour !")
    else :
        print("Connexion impossible !")
else :
    print("Run sans OTA")