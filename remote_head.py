from periphery import GPIO
import time
from tkinter import *
import json

#======================== PINOUT DEF ======================

try:
    with open ("config.json") as config_f:
       config = json.load(config_f)
       step_resolution = config["STEP_RESOLUTION"]
except FileNotFoundError:
    print("Brak pliku konfiguracyjnego.")
    exit()


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
DIR_AZ_GPIO.write(True) #dir- lewo
DIR_EL_GPIO.write(False) #dir- gora
STEP_AZ_GPIO.write(False)
STEP_EL_GPIO.write(False)
MS1_GPIO.write(False)
MS2_GPIO.write(False)
MS3_GPIO.write(False)


def resolution(step_resolution): #brane z configu
    if step_resolution==1:
        #full step
        MS1_GPIO.write(False)
        MS2_GPIO.write(False)
        MS3_GPIO.write(False)
        print("Dokładność ustawiona na 1.8 stopnia.")
    elif step_resolution==2:
        #half step
        MS1_GPIO.write(True)
        MS2_GPIO.write(False)
        MS3_GPIO.write(False)
        print("Dokładność ustawiona na 0.9 stopnia")
    elif step_resolution==4:
        #1/4 step
        MS1_GPIO.write(False)
        MS2_GPIO.write(True)
        MS3_GPIO.write(False)
        print("Dokładność ustawiona na  0.45 stopnia")
    elif step_resolution==8:
        #1/8 step
        MS1_GPIO.write(True)
        MS2_GPIO.write(True)
        MS3_GPIO.write(False)
        print("Dokładność ustawiona na 0.225 stopnia")
    elif step_resolution==16:
        #1/16 step
        MS1_GPIO.write(True)
        MS2_GPIO.write(True)
        MS3_GPIO.write(True)
        print("Dokładność ustawiona na 0.1125 stopnia")
    else: 
        #full
        MS1_GPIO.write(False)
        MS2_GPIO.write(False)
        MS3_GPIO.write(False)

def az360(): #kalibracja
    DIR_AZ_GPIO.write(True)#lewo
    for i in range(200):
        STEP_AZ_GPIO.write(True)
        time.sleep(0.01)
        STEP_AZ_GPIO.write(False)
        time.sleep(0.01)
    x=input("Kliknij enter aby wrócić do startowej pozycji.")
    DIR_AZ_GPIO.write(False)#prawo
    for i in range(200):
        STEP_AZ_GPIO.write(True)
        time.sleep(0.01)
        STEP_AZ_GPIO.write(False)
        time.sleep(0.01)
    DIR_AZ_GPIO.write(True)#lewo
    print("System w pozycji startowej.")

def el360(): #kalibracja
    DIR_EL_GPIO.write(False) #gora
    for i in range(200):
        STEP_EL_GPIO.write(True)
        time.sleep(0.01)
        STEP_EL_GPIO.write(False)
        time.sleep(0.01)
    x=input("Kliknij enter aby wrócić do startowej pozycji.")
    DIR_EL_GPIO.write(True) #dol
    for i in range(200):
        STEP_EL_GPIO.write(True)
        time.sleep(0.01)
        STEP_EL_GPIO.write(False)
        time.sleep(0.01)
    DIR_EL_GPIO.write(False) #gora
    print("System w pozycji startowej.")

def step_up_down():
    STEP_EL_GPIO.write(True)
    time.sleep(0.01)
    STEP_EL_GPIO.write(False)
    time.sleep(0.01)

def step_left_right():
    STEP_AZ_GPIO.write(True)
    time.sleep(0.01)
    STEP_AZ_GPIO.write(False)
    time.sleep(0.01)

def obrot_lewo(ilosc_krokow):
    print("Obrót w lewo o " + str(ilosc_krokow*(1/step_resolution)*1.8))
    DIR_AZ_GPIO.write(False)  #lewo
    for i in range(ilosc_krokow):
        step_left_right()

