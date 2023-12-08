from periphery import GPIO
import time
import analyzer

#======================== PINOUT DEF ======================
#Kąt azymut-dolny silnik
DIR_AZ_GPIO=GPIO(95,'out')
STEP_AZ_GPIO=GPIO(96,'out')
#Kąt elewacji-górny silnik 
DIR_EL_GPIO=GPIO(115,'out')
STEP_EL_GPIO=GPIO(100,'out')
#Rozdzielczosc kroku
MS1_GPIO=GPIO(98,'out')
MS2_GPIO=GPIO(102,'out')
MS3_GPIO=GPIO(101,'out')

#default values
DIR_AZ_GPIO.write(False) #dir-
DIR_EL_GPIO.write(False)
STEP_AZ_GPIO.write(False)
STEP_EL_GPIO.write(False)
MS1_GPIO.write(False)
MS2_GPIO.write(False)
MS3_GPIO.write(False)


def resolution():
    res_val=1
    #res_val=input("Wybierz rozdzielczość: \n 1. full \n 2. 1/2 \n 4. 1/4 \n 8. 1/8 \n 16. 1/16 \n Wybieram: ")
    if res_val==1:
        #full step
        MS1_GPIO.write(False)
        MS2_GPIO.write(False)
        MS3_GPIO.write(False)
    elif res_val==2:
        #half step
        MS1_GPIO.write(True)
        MS2_GPIO.write(False)
        MS3_GPIO.write(False)
    elif res_val==4:
        #1/4 step
        MS1_GPIO.write(False)
        MS2_GPIO.write(True)
        MS3_GPIO.write(False)
    elif res_val==8:
        #1/8 step
        MS1_GPIO.write(True)
        MS2_GPIO.write(True)
        MS3_GPIO.write(False)
    elif res_val==16:
        #1/16 step
        MS1_GPIO.write(True)
        MS2_GPIO.write(True)
        MS3_GPIO.write(True)
    else: 
        #full
        MS1_GPIO.write(False)
        MS2_GPIO.write(False)
        MS3_GPIO.write(False)


def azimut_step():
    print('hops lewoprawo')

def elew_step():
    print('hops goradol')

def az360():
    for i in range(200):
        STEP_AZ_GPIO.write(True)
        time.sleep(0.2)
        STEP_AZ_GPIO.write(False)
        time.sleep(0.2)
    x=input("Kliknij enter aby wrócić do startowej pozycji.")
    DIR_AZ_GPIO.write(True)
    for i in range(200):
        STEP_AZ_GPIO.write(True)
        time.sleep(0.2)
        STEP_AZ_GPIO.write(False)
        time.sleep(0.2)
    DIR_AZ_GPIO.write(False)
    print("System w pozycji startowej.")

def el360():
    for i in range(200):
        STEP_EL_GPIO.write(True)
        time.sleep(0.2)
        STEP_EL_GPIO.write(False)
        time.sleep(0.2)
    x=input("Kliknij enter aby wrócić do startowej pozycji.")
    DIR_EL_GPIO.write(True)
    for i in range(200):
        STEP_EL_GPIO.write(True)
        time.sleep(0.2)
        STEP_EL_GPIO.write(False)
        time.sleep(0.2)
    DIR_EL_GPIO.write(False)
    print("System w pozycji startowej.")


def kroki_20():
    
    for i in range(20):
        STEP_AZ_GPIO.write(True)
        time.sleep(0.01)
        STEP_AZ_GPIO.write(False)
        time.sleep(0.01)

def kroki_wstecz():
    
    for i in range(20):
        STEP_AZ_GPIO.write(True)
        time.sleep(0.01)
        STEP_AZ_GPIO.write(False)
        time.sleep(0.01)

def step_up():
    DIR_EL_GPIO.write(False) #TODO SPRAWDZIC CZY DOBRA STRONA

    STEP_EL_GPIO.write(True)
    time.sleep(0.2)
    STEP_EL_GPIO.write(False)
    time.sleep(0.2)

def step_down():
    DIR_EL_GPIO.write(True) #TODO SPRAWDZIC CZY DOBRA STRONA

    STEP_EL_GPIO.write(True)
    time.sleep(0.2)
    STEP_EL_GPIO.write(False)
    time.sleep(0.2)

def step_left():
    DIR_AZ_GPIO.write(False) #TODO SPRAWDZIC CZY DOBRA STRONA

    STEP_AZ_GPIO.write(True)
    time.sleep(0.2)
    STEP_AZ_GPIO.write(False)
    time.sleep(0.2)

def step_right():
    DIR_AZ_GPIO.write(True) #TODO SPRAWDZIC CZY DOBRA STRONA

    STEP_AZ_GPIO.write(True)
    time.sleep(0.2)
    STEP_AZ_GPIO.write(False)
    time.sleep(0.2)


"""
while True:
    try:
        print("Wybierz opcje: \n ")
        



    except KeyboardInterrupt:
        LED_GPIO.write(False)
        break
    except IOError:
        print('error')


"""

analyzer.com_prep()
analyzer.com_check()
#analyzer.meas_prep(28E9, 100E3, "MAXHold ")
print("Pomiar 20 krokow")

for i in range(10):
    analyzer.meas_prep(28E9, 100E3, "MAXHold ", -30, "500 Hz")
    analyzer.trace_get()

    kroki_20()
    time.sleep(0.3)

time.sleep(1)

for i in range(10):
    DIR_AZ_GPIO.write(True)
    kroki_wstecz()
    

analyzer.close()

DIR_AZ_GPIO.close()
DIR_EL_GPIO.close()
STEP_AZ_GPIO.close()
STEP_EL_GPIO.close()
MS1_GPIO.close()
MS2_GPIO.close()
MS3_GPIO.close()