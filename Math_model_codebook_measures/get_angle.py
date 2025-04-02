from math import acos, sqrt, cos, pi, degrees
from get_distances import UWB_module
import os
from time import sleep

class Antenna_Geometry():
    def __init__(self, Anchor: UWB_module, ris_dist): #RIS_DIST IN METERS
        self.Anchor = Anchor
        self.ris_dist = ris_dist*1000
        self.b = self.ris_dist
        self.half_of_b = self.ris_dist/2
        self.Anchor_dists = None
        self.Tag_dist = None
    
    def calc_alpha(self, a, c):
        ''' Alpha - kąt między RIS a A0-A1
            a == A0 do A1,
            c == A1 do A2        '''
        alpha_arg = (a**2 + self.b**2 -c**2)/(2*a*self.b)
        # print("alfa")
        return acos(alpha_arg)

    def calc_beta(self, x, y):
        ''' Beta kąt między RIS a A2-T
            x == A2 do T
            y == A0 do T        '''
        beta_arg = (x**2 + self.b**2 - y**2)/(2*x*self.b)
        # print("beta")
        return acos(beta_arg)
    
    def calc_m(self, x, b, beta):
        return sqrt(x**2 + b**2 - 2*x*b*cos(beta))
    
    def calc_n(self, a, b, alpha):
        return sqrt(a**2 + b**2 - 2*a*b*cos(alpha))
    
    def calc_theta(self, x, b, m):
        theta_arg = (m**2 + b**2 - x**2)/(2*m*b)
        # print("teta")
        return acos(theta_arg)
    
    def calc_omega(self, a, b, n):
        omega_arg = (n**2 + b**2 - a**2)/(2*n*b)
        # print("omega")
        return acos(omega_arg)
    
    def get_distances(self):
        self.Tag_dist, self.Anchor_dists = self.Anchor.get_distances()
        return
    
    def calc_triangle_side_opposite_angle(a, b, alpha):
        return sqrt(a**2 + b**2 - 2*a*b*cos(alpha))

    def calc_triangle_angle(a,b,c):
        arg = (a**2 + b**2 - c**2)/(2*a*b)
        return acos(arg)

    def get_angles(self, Print_vals = False):
        '''
        DISTANCES ARE IN mm BY DEFAULT
        ANGLES IN RADIANS        
        '''
        self.get_distances()
        a = self.Anchor_dists[1]
        c = self.Anchor_dists[3]
        y = self.Tag_dist[0]
        x = self.Tag_dist[2]
        alpha = self.calc_alpha(a=a, c=c)
        beta = self.calc_beta(x=x, y=y)
        m = self.calc_m(x=x, b=self.half_of_b, beta=beta)
        n = self.calc_n(a=a, b=self.half_of_b, alpha=alpha)
        theta = self.calc_theta(x=x, b=self.half_of_b, m=m)
        omega = self.calc_omega(a=a, b=self.half_of_b, n=n)
        Rx, Tx = degrees((pi/2) - theta), degrees((pi/2) - omega)*(-1)
        if Print_vals:
            print(f"Tx Dystance a = {a/1000} \nTx Dystance c = {c/1000} \nRx Dystance  x = {x/1000} \nRx Dystance  y = {y/1000}\nTx angle = {Tx} \nRx angle = {Rx}\n\n")
        return Rx, Tx, a, c, y, x, self.ris_dist
    


    

if __name__ == "__main__":
    uwb = UWB_module(no_of_lines=10)
    geo = Antenna_Geometry(uwb, 0.8425
                           )
    while True:
        try:
            geo.get_angles(Print_vals=True)
        except Exception as e:
            print(e)
        sleep(1)
        # if os.name == "nt":
        #     os.system("cls")
        # else:
        #     os.system("clear")
        