def obrot_prawo(ilosc_krokow):
    print("Obrót w prawo o " + str(ilosc_krokow*(1/step_resolution)*1.8))
    DIR_AZ_GPIO.write(True)  #prawo
    for i in range(ilosc_krokow):
        step_left_right()

def obrot_gora(ilosc_krokow):
    print("Obrót w góra o " + str(ilosc_krokow*(1/step_resolution)*1.8))
    DIR_EL_GPIO.write(False) #gora
    for i in range(ilosc_krokow):
        step_up_down()

def obrot_dol(ilosc_krokow):
    print("Obrót w dół o " + str(ilosc_krokow*(1/step_resolution)*1.8))
    DIR_EL_GPIO.write(True) #dol
    for i in range(ilosc_krokow):
        step_up_down()

######## TK_INTER_KLAWIATURA ###############
def move_left():
    DIR_AZ_GPIO.write(False) 
    step_left_right()

def move_right():
    DIR_AZ_GPIO.write(True) 
    step_left_right()

def move_up():
    DIR_EL_GPIO.write(False) 
    step_up_down()

def move_down():
    DIR_EL_GPIO.write(True) 
    step_up_down()

def klawisze():
    # Utwórz okno tkinter
    root = Tk()
    root.title("Sterowanie silnikiem krokowym")

    # Dodaj przyciski do sterowania
    button_left = Button(root, text="W lewo", command=move_left)
    button_right = Button(root, text="W prawo", command=move_right)
    button_up = Button(root, text="W górę", command=move_up)
    button_down = Button(root,text="  W dół  ", command=move_down)
    button_stop = Button(root, text="Stop", command=root.destroy)

    # Ustawienie układu przycisków
    button_left.grid(row=2, column=0)
    button_right.grid(row=2, column=2)
    button_up.grid(row=1,column=1)
    button_down.grid(row=2,column=1)
    button_stop.grid(row=3, column=1)

    # Obsługa zdarzeń klawiatury
    def on_key_press(event):
        if event.keysym == 'Left':
            move_left()
        elif event.keysym == 'Right':
            move_right()
        elif event.keysym == 'Up':
            move_up()
        elif event.keysym == 'Down':
            move_down()

    def on_key_release(event):
        print('done')
    
    # Przypisanie funkcji do zdarzeń klawiatury
    root.bind('<KeyPress>', on_key_press)
    root.bind('<KeyRelease>', on_key_release)

    # Uruchomienie pętli głównej
    root.mainloop()

    print("Zamknieto okno.")


################################# MENU #################################
if __name__ == "__main__":
    resolution(step_resolution)
    while True:
        print("MENU: \n 1.Pokaz obrotu lewo-prawo \n 2.Sterowanie klawiatura \n 3.Kalibracja obrotu j\n 0.Wyjście")
        menu_val=input("Wybierz numer: ")
        try:
            menu_val=int(menu_val)
        except:
            print('Wpisz poprawną liczbę opcji. Spróbuj ponownie.')

        if menu_val==1:
            print("Tu będzie pokaz.")
            
        elif menu_val==2:
            klawisze()

        elif menu_val==3:
            while True:
                print("Sprawdź kalibracje w: \n 1.Poziomie-Azymucie \n 2.Pionie-Elewacji \n 3.WRÓĆ")
                menu_kal_val=int(input("Wybierz opcje: "))
                if menu_kal_val==1:
                    print("Czy 360 to 360? - lewoprawo ")
                    az360()
                elif menu_kal_val==2:
                    print("Czy 360 to 360? - goradol ")
                    el360()
                elif menu_kal_val==3:
                    break
                else:
                    print("cos poszlo nie tak w kalibracji")

        elif menu_val==0:
            break
        else:
            print("Coś poszło nie tak w menu")

    print('SHUTDOWN.')

    DIR_AZ_GPIO.close()
    DIR_EL_GPIO.close()
    STEP_AZ_GPIO.close()
    STEP_EL_GPIO.close()
    MS1_GPIO.close()
    MS2_GPIO.close()
    MS3_GPIO.close()
