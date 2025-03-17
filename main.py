import var
import time
from oled_display import *
from user_inputs import *
from communication import *
from serial_to_eth import*

version = "20241024"
etatSystem = "START"
oldEtatSystem = "RIEN"

class switch(object):
    value = None
    def __new__(class_, value):
        class_.value = value
        return True

def case(*args):
    return any((arg == switch.value for arg in args))

def restore():
    try:
        f = open("backup.txt", "r")
        sauvegarde = f.readlines()
        f.close()
        if sauvegarde:
            var.color[0] = int(sauvegarde[0][0])
            var.color[1] = int(sauvegarde[0][1])
            var.lux = int(sauvegarde[0][2])
            var.score[0][0] = int(sauvegarde[1][0])
            var.score[0][1] = int(sauvegarde[1][1])
            var.score[0][2] = int(sauvegarde[1][2])
            var.score[1][0] = int(sauvegarde[1][3])
            var.score[1][1] = int(sauvegarde[1][4])
            var.score[1][2] = int(sauvegarde[1][5])
            setNum = int(sauvegarde[2])
            setWin[0][0] = int(sauvegarde[3][0])
            setWin[0][1] = int(sauvegarde[3][1])
            setWin[0][2] = int(sauvegarde[3][2])
            setWin[1][0] = int(sauvegarde[3][3])
            setWin[1][1] = int(sauvegarde[3][4])
            setWin[1][2] = int(sauvegarde[3][5])
            etatSystem = sauvegarde[4]
    except:
        print("Erreur de sauvagarde !")

def backup():
    try:
        f=open('backup.txt', 'w')
        f.write(str(var.color[0]))
        f.write(str(var.color[1]))
        f.write(str(var.lux)+"\n")
        f.write(str(var.score[0][0]))
        f.write(str(var.score[0][1]))
        f.write(str(var.score[0][2]))
        f.write(str(var.score[1][0]))
        f.write(str(var.score[1][1]))
        f.write(str(var.score[1][2])+"\n")
        f.write(str(var.setNum)+"\n")
        f.write(str(var.setWin[0][0]))
        f.write(str(var.setWin[0][1]))
        f.write(str(var.setWin[0][2]))
        f.write(str(var.setWin[1][0]))
        f.write(str(var.setWin[1][1]))
        f.write(str(var.setWin[1][2])+"\n")
        f.write(etatSystem)
        f.close()
    except:
        print("Erreur de sauvegarde")

clear_screen()
write_ligne(" Tennis Scorer ", 1)
write_ligne(" ------------- ", 2)
mes="Rev : " + version
write_ligne(mes, 3)
write_ligne("Etat afficheurs",4)
write_ligne("   | | | | |   ",5)
write_ligne(" ------------- ",6)
write_ligne("Attente reponse",7)
write_ligne("afficheurs.....",8)

#init_configuration()
start_http_server() #start the HTTP page _thread
#serv_web()

while True:
    pass

print("Attente des afficheurs ...")
test_connexion()

restore()

print ("")
print ("Pupitre TennisScorer Rev: " + version)
print ("Niveau de luminosité :", var.lux)
print ("Couleur J1 :", var.couleurs[var.color[0]], "Couleur J2 :", var.couleurs[var.color[1]]) 
print ("Joueur 1", var.score[0], ": Joueur 2", var.score[1], "\r")
    
f = open("update.txt", "r")
updateTest = f.read()
f.close()
if "True" in updateTest:
    # Envoi de U pour Update aux 6 afficheurs
    update_afficheurs_firmware()
    f = open("update.txt", "w")
    f.write("False")
    f.close()



