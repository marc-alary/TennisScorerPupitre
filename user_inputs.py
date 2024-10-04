# Gestion des boutons poussoir en interruption
from machine import Pin, ADC, Timer
import var
import time

timer = Timer(0)

def debounce(t):
    var.bp = 0

def bp_j1_up_isr(pin):
    if var.bp == 0:           
        testJ1 = var.setWin[0]
        testJ2 = var.setWin[1]
        if testJ1.count(1) < 2 and testJ2.count(1) < 2:
            var.score[0][var.setNum] = var.score[0][var.setNum] + 1
        timer.init(mode=Timer.ONE_SHOT, period=300, callback=debounce)
        var.bp = var.bp + 1

def bp_j2_up_isr(pin):
    if var.bp == 0: 
        testJ1 = var.setWin[0]
        testJ2 = var.setWin[1]
        if testJ1.count(1) < 2 and testJ2.count(1) < 2:
            var.score[1][var.setNum] = var.score[1][var.setNum] + 1
        timer.init(mode=Timer.ONE_SHOT, period=300, callback=debounce)
        var.bp = var.bp + 1
   
def bp_j1_down_isr(pin):
    if var.bp == 0: 
        var.score[0][var.setNum] = var.score[0][var.setNum] - 1
        timer.init(mode=Timer.ONE_SHOT, period=300, callback=debounce)
        var.bp = var.bp + 1
   
def bp_j2_down_isr(pin):
    if var.bp == 0: 
        var.score[1][var.setNum] = var.score[1][var.setNum] - 1
        timer.init(mode=Timer.ONE_SHOT, period=300, callback=debounce)
        var.bp = var.bp + 1
    
def bp_parameter_isr(pin):
    if var.bp == 0: 
        var.parameters = True
        timer.init(mode=Timer.ONE_SHOT, period=300, callback=debounce)
        var.bp = var.bp + 1

def bp_valid_isr(pin):
    if var.bp == 0: 
        var.valid = True
        timer.init(mode=Timer.ONE_SHOT, period=300, callback=debounce)
        var.bp = var.bp + 1 
    
def bp_score_reset_isr(pin):
    if var.bp == 0:
        var.reset = True
        timer.init(mode=Timer.ONE_SHOT, period=300, callback=debounce)
        var.bp = var.bp + 1     

def vin_test_isr(pin):
    print ("\n\rCoupure courant !")
    f=open('backup.txt', 'w')
    f.write(str(var.colorJ1))
    f.write(str(var.colorJ2))
    f.write(str(var.lux))
    f.write(str(var.scoreJ1[0]))
    f.write(str(var.scoreJ1[1]))
    f.write(str(var.scoreJ1[2]))
    f.write(str(var.scoreJ2[0]))
    f.write(str(var.scoreJ2[1]))
    f.write(str(var.scoreJ2[2]))
    f.close()
    print ("Joueur 1", var.scoreJ1, ": Joueur 2", var.scoreJ2, "\r", end='')

var.BP_J1_UP.irq(trigger=Pin.IRQ_RISING,handler=bp_j1_up_isr)
var.BP_J2_UP.irq(trigger=Pin.IRQ_RISING,handler=bp_j2_up_isr)
var.BP_J1_DOWN.irq(trigger=Pin.IRQ_RISING,handler=bp_j1_down_isr)
var.BP_J2_DOWN.irq(trigger=Pin.IRQ_RISING,handler=bp_j2_down_isr)
var.BP_RESET_SCORE.irq(trigger=Pin.IRQ_RISING,handler=bp_score_reset_isr)
var.BP_PARAMETER.irq(trigger=Pin.IRQ_FALLING,handler=bp_parameter_isr)
var.BP_VALID.irq(trigger=Pin.IRQ_FALLING,handler=bp_valid_isr)
var.VIN_TEST.irq(trigger=Pin.IRQ_FALLING,handler=vin_test_isr)

