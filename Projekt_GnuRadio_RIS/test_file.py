from RIS import RIS
from time import sleep



if __name__ == "__main__":
    ris_0 = RIS(port = "/dev/ttyUSB0", id = 0)
    ris_0.set_pattern("0xFF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00")
    #sleep(1e-3)
    print(ris_0.read_pattern())
    #sleep(1e-3)
    ris_0.reset()
    #sleep(1e-3)
    ris_0.set_pattern("0x00007FFE40025FFA500A57EA542A55AA55AA542A57EA500A5FFA40027FFE0000")
    #sleep(1e-3)
    print(ris_0.read_pattern())
    exit(0)

