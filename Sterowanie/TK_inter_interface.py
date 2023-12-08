from tkinter import *


def move_left():
    print('leca w lewo')

def move_right():
    print('leca w prawo') 

def stop_program():
    print('papa')
    #TODO
# Utwórz okno tkinter
root = Tk()
root.title("Sterowanie silnikiem krokowym")

# Dodaj przyciski do sterowania
button_left = Button(root, text="W lewo", command=move_left)
button_right = Button(root, text="W prawo", command=move_right)
button_stop = Button(root, text="Stop program", command=stop_program)

# Ustawienie układu przycisków
button_left.grid(row=1, column=0)
button_right.grid(row=1, column=2)
button_stop.grid(row=2, column=1)

# Obsługa zdarzeń klawiatury
def on_key_press(event):
    if event.keysym == 'Left':
        move_left()
    elif event.keysym == 'Right':
        move_right()

def on_key_release(event):
    print('done')

# Przypisanie funkcji do zdarzeń klawiatury
root.bind('<KeyPress>', on_key_press)
root.bind('<KeyRelease>', on_key_release)

# Uruchomienie pętli głównej
root.mainloop()