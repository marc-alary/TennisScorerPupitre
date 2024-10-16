import var
import time
from user_inputs import *
from communication import * 

etatSystem = "START"
oldEtatSystem = "RIEN"

class switch(object):
    value = None
    def __new__(class_, value):
        class_.value = value
        return True

def case(*args):
    return any((arg == switch.value for arg in args))

f = open("backup.txt", "r")
sauvegarde = f.read()
f.close()
if sauvegarde:
    var.color[0] = int(sauvegarde[0])
    var.color[1] = int(sauvegarde[1])
    var.lux = int(sauvegarde[2])
    var.score[0][0] = int(sauvegarde[3])
    var.score[0][1] = int(sauvegarde[4])
    var.score[0][2] = int(sauvegarde[5])
    var.score[1][0] = int(sauvegarde[6])
    var.score[1][1] = int(sauvegarde[7])
    var.score[1][2] = int(sauvegarde[8])

print("Attente des afficheurs ...")
test_connexion()

print ("")
print ("Pupitre TennisScorer V1.0")
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
            if var.oldScore != var.score:
                etatSystem="SET 1"
                var.setNum = 0
                print("Etat système :", etatSystem)
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
            var.valid = False
            break
        #######################################################
        # Réglage lumisoité joueurs 1 et 2
        #######################################################
        if case("LUMINOSITE"):
            while var.valid is not True:
                if var.parameters is True:
                    var.parameters = False
                    if var.lux < 10:
                        var.lux = var.lux + 1
                        if var.lux > 9:
                            var.lux = 0
                        var.oldLux = var.lux
                    sendall_to_everyone()
            var.valid = False
            f=open('backup.txt', 'w')
            f.write(str(var.color[0]))
            f.write(str(var.color[1]))
            f.write(str(var.lux))
            f.write("000000")
            f.close()
            etatSystem="START"
            break
        #######################################################
        # Egalité zéro zéro, début du match premier set
        #######################################################
        if case("SET 1"):
            if var.reset == True:
                etatSystem = "RESET"
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
                    if var.setNum == 1:
                        etatSystem="SET 2"
                        print("Etat système :", etatSystem)
                send_change()
            break
        #######################################################
        # Victoire d'un joueur fin du match
        #######################################################
        if case("RESET"):
            oldEtatSystem = etatSystem
            etatSystem = "START"
            break
