# Gestion des boutons poussoir en interruption
from machine import Pin, ADC, Timer
import var
import time

timer = Timer(0)
TIME_DEBOUNCE=300

def debounce(t):
    var.bp = True

def bp_j1_up_isr(pin):
    if var.bp is True:
        var.bp = False
        var.j1Up = True
        timer.init(mode=Timer.ONE_SHOT, period=TIME_DEBOUNCE, callback=debounce)
        #print(var.j1Up)

def bp_j2_up_isr(pin):
    if var.bp is True:
        var.bp = False
        var.j2Up = True
        timer.init(mode=Timer.ONE_SHOT, period=TIME_DEBOUNCE, callback=debounce)
        #print(var.j2Up)
   
def bp_j1_down_isr(pin):
    if var.bp is True:
        var.bp = False
        var.j1Dn = True
        timer.init(mode=Timer.ONE_SHOT, period=TIME_DEBOUNCE, callback=debounce)
        #print(var.j1Dn)
   
def bp_j2_down_isr(pin):
    if var.bp is True:
        var.bp = False
        var.j2Dn = True
        timer.init(mode=Timer.ONE_SHOT, period=TIME_DEBOUNCE, callback=debounce)
        #print(var.j2Dn)
        
def bp_parameter_isr(pin):
    if var.bp is True:
        var.bp = False
        var.parameter = True
        timer.init(mode=Timer.ONE_SHOT, period=TIME_DEBOUNCE, callback=debounce)
        #print(var.parameter) 

def bp_valid_isr(pin):
    if var.bp is True:
        var.bp = False
        var.valid = True
        timer.init(mode=Timer.ONE_SHOT, period=TIME_DEBOUNCE, callback=debounce)
        #print(var.valid) 
    
def bp_score_reset_isr(pin):
    if var.bp is True:
        var.bp = False
        var.reset = True
        timer.init(mode=Timer.ONE_SHOT, period=TIME_DEBOUNCE, callback=debounce)
        #print(var.reset)    

def vin_test_isr(pin):
    pass

var.BP_J1_UP.irq(trigger=Pin.IRQ_RISING,handler=bp_j1_up_isr)
var.BP_J2_UP.irq(trigger=Pin.IRQ_RISING,handler=bp_j2_up_isr)
var.BP_J1_DOWN.irq(trigger=Pin.IRQ_RISING,handler=bp_j1_down_isr)
var.BP_J2_DOWN.irq(trigger=Pin.IRQ_RISING,handler=bp_j2_down_isr)
var.BP_RESET_SCORE.irq(trigger=Pin.IRQ_RISING,handler=bp_score_reset_isr)
var.BP_PARAMETER.irq(trigger=Pin.IRQ_FALLING,handler=bp_parameter_isr)
var.BP_VALID.irq(trigger=Pin.IRQ_FALLING,handler=bp_valid_isr)
#var.VIN_TEST.irq(trigger=Pin.IRQ_FALLING,handler=vin_test_isr)

