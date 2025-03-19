from periphery import GPIO
import time
#from tkinter import *

class Remote_Head:
    def __init__(self, CONFIG):
        self.step_resolution = CONFIG.step_resolution
        self.azimuth_step_time = CONFIG.azimuth_step_time
        self.elevation_step_time = CONFIG.elevation_step_time
        self.header_steps_az = CONFIG.header_steps_az
        self.header_steps_el = CONFIG.header_steps_el
        
        # Initialize GPIO pins

        #Kąt azymut-dolny silnik
        self.DIR_AZ_GPIO = GPIO(95, 'out')
        self.STEP_AZ_GPIO = GPIO(96, 'out')
        #Kąt elewacji-górny silnik 
        self.DIR_EL_GPIO = GPIO(115, 'out')
        self.STEP_EL_GPIO = GPIO(100, 'out')
         #Rozdzielczosc kroku
        self.MS1_GPIO = GPIO(98, 'out')
        self.MS2_GPIO = GPIO(102, 'out')
        self.MS3_GPIO = GPIO(101, 'out')

        # Set default values
        self.initialize()
        self.resolution(self.step_resolution)

    def __del__(self):
        self.DIR_AZ_GPIO.close()
        self.DIR_EL_GPIO.close()
        self.STEP_AZ_GPIO.close()
        self.STEP_EL_GPIO.close()
        self.MS1_GPIO.close()
        self.MS2_GPIO.close()
        self.MS3_GPIO.close()

    def initialize(self):
        self.DIR_AZ_GPIO.write(True)  # dir - left
        self.DIR_EL_GPIO.write(False)  # dir - up
        self.STEP_AZ_GPIO.write(False)
        self.STEP_EL_GPIO.write(False)
        self.MS1_GPIO.write(False)
        self.MS2_GPIO.write(False)
        self.MS3_GPIO.write(False)

    def resolution(self, step_resolution):
        self.step_resolution = step_resolution
        if step_resolution == 1:
            self.MS1_GPIO.write(False)
            self.MS2_GPIO.write(False)
            self.MS3_GPIO.write(False)
            print("Dokładność ustawiona na 1.8 stopnia.")
        elif step_resolution == 2:
            self.MS1_GPIO.write(True)
            self.MS2_GPIO.write(False)
            self.MS3_GPIO.write(False)
            print("Dokładność ustawiona na 0.9 stopnia")
        elif step_resolution == 4:
            self.MS1_GPIO.write(False)
            self.MS2_GPIO.write(True)
            self.MS3_GPIO.write(False)
            print("Dokładność ustawiona na 0.45 stopnia")
        elif step_resolution == 8:
            self.MS1_GPIO.write(True)
            self.MS2_GPIO.write(True)
            self.MS3_GPIO.write(False)
            print("Dokładność ustawiona na 0.225 stopnia")
        elif step_resolution == 16:
            self.MS1_GPIO.write(True)
            self.MS2_GPIO.write(True)
            self.MS3_GPIO.write(True)
            print("Dokładność ustawiona na 0.1125 stopnia")
        else:
            self.MS1_GPIO.write(False)
            self.MS2_GPIO.write(False)
            self.MS3_GPIO.write(False)

    def az360(self): #kalibracja w azymucie
        self.DIR_AZ_GPIO.write(True)  # left
        for _ in range(200):
            self.STEP_AZ_GPIO.write(True)
            time.sleep(self.azimuth_step_time)
            self.STEP_AZ_GPIO.write(False)
            time.sleep(self.azimuth_step_time)
        input("Kliknij enter aby wrócić do startowej pozycji.")
        self.DIR_AZ_GPIO.write(False)  # right
        for _ in range(200):
            self.STEP_AZ_GPIO.write(True)
            time.sleep(self.azimuth_step_time)
            self.STEP_AZ_GPIO.write(False)
            time.sleep(self.azimuth_step_time)
        self.DIR_AZ_GPIO.write(True)  # left
        print("System w pozycji startowej.")

    def el360(self): #kalibracja elewacji
        self.DIR_EL_GPIO.write(False)  # up
        for _ in range(200):
            self.STEP_EL_GPIO.write(True)
            time.sleep(self.elevation_step_time)
            self.STEP_EL_GPIO.write(False)
            time.sleep(self.elevation_step_time)
        input("Kliknij enter aby wrócić do startowej pozycji.")
        self.DIR_EL_GPIO.write(True)  # down
        for _ in range(200):
            self.STEP_EL_GPIO.write(True)
            time.sleep(self.elevation_step_time)
            self.STEP_EL_GPIO.write(False)
            time.sleep(self.elevation_step_time)
        self.DIR_EL_GPIO.write(False)  # up
        print("System w pozycji startowej.")

    def step_up_down(self):
        self.STEP_EL_GPIO.write(True)
        time.sleep(self.elevation_step_time)
        self.STEP_EL_GPIO.write(False)
        time.sleep(self.elevation_step_time)

    def step_left_right(self):
        self.STEP_AZ_GPIO.write(True)
        time.sleep(self.azimuth_step_time)
        self.STEP_AZ_GPIO.write(False)
        time.sleep(self.azimuth_step_time)

    def rotate_left(self, step_number = None):
        if step_number == None:
            step_number = self.header_steps_az
        print("[Obrót w lewo o]: " + str(step_number * (1 / self.step_resolution) * 1.8))
        self.DIR_AZ_GPIO.write(False)  # left
        for _ in range(step_number):
            self.step_left_right()

    def rotate_right(self, step_number = None):
        if step_number == None:
            step_number = self.header_steps_az
        print("[Obrót w prawo o]: " + str(step_number * (1 / self.step_resolution) * 1.8))
        self.DIR_AZ_GPIO.write(True)  # right
        for _ in range(step_number):
            self.step_left_right()

    def rotate_down(self, step_number = None):
        if step_number == None:
            step_number = self.header_steps_az
        print("[Obrót w dół o]: " + str(step_number * (1 / self.step_resolution) * 1.8))
        self.DIR_EL_GPIO.write(False)  # up
        for _ in range(step_number):
            self.step_up_down()

    def rotate_up(self, step_number = None):
        if step_number == None:
            step_number = self.header_steps_az
        print("[Obrót w górę o]: " + str(step_number * (1 / self.step_resolution) * 1.8))
        self.DIR_EL_GPIO.write(True)  # down
        for _ in range(step_number):
            self.step_up_down

    def steering_command(self, command):
        if command=='l':
            self.rotate_left(self.header_steps_az)
        elif command=='r':
            self.rotate_right(self.header_steps_az)
        elif command=='u':
            self.rotate_up(self.header_steps_el)
        elif command=='d':
            self.rotate_down(self.header_steps_el)
        else:
            print("Błędny lub brak argumentu (cmd == )" + str(command))