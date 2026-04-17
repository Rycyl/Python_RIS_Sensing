def funkcja_do_wykonania(arg):
    print(f"Funkcja została wykonana z argumentem: {arg}")

def funkcja_przekazujaca(funkcja, arg):
    print("Rozpoczynam wykonanie funkcji...")
    funkcja(arg)  # Wywołanie przekazanej funkcji z argumentem
    print("Zakończono wykonanie funkcji.")

# Przekazanie funkcji_do_wykonania jako argument z dodatkowym argumentem
funkcja_przekazujaca(funkcja_do_wykonania, "Hello, World!")