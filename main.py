# Afficheur V5.0
# Date mise à jour : 09/04/2025
#################################################################### Etat # Actif #####   
# Fonction : Gestion touches +- RAZ des joueurs : ................... ok     Oui
# Fonction : Gestion scores et des conditions de victoires : ........ ok     Oui
# Fonction : Décrémentation possible en cas de victoire : ........... ok     Oui
# Fonction : Sauvegarde, restauration scores et des paramètres : .... ok     Non
# Fonction : Paramètres couleurs joueurs et luminosité globale : .... ok     Oui
# Fonction : Communication score par ethernet : ..................... ok     Oui
# Fonction : Luminosité automatique : ............................... xx     --
# Fonction : Affichage informations de débogage sur écran oled : .... xx     --
# Fonction : Mise à jour other the air : ............................ ok     Oui
# Fonction : Gestion du score par smartphone : ...................... xx     --
# Fonction : Gestion des modes de fonctionnement : .................. ok   Partiel
#######################################################################################
# A définir avec le client :
#	Que faire en cas de non réponse d'un afficheur ?
#	Comment choisir le mode smartphone, avec club house ou pupitre seul ?
#	 

import var
import time
from communication import *
from user_inputs import *
from oled_display import *
from game import *
from serial_to_eth import *

version = "20250409"

class switch(object):
    value = None
    def __new__(class_, value):
        class_.value = value
        return True

def case(*args):
    return any((arg == switch.value for arg in args))

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

print("Attente des afficheurs ...")
test_connexion()
restore()

print ("")
print ("Pupitre TennisScorer Rev: " + version)
print ("Niveau de luminosité :", var.userLum)
print ("Couleur J1 :", var.couleurs[var.color[0]], "Couleur J2 :", var.couleurs[var.color[1]]) 
print ("Joueur 1", var.score[0], ": Joueur 2", var.score[1], "\r")
    
f = open("update.txt", "r")
updateTest = f.read()
f.close()
if "True" in updateTest:
    # Envoi de U pour Update aux 6 afficheurs
    print("Update afficheurs")
    update_afficheurs_firmware()
    f = open("update.txt", "w")
    f.write("False")
    f.close()
    test_update()
    clear_screen()
    write_ligne(" Tennis Scorer ", 1)
    write_ligne(" ------------- ", 2)
    mes="Rev : " + version
    write_ligne(mes, 3)
    write_ligne("Etat afficheurs",4)
    write_ligne("   | | | | |   ",5)
    write_ligne(" ------------- ",6)
    message = "  "+afficheurs[0]+"|"\
          +afficheurs[1]+"|"\
          +afficheurs[2]+"|"\
          +afficheurs[3]+"|"\
          +afficheurs[4]+"|"\
          +afficheurs[5]+"  "
    write_ligne(message, 5)
    
send_score()

#init_configuration()

