import motor_controller
#from tk_same_klawisze import *

while True:
    print("MENU: \n 1.Pełny pomiar przestrzenny \n 2.Pomiar w jednym kierunku \n 3.Kalibracja obrotu \n 0.Wyjście")
    menu_val=input("Wybierz numer: ")
    try:
        menu_val=int(menu_val)
    except:
        print('Wpisz poprawną liczbę opcji. Spróbuj ponownie.')
    


    if menu_val==1:
        
        print("Zaraz zostanie wykoany pomiar przestrzenny, czy wszyscy sa gotowi?")
        print("Przejscie po czestotliwosci i obroty")
        motor_controller.kroki_20()
        

    elif menu_val==2:
        #print("Tutaj bedzie sterowanie itp.")
        #klawisze()  #tk_same_klawisze
        f_pomiaru=input("Podaj czestotliwość pomiaru w Hz: ")
        potwierdzenie=input("Czy wykonać pomiar? T/N ")
        if potwierdzenie=='N':
            continue
        else:
            print("Wykonuje")
            #pomiar here

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