while(True):   
    ####################################################
    # Test de l'état du système
    ####################################################    
    while switch(etatSystem):  
        #######################################################
        # Premier set égalité zéro partout, début du match
        #######################################################
        if case("START"):
            if oldEtatSystem != etatSystem:
                clear_ligne(7)
                clear_ligne(8)
                write_ligne(etatSystem,7)
                oldEtatSystem = etatSystem
                var.score = [[0, 0, 0],[0, 0, 0]]                
                var.setNum = 0
                var.setWin = [[0, 0, 0],[0, 0, 0]]
                sendall_to_everyone()
                var.oldSetNum = 0
                var.oldScore = [[0, 0, 0],[0, 0, 0]]
                sleep(1)
                sleep(2)
                sleep(4)
                sleep(5)
                print("Etat système START premier passage")
            if var.valid == True:
                var.valid = False
                etatSystem="COLORJ1"
                print("Etat système :", etatSystem)
                clear_ligne(7)
                clear_ligne(8)
                write_ligne(etatSystem,7)
            if var.oldScore != var.score:
                etatSystem="SET 1"
                var.setNum = 0
                print("Etat système :", etatSystem)
                clear_ligne(7)
                clear_ligne(8)
                write_ligne(etatSystem,7)
            break
        #######################################################
        # Réglage couleur joueur 1
        #######################################################
        if case("COLORJ1"):
            var.score = [[8, 8, 8],[8, 8, 8]]
            sendall_to_everyone()
            while var.valid is not True:
                if var.parameters is True:
                    var.parameters = False
                    if var.color[0] <= 7:
                        var.color[0] = var.color[0] + 1
                        if var.color[0] > 7:
                            var.color[0] = 0
                        var.oldColor[0] = var.color[0]
                    for i in range(3):
                        e.send(var.adrMac[i], data_convert(i))
                        #print(var.adrMac[i], data_convert(i))
            etatSystem="COLORJ2"
            print("Etat système :", etatSystem)
            clear_ligne(7)
            clear_ligne(8)
            write_ligne(etatSystem,7)
            var.valid = False
            break
        #######################################################
        # Réglage couleur joueur 2
        #######################################################
        if case("COLORJ2"):
            while var.valid is not True:
                if var.parameters is True:
                    var.parameters = False
                    if var.color[1] <= 7:
                        var.color[1] = var.color[1] + 1
                        if var.color[1] > 7:
                            var.color[1] = 0
                        var.oldColor[1] = var.color[1]
                    for i in range(3):
                        e.send(var.adrMac[i+3], data_convert(i+3))
                        #print(var.adrMac[i], data_convert(i))
            etatSystem="LUMINOSITE"
            print("Etat système :", etatSystem)
            clear_ligne(7)
            clear_ligne(8)
            write_ligne(etatSystem,7)
            var.valid = False
            break
        #######################################################
        # Réglage lumisoité joueurs 1 et 2
        #######################################################
        if case("LUMINOSITE"):
            while var.valid is not True:
                if var.parameters is True:
                    var.parameters = False
                    if var.lux < 4:
                        var.lux = var.lux + 1
                        if var.lux > 3:
                            var.lux = 0
                        var.oldLux = var.lux
                    sendall_to_everyone()
            var.valid = False
            etatSystem="START"
            try:
                f = open("backup.txt", "r")
                sauvegarde = f.readlines()
                f.write(str(var.color[0]) + str(var.color[1]) + str(var.lux))
                f.close()
            except:
                print("Erreur de sauvegarde")
            clear_ligne(7)
            clear_ligne(8)
            write_ligne(etatSystem,7)
            break
        #######################################################
        # Egalité zéro zéro, début du match premier set
        #######################################################
        if case("SET 1"):
            if var.reset == True:
                etatSystem = "RESET"
                clear_ligne(7)
                clear_ligne(8)
                write_ligne(etatSystem,7)
                var.reset = False
                print("Etat système :", etatSystem)
            else:
                for j1 in range(2):
                    if j1 == 1:
                        j2 = 0
                    else:
                        j2 = j1+1
                    if (var.score[j1][var.setNum] == 6 and var.score[j2][var.setNum] < 5) \
                    or var.score[j1][var.setNum] == 7:
                        var.setWin[j1][var.setNum] = var.setWin[j1][var.setNum] + 1
                        etatSystem="SET 2"
                        var.setNum = 1
                        print("Etat système :", etatSystem)
                        clear_ligne(7)
                        clear_ligne(8)
                        write_ligne(etatSystem,7)
                        awake(1)
                        awake(4)
                    if var.score[j1][var.setNum] < 0:
                        var.score[j1][var.setNum] = 0
                send_change()
            break
        #######################################################
        # Un joueur mène un set à zéro, deuxième set
        #######################################################
        if case("SET 2"):
            if var.reset == True:
                etatSystem="RESET"
                var.reset = False
                print("Etat système :", etatSystem)
                clear_ligne(7)
                clear_ligne(8)
                write_ligne(etatSystem,7)
            else:
                for j1 in range(2):
                    if j1 == 1:
                        j2 = 0
                    else:
                        j2 = j1+1
                    if (var.score[j1][var.setNum] == 6 and var.score[j2][var.setNum] < 5) \
                    or var.score[j1][var.setNum] == 7:
                        var.setWin[j1][var.setNum] = var.setWin[j1][var.setNum] + 1
                        test = var.setWin[j1]
                        if test.count(1) == 2:
                            etatSystem="VICTORY"
                        else:
                            etatSystem="SET 3"
                            var.setNum = 2
                            awake(2)
                            awake(5)
                        print("Etat système :", etatSystem)
                        clear_ligne(7)
                        clear_ligne(8)
                        write_ligne(etatSystem,7)
                        var.setNum = 2
                    if var.score[j1][var.setNum] < 0:
                        if var.setWin[j1][var.setNum -1] == 0:
                            var.score[j1][var.setNum] = 0
                        if var.setWin[j1][var.setNum -1] == 1:
                            var.score[j1][var.setNum] = 0
                            var.score[j2][var.setNum] = 0
                            var.score[j1][var.setNum -1] = var.score[j1][var.setNum -1] - 1
                            var.setWin[j1][var.setNum -1] = var.setWin[j1][var.setNum -1] - 1
                            etatSystem="SET 1"
                            var.setNum = 0
                            sleep(1)
                            sleep(4)
                send_change()
            break
        #######################################################
        # Egalité un Set partout, troisième et dernier set
        #######################################################
        if case("SET 3"):
            if var.reset == True:
                etatSystem="RESET"
                var.reset = False
                print("Etat système :", etatSystem)
                clear_ligne(7)
                clear_ligne(8)
                write_ligne(etatSystem,7)
            else:
                for j1 in range(2):
                    if j1 == 1:
                        j2 = 0
                    else:
                        j2 = j1+1
                    if (var.score[j1][var.setNum] == 6 and var.score[j2][var.setNum] < 5) \
                    or var.score[j1][var.setNum] == 7:
                        var.setWin[j1][var.setNum] = var.setWin[j1][var.setNum] + 1
                        test = var.setWin[j1]
                        if test.count(1) == 2:
                            etatSystem = "VICTORY"
                            print("Etat système :", etatSystem)
                            clear_ligne(7)
                            clear_ligne(8)
                            write_ligne(etatSystem,7)
                    if var.score[j1][var.setNum] < 0:
                        if var.setWin[j1][var.setNum - 1] == 0:
                            var.score[j1][var.setNum] = 0
                        if var.setWin[j1][var.setNum - 1] == 1:
                            var.score[j1][var.setNum] = 0
                            var.score[j2][var.setNum] = 0
                            var.score[j1][var.setNum - 1] = var.score[j1][var.setNum -1] - 1
                            var.setWin[j1][var.setNum -1] = var.setWin[j1][var.setNum - 1] - 1
                            etatSystem="SET 2"
                            print("Etat système :", etatSystem)
                            clear_ligne(7)
                            clear_ligne(8)
                            write_ligne(etatSystem,7)
                            var.setNum = 1
                            sleep(2)
                            sleep(5)
                send_change()
            break
        #######################################################
        # Victoire d'un joueur fin du match
        #######################################################
        if case("VICTORY"):    
            if var.reset == True:
                etatSystem="RESET"
                var.reset = False
                print("Etat système :", etatSystem)
                clear_ligne(7)
                clear_ligne(8)
                write_ligne(etatSystem,7)
            else:
                for j1 in range(2):
                    if j1 == 1:
                        j2 = 0
                    else:
                        j2 = j1+1          
                    if var.setWin[j1][var.setNum] == 0:
                        if var.score[j1][var.setNum] < 0:
                            var.score[j1][var.setNum] = 0
                    if var.setWin[j1][var.setNum] == 1:
                        if (var.score[j1][var.setNum] == 5 and var.score[j2][var.setNum] < 5)\
                        or (var.score[j1][var.setNum] == 6 and (var.score[j2][var.setNum] ==6 \
                        or var.score[j2][var.setNum] ==5)): 
                            var.setWin[j1][var.setNum] = var.setWin[j1][var.setNum] - 1
                test1 = var.setWin[0]
                test2 = var.setWin[1]
                if test1.count(1) < 2 and test2.count(1) < 2:
                    if var.setNum == 2:
                        etatSystem="SET 3"
                        print("Etat système :", etatSystem)
                        clear_ligne(7)
                        clear_ligne(8)
                        write_ligne(etatSystem,7)
                    if var.setNum == 1:
                        etatSystem="SET 2"
                        print("Etat système :", etatSystem)
                        clear_ligne(7)
                        clear_ligne(8)
                        write_ligne(etatSystem,7)
                send_change()
            break
        #######################################################
        # Victoire d'un joueur fin du match
        #######################################################
        if case("RESET"):
            oldEtatSystem = etatSystem
            etatSystem = "START"
            clear_ligne(7)
            clear_ligne(8)
            write_ligne(etatSystem,7)
            break