while(True):
    ####################################################
    # Test de l'état du système
    ####################################################    
    while switch(var.etatSystem):  
        #######################################################
        # Premier set égalité zéro partout, début du match
        #######################################################
        if case("SET 1"):
            if var.oldEtatSystem != var.etatSystem:
                print("Etat système :", var.etatSystem)
                oled_system_state(var.etatSystem)
                var.oldEtatSystem = var.etatSystem
                awake(0)
                awake(3)
                sleep(1)
                sleep(2)
                sleep(4)
                sleep(5)
            match=up_down_test()
            if match is "PLUS":
                var.etatSystem = "SET 2"
                awake(1)
                awake(4)
            if parameter_test() is True and zero_test() is True: # Appui sur couleur
                var.etatSystem = "COLORJ1"
            if reset_test() is True:
                var.etatSystem = "RESET"
            send_score()
            break
        #######################################################
        # Réglage couleur joueur 1
        #######################################################
        if case("COLORJ1"):
            if var.oldEtatSystem != var.etatSystem:
                print("Etat système :", var.etatSystem)
                oled_system_state(var.etatSystem)
                var.oldEtatSystem = var.etatSystem
            var.score = [[8, 8, 8],[8, 8, 8]]
            sendall_to_everyone()
            while parameter_test() is False:
                if valid_test() is True:
                    time.sleep_ms(200)
                    if var.color[0] <= 7:
                        var.color[0] = var.color[0] + 1
                        if var.color[0] > 7:
                            var.color[0] = 0
                        var.oldColor[0] = var.color[0]
                    for i in range(3):
                        e.send(var.adrMac[i], data_convert(i))
                        #print(var.adrMac[i], data_convert(i))
            var.etatSystem="COLORJ2"
            print("Etat système :", var.etatSystem)
            oled_system_state(var.etatSystem)
            break
        #######################################################
        # Réglage couleur joueur 2
        #######################################################
        if case("COLORJ2"):
            while parameter_test() is False:
                if valid_test() is True:
                    time.sleep_ms(200)
                    if var.color[1] <= 7:
                        var.color[1] = var.color[1] + 1
                        if var.color[1] > 7:
                            var.color[1] = 0
                        var.oldColor[1] = var.color[1]
                    for i in range(3):
                        e.send(var.adrMac[i+3], data_convert(i+3))
                        #print(var.adrMac[i], data_convert(i))
            var.etatSystem="LUMINOSITE"
            print("Etat système :", var.etatSystem)
            oled_system_state(var.etatSystem)
            break
        #######################################################
        # Réglage lumisoité joueurs 1 et 2
        #######################################################
        if case("LUMINOSITE"):
            while parameter_test() is False:
                if valid_test() is True:
                    time.sleep_ms(200)
                    if var.userLum < 4:
                        var.userLum = var.userLum + 1
                        if var.userLum > 3:
                            var.userLum = 1
                        var.oldUserLum = var.userLum
                    sendall_to_everyone()
            var.etatSystem="RESET"
            backup()
            oled_system_state(var.etatSystem)
            break
        #######################################################
        # Un joueur mène un set à zéro, deuxième set
        #######################################################
        if case("SET 2"):
            if var.oldEtatSystem != var.etatSystem:
                print("Etat systeme : ", var.etatSystem)
                oled_system_state(var.etatSystem)
                var.oldEtatSystem = var.etatSystem
            match=up_down_test()
            if match is "PLUS":
                var.etatSystem = "SET 3"
                awake(2)
                awake(5)
            if match is "VICTORY":
                var.etatSystem = "VICTORY"
            if match is "MOINS":
                var.etatSystem = "SET 1"
                sleep(1)
                sleep(4)
            if reset_test() is True:
                var.etatSystem = "RESET"
            send_score()
            break
        #######################################################
        # Egalité un Set partout, troisième et dernier set
        #######################################################
        if case("SET 3"):
            if var.oldEtatSystem != var.etatSystem:
                print("Etat systeme : ", var.etatSystem)
                oled_system_state(var.etatSystem)
                var.oldEtatSystem = var.etatSystem
            match=up_down_test()
            if match is "VICTORY":
                var.etatSystem = "VICTORY"
            if match is "MOINS":
                var.etatSystem = "SET 2"
                sleep(2)
                sleep(5)
            if reset_test() is True:
                var.etatSystem = "RESET"
            send_score()
            break
        #######################################################
        # Victoire d'un joueur fin du match
        #######################################################
        if case("VICTORY"):
            if var.oldEtatSystem != var.etatSystem:
                print("Etat systeme : ", var.etatSystem)
                oled_system_state(var.etatSystem)
                var.oldEtatSystem = var.etatSystem
            match=up_down_test()
            if match is "SET 3":
                var.etatSystem = "SET 3"
            if match is "SET 2":
                var.etatSystem = "SET 2"
            if reset_test() is True:
                var.etatSystem = "RESET"
            send_score()
            break
        #######################################################
        # Remise à zéro du score
        #######################################################
        if case("RESET"):
            if var.oldEtatSystem != var.etatSystem:
                print("Etat systeme : ", var.etatSystem)
                oled_system_state(var.etatSystem)
                var.oldEtatSystem = var.etatSystem
            reset_game()
            var.etatSystem = "SET 1"
            break