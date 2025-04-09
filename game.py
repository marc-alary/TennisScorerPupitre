import var
import time
from communication import*

def restore():
    try:
        f = open("backup.txt", "r")
        sauvegarde = f.readlines()
        f.close()
        if sauvegarde:
            var.color[0] = int(sauvegarde[0][0])
            var.color[1] = int(sauvegarde[0][1])
            var.userLum = int(sauvegarde[0][2])
            var.score[0][0] = int(sauvegarde[1][0])
            var.score[0][1] = int(sauvegarde[1][1])
            var.score[0][2] = int(sauvegarde[1][2])
            var.score[1][0] = int(sauvegarde[1][3])
            var.score[1][1] = int(sauvegarde[1][4])
            var.score[1][2] = int(sauvegarde[1][5])
            var.setNum = int(sauvegarde[2])
            var.setWin[0][0] = int(sauvegarde[3][0])
            var.setWin[0][1] = int(sauvegarde[3][1])
            var.setWin[0][2] = int(sauvegarde[3][2])
            var.setWin[1][0] = int(sauvegarde[3][3])
            var.setWin[1][1] = int(sauvegarde[3][4])
            var.setWin[1][2] = int(sauvegarde[3][5])
            var.etatSystem = sauvegarde[4]
    except Exception as e:
        print(f"Erreur : {e}")

def backup():
    pass
#     for jeux in range(3):
#         if var.oldScore[0][jeux] != var.score[0][jeux] \
#         or var.oldScore[1][jeux] != var.score[1][jeux]:
#             difference=difference + 1
#         if var.oldColor[0] != var.color[0] or var.oldColor[1] != var.color[1] \
#         or var.userLum != varOldUserLum or var.setNum != var.oldSetNum :
#             difference=difference + 1
#     if difference != 0:
#         try:
#             f=open('backup.txt', 'w')           
#             f.write(str(var.color[0]))
#             f.write(str(var.color[1]))
#             f.write(str(var.userLum)+"\n")
#             f.write(str(var.score[0][0]))
#             f.write(str(var.score[0][1]))
#             f.write(str(var.score[0][2]))
#             f.write(str(var.score[1][0]))
#             f.write(str(var.score[1][1]))
#             f.write(str(var.score[1][2])+"\n")   
#             f.write(str(var.setNum)+"\n")
#             f.write(str(var.setWin[0][0]))
#             f.write(str(var.setWin[0][1]))
#             f.write(str(var.setWin[0][2]))
#             f.write(str(var.setWin[1][0]))
#             f.write(str(var.setWin[1][1]))
#             f.write(str(var.setWin[1][2])+"\n")         
#             f.write(var.etatSystem)
#             f.close()
#         except Exception as e:
#             print(f"Erreur : {e}")

def zero_test():
    # On regarde si tout est à zéro score et sets gagnés
    for ligne in var.score:
        for element in ligne:
            if element != 0:
                return False
    for ligne in var.setWin:
        for element in ligne:
            if element != 0:
                return False
    var.j1Dn = var.j2Dn = False
    return True

def win_test():
    # On regarde si un des joueurs à gagné deux sets
    winJ1=var.setWin[0][0]+var.setWin[0][1]+var.setWin[0][2]
    winJ2=var.setWin[1][0]+var.setWin[1][1]+var.setWin[1][2]
    # Si ce n'est pas le cas on peut augmenter les score
    if winJ1 == 2 or winJ2 == 2:
        var.j1Up = var.j2Up = False
        return True
    return False

def up_gestion(j1,j2):
    etat = "STAY"
    var.score[j1][var.setNum] = var.score[j1][var.setNum] + 1
    # Conditions de victoire d'un set
    if (var.score[j1][var.setNum] == 6 and var.score[j2][var.setNum] < 5) \
    or var.score[j1][var.setNum] == 7:
        var.setWin[j1][var.setNum] = var.setWin[j1][var.setNum] + 1
        if win_test() is False:
            var.setNum = var.setNum + 1
            etat = "PLUS"
        else:
            # Condition de fin du match
            etat = "VICTORY"
    return etat
    
def down_gestion(j1,j2):
    etat = "STAY"
    # en cas de victoire 
    if win_test() is True:
        # seul un joueur qui a gagné le set peut revenir au set précédent
        if var.setWin[j1][var.setNum] ==1:
            # on diminue le score mais ...
            var.score[j1][var.setNum] = var.score[j1][var.setNum] - 1
            var.setWin[j1][var.setNum] = var.setWin[j1][var.setNum] - 1
            if var.setNum == 2:
                etat = "SET 3"
            if var.setNum == 1:
                etat = "SET 2"
    if (var.etatSystem is "SET 2" or var.etatSystem is "SET 3"):
        var.score[j1][var.setNum] = var.score[j1][var.setNum] - 1        
        if var.score[j1][var.setNum] < 0 and var.setWin[j1][var.setNum-1] ==1:
            var.score[j1][var.setNum] = 0
            var.score[j2][var.setNum] = 0
            var.setNum = var.setNum - 1
            if var.score[j1][var.setNum] > 5:
                var.score[j1][var.setNum]=5
            var.setWin[j1][var.setNum] = var.setWin[j1][var.setNum] - 1
            etat="MOINS"
        elif var.score[j1][var.setNum] < 0:
            var.score[j1][var.setNum] = 0
    if var.etatSystem is "SET 1":
        var.score[j1][var.setNum] = var.score[j1][var.setNum] - 1
        if var.score[j1][var.setNum] < 0:
            var.score[j1][var.setNum] = 0
        etat = "STAY"        
    return etat

def reset_test():
    if var.reset is True:
        var.reset = False
        return True
    return False

def parameter_test():
    if var.parameter is True:
        var.parameter = False
        return True
    return False

def valid_test():
    if var.valid is True:
        var.valid = False
        return True
    return False

def reset_game():
    var.score = [[0, 0, 0],[0, 0, 0]] 
    var.oldScore = [[0, 0, 0],[0, 0, 0]]                
    var.setNum = 0
    var.oldSetNum = 0
    var.setWin = [[0, 0, 0],[0, 0, 0]] 
    var.oldSetWin = [[0, 0, 0],[0, 0, 0]]
    sendall_to_everyone()
    send_to_club_house()
    sleep(1)
    sleep(2)
    sleep(4)
    sleep(5)

def up_down_test():
    suite="STAY"
    if win_test() is False :
        if var.j1Up is True:
            var.j1Up = False
            #var.j1Dn = var.j2Up = var.j2Dn = False
            suite=up_gestion(0,1)
        if var.j2Up is True:
            var.j2Up = False
            #var.j1Dn = var.j1Up = var.j2Dn = False
            suite=up_gestion(1,0)
    if zero_test() is False:
        if var.j1Dn is True:
            var.j1Dn = False
            #var.j1Up = var.j2Up = var.j2Dn = False
            suite = down_gestion(0,1)    
        if var.j2Dn is True:
            var.j2Dn = False
            #var.j1Dn = var.j2Up = var.j1Up = False
            suite = down_gestion(1,0)
    return suite