from remote_head import Remote_Head
from config_obj import Config


if __name__ == "__main__":
    Config = Config()
    r_h = Remote_Head(Config)
    r_h.resolution(2)
    r_h.rotate_left(10)
    r_h.rotate_right(10)
    r_h.rotate_right(10)
    r_h.rotate_left(10)
    print("Done")
    exit()
