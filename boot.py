# Boot pupitre
import ugit
import network
import time
from machine import Pin
from oled_display import *

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

BP_RESET_SCORE = Pin(19, Pin.IN, Pin.PULL_DOWN)

if BP_RESET_SCORE.value()==1:
    wlan.connect("Marcus","cf08cfa03572")
    essais = 0
    time.sleep(2)
    clear_screen()
    write_ligne("Firmware update",3)
    write_ligne("in progress ...",4)
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
            clear_screen()
            write_ligne("   Erreur de   ",3)
            write_ligne(" transfert !!! ",4)
    else :
        print("Connexion impossible !")
        clear_screen()
        write_ligne(" Connexion Web ",3)
        write_ligne(" impossible !  ",4)
else :
    print("Run sans OTA")