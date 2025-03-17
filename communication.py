import var
import time
import network
import espnow
from oled_display import *

sta = network.WLAN(network.STA_IF)
sta.active(True)

#time.sleep(1)
e = espnow.ESPNow()
e.active(True)
#time.sleep(1)

var.parameters = False
afficheurs = [" "," "," "," "," "," "]

for i in range (0, 6):
    e.add_peer(var.adrMac[i])
#     print("Conecting with : ", var.adrMac[i])
#     time.sleep(1)

def send_with_ack(peerAck, dataAck):
    essais = 0
    while(e.send(peerAck, dataAck, True)) is not True and essais < 3:
        essais = essais + 1
        time.sleep(0.1)
        print("Erreur com with : ", peerAck)

def etat_afficheurs():      
        message = "  "+afficheurs[0]+"|"\
          +afficheurs[1]+"|"\
          +afficheurs[2]+"|"\
          +afficheurs[3]+"|"\
          +afficheurs[4]+"|"\
          +afficheurs[5]+""
        time.sleep(5)
        return message

def test_connexion():
    while " " in afficheurs:
        for i in range (0, 6):
            try:
                e.add_peer(var.adrMac[i])
            except:
                print("Afficheur ", i, "déjà connecté !")
        for i in range (0, 6):
            if (e.send(var.adrMac[i], "black-0-0", True)) is True:
                print(i, "Ok")
                afficheurs[i] = "X"
            else:
                print("Afficheur n°",i," ne répond pas !")
            print(afficheurs)
        clear_ligne(5)
        message = "  "+afficheurs[0]+"|"\
          +afficheurs[1]+"|"\
          +afficheurs[2]+"|"\
          +afficheurs[3]+"|"\
          +afficheurs[4]+"|"\
          +afficheurs[5]+"  "
        write_ligne(message, 5)
        time.sleep(5)
        
def update_afficheurs_firmware():
    for i in range (0, 6):
        send_with_ack(var.adrMac[i], "U")

def sleep(number):
    data = "black-0-0"
    send_with_ack(var.adrMac[number], data)
   
def awake(number):
    if number < 3:
        data = str(var.couleurs[var.color[0]])+"-"+str(var.score[0][number])+"-"+str(var.lux)
    if number > 2 and number < 6:
        data = str(var.couleurs[var.color[1]])+"-"+str(var.score[1][number-3])+"-"+str(var.lux)    
    send_with_ack(var.adrMac[number], data)

def data_convert(number):
    if number in range(0,3):
        data = str(var.couleurs[var.color[0]])+"-"+str(var.score[0][number])+"-"+str(var.lux)
    if number in range (3,6):
        data = str(var.couleurs[var.color[1]])+"-"+str(var.score[1][number-3])+"-"+str(var.lux)
    return data

def sendall_to_everyone():
    # Envoi couleurs choisies et luminosité globale
    print("-----------------------------")    
    for afficheur in range (0,6):
        #print(var.adrMac[afficheur], data_convert(afficheur))
        send_with_ack(var.adrMac[afficheur], data_convert(afficheur))       

def send_change():
    for jeux in range (3):
        if var.oldScore[0][jeux] != var.score[0][jeux]:
            send_with_ack(var.adrMac[jeux], data_convert(jeux))
            print ("Set", var.setNum, "J1", var.score[0], var.setWin[0], \
            ": J2", var.score[1], var.setWin[1])
            #print (var.adrMac[jeux], data_convert(jeux), "                  ")
        if var.oldScore[1][jeux] != var.score[1][jeux]:
            send_with_ack(var.adrMac[jeux+3], data_convert(jeux+3))
            print ("Set", var.setNum, "J1", var.score[0], var.setWin[0], \
            ": J2", var.score[1], var.setWin[1])
            #print (var.adrMac[jeux+3], data_convert(jeux+3), "                  ")
        var.oldScore[0][jeux] = var.score[0][jeux]
        var.oldScore[1][jeux] = var.score[1][jeux]