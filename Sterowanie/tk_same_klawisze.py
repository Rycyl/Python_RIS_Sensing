from tkinter import *
from motor_controller import *


def move_left():
    print('leca w lewo')
    step_left()

def move_right():
    print('leca w prawo') 
    step_right()

def move_up():
    print('gora')
    step_up()

def move_down():
    print('dol')
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


