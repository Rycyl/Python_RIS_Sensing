import numpy as np

def kat(a, b, c, degree=True):
    """
    Zwraca kąt między bokami a i b (kąt przy wierzchołku naprzeciw boku c).
    a, b, c: długości boków trojkata (liczby dodatnie)
    degree: jeśli True — wynik w stopniach; jeśli False — w radianach
    """
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    c = np.asarray(c, dtype=float)

    # Walidacja: dodatnie długości i spełnienie nierówności trójkąta
    if np.any(a <= 0) or np.any(b <= 0) or np.any(c <= 0):
        raise ValueError("Wszystkie boki muszą być > 0")
    if np.any(a + b <= c) or np.any(a + c <= b) or np.any(b + c <= a):
        raise ValueError("Podane długości nie tworzą trójkąta")

    # Twierdzenie cosinusów: cos(gamma) = (a^2 + b^2 - c^2) / (2ab)
    cos_gamma = (a**2 + b**2 - c**2) / (2 * a * b)
    # Zaokrąglenie do zakresu [-1, 1] by uniknąć błędów numerycznych
    cos_gamma = np.clip(cos_gamma, -1.0, 1.0)

    gamma = np.acos(cos_gamma)  # w radianach
    if degree:
        return np.degrees(gamma)
    return gamma
if __name__=="__main__":
    while(True):
        print("KAT AB z tw cos")
        a = input("A:")
        b = input("B:")
        c = input("C:")
        print("AB angle = ", kat(a,b,c))