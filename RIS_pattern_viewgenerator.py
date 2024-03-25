import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageDraw

def hex_to_bin(hex_string):
    # Usuwamy prefix 0x
    hex_string = hex_string.replace("0x", "") 
    # Konwersja hex na binarną z usunięciem prefixu binarnego '0b' i dopełnieniem zerami
    bin_string = ''.join(format(int(c, 16),'04b') for c in hex_string)
    print(bin_string)
    return bin_string

# Funkcja rysująca GUI na podstawie ciągu binarnego
def generate_image(binary_string):
    window = tk.Tk()
    window.title("Hex to Binary Grid")

    grid_size = 16
    cell_size = 30
    
    for i in range(256):
        row = i // grid_size
        col = i % grid_size
        color = "green" if binary_string[i] == '1' else "white"
        
        canvas = tk.Canvas(window, width=cell_size*2, height=cell_size , highlightthickness=0)
        canvas.create_rectangle(1, 1, cell_size*2, cell_size, fill=color, outline=color)
        canvas.grid(row=row, column=col, padx=(0.1), pady=(0.1))
        
    window.mainloop()

def on_convert():
    hex_string = entry.get()
    bin_string = hex_to_bin(hex_string)
    img = generate_image(bin_string)
    img.show()

# Ustawienia GUI
root = tk.Tk()
root.title("Hex to Bin Image Converter")

# Etykieta i pole wprowadzania
label = ttk.Label(root, text="Podaj ciąg hex:")
label.pack()
entry = ttk.Entry(root)
entry.pack()

# Przycisk do konwersji
convert_button = ttk.Button(root, text="Konwertuj i pokaż obraz", command=on_convert)
convert_button.pack()

root.mainloop()
