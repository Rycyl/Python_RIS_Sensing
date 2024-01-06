from periphery import GPIO
import time
from tkinter import *
#import analyzer

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
DIR_AZ_GPIO.write(True) #dir- lewo
DIR_EL_GPIO.write(False) #dir- gora
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


def azimut_step(step_number_az):
    DIR_AZ_GPIO.write(True) #lewo
    for i in range(step_number_az):
        STEP_AZ_GPIO.write(True)
        time.sleep(0.01)
        STEP_AZ_GPIO.write(False)
        time.sleep(0.01)

def elew_step(step_number_el):
    DIR_EL_GPIO.write(False) #gora
    for i in range(step_number_el):
        STEP_EL_GPIO.write(True)
        time.sleep(0.006)
        STEP_EL_GPIO.write(False)
        time.sleep(0.006)

def az360():
    DIR_AZ_GPIO.write(True)#lewo
    for i in range(200):
        STEP_AZ_GPIO.write(True)
        time.sleep(0.006)
        STEP_AZ_GPIO.write(False)
        time.sleep(0.006)
    x=input("Kliknij enter aby wrócić do startowej pozycji.")
    DIR_AZ_GPIO.write(False)#prawo
    for i in range(200):
        STEP_AZ_GPIO.write(True)
        time.sleep(0.006)
        STEP_AZ_GPIO.write(False)
        time.sleep(0.006)
    DIR_AZ_GPIO.write(True)#lewo
    print("System w pozycji startowej.")

def el360():
    DIR_EL_GPIO.write(False) #gora
    for i in range(200):
        STEP_EL_GPIO.write(True)
        time.sleep(0.006)
        STEP_EL_GPIO.write(False)
        time.sleep(0.006)
    x=input("Kliknij enter aby wrócić do startowej pozycji.")
    DIR_EL_GPIO.write(True) #dol
    for i in range(200):
        STEP_EL_GPIO.write(True)
        time.sleep(0.006)
        STEP_EL_GPIO.write(False)
        time.sleep(0.006)
    DIR_EL_GPIO.write(False) #gora
    print("System w pozycji startowej.")


def kroki_el_pom(ile_kr):
    for i in range(ile_kr):
        STEP_EL_GPIO.write(True)
        time.sleep(0.006)
        STEP_EL_GPIO.write(False)
        time.sleep(0.006)

def kroki_wstecz_az(): #obrot wstecz o 360 stopni
    DIR_AZ_GPIO.write(False) #prawo
    for i in range(200):
        STEP_AZ_GPIO.write(True)
        time.sleep(0.006)
        STEP_AZ_GPIO.write(False)
        time.sleep(0.006)
    DIR_AZ_GPIO.write(True) #lewo
        
def kroki_wstecz_el(ile):
    DIR_EL_GPIO.write(True) #dol
    for i in range(ile): #TODO ILE WSTECZ W ELEWACJI?
        STEP_EL_GPIO.write(True)
        time.sleep(0.006)
        STEP_EL_GPIO.write(False)
        time.sleep(0.006)

def step_up():
    DIR_EL_GPIO.write(False) 

    STEP_EL_GPIO.write(True)
    time.sleep(0.006)
    STEP_EL_GPIO.write(False)
    time.sleep(0.006)
def step_down():
    DIR_EL_GPIO.write(True) 

    STEP_EL_GPIO.write(True)
    time.sleep(0.006)
    STEP_EL_GPIO.write(False)
    time.sleep(0.006)
def step_left():
    DIR_AZ_GPIO.write(False) 

    STEP_AZ_GPIO.write(True)
    time.sleep(0.006)
    STEP_AZ_GPIO.write(False)
    time.sleep(0.006)
def step_right():
    DIR_AZ_GPIO.write(True) 

    STEP_AZ_GPIO.write(True)
    time.sleep(0.006)
    STEP_AZ_GPIO.write(False)
    time.sleep(0.006)

def pomiar():
    DIR_EL_GPIO.write(True) #dol
    kroki_el_pom(15) #zjazd o i stopni w dol - punkt poczatkowy pomiaru
    
    for i in range(20):
        for x in range(7):
            az_angle=i*18
            el_angle=-27+9*x
            #analyzer.meas_prep(28E9, 100E3, "MAXHold ", -30, "500 Hz")
            #analyzer.trace_get(az_angle,el_angle)
            time.sleep(0.1)
            elew_step(5) #TODO o ile krokow w gore - 9 stopni
            
        kroki_wstecz_el(35) #TODO o ile krokow wraca 7*5=35
        azimut_step(10) # krok w azymucie o 18 stopni

    time.sleep(1)
    kroki_wstecz_az() #powrot o 360 stopni w azymucie

    DIR_EL_GPIO.write(False) #dol
    kroki_el_pom(15) #powrot o i stopni w gore

        
######## TK_INTER_KLAWIATURA ###############
def move_left():
    step_left()

def move_right():
    step_right()

def move_up():
    step_up()

def move_down():
    step_down()

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

    print("Zamknieto okno, uzupełnij dane pomiaru.")
################################# MENU #################################

#analyzer.com_prep()
#analyzer.com_check()
while True:
    print("MENU: \n 1.Pełny pomiar przestrzenny \n 2.Pomiar w jednym kierunku \n 3.Kalibracja obrotu \n 0.Wyjście")
    menu_val=input("Wybierz numer: ")
    try:
        menu_val=int(menu_val)
    except:
        print('Wpisz poprawną liczbę opcji. Spróbuj ponownie.')

    if menu_val==1:
        print("Wykonuje pomiar przestrzenny....")
        pomiar() 

    elif menu_val==2:
        print("MENU: \n 1.Pomiar z ustawieniem ręcznym głowicy. \n 2.Pomiar z wykorzystaniem klawiatury.")
        menu2_val=input("Wybierz numer: ")
        try:
            menu2_val=int(menu2_val)
        except:
            print('Wpisz poprawną liczbę opcji. Spróbuj ponownie.')

        if(menu2_val==2):
            klawisze()  #tk_same_klawisze - sterowanie mozna odpalic tylko na rocku, nie da sie zdalnie
        else:
            pom_menu2=input("Po ustawieniu wciśnij cokolwiek.")

        f_pomiaru=input("Podaj czestotliwość pomiaru w GHz: ")
        potwierdzenie=input("Czy wykonać pomiar? T/N ")
        if potwierdzenie=='N':
            continue
        else:
            print("Wykonuje.")
            #analyzer.meas_prep({f_pomiaru}E9, 100E3, "MAXHold ", -30, "500 Hz")
            #analyzer.trace_get(0,0) #nalezy podac katy jako argumenty
            print("Zapisano wynik pomiaru do pliku.")
            

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

#analyzer.close()
DIR_AZ_GPIO.close()
DIR_EL_GPIO.close()
STEP_AZ_GPIO.close()
STEP_EL_GPIO.close()
MS1_GPIO.close()
MS2_GPIO.close()
MS3_GPIO.close()
