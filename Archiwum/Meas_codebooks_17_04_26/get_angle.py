from math import acos, sqrt, cos, pi, degrees
from get_distances import New_UWB_module
import os
import re
import numpy as np
import serial
from time import sleep

def angle_from_points(a, b, c, degrees=True):
    """
    calculate BAC angle from coordinates of points
    a,b,c = np.array([x,y,z])
    """
    ab = b - a
    ac = c - a
    
    cos_theta = np.dot(ab, ac) / (np.linalg.norm(ab) * np.linalg.norm(ac))
    cos_theta = np.clip(cos_theta, -1.0, 1.0)  # stabilność numeryczna
    
    theta = np.arccos(cos_theta)
    
    if degrees:
        return np.degrees(theta)
    return theta

# class Antenna_Geometry():
#     def __init__(self, Anchor: UWB_module, ris_dist): #RIS_DIST IN METERS
#         self.Anchor = Anchor
#         self.ris_dist = ris_dist*1000
#         self.b = self.ris_dist
#         self.half_of_b = self.ris_dist/2
#         self.Anchor_dists = None
#         self.Tag_dist = None
    
#     def calc_alpha(self, a, c):
#         ''' Alpha - kąt między RIS a A0-A1
#             a == A0 do A1,
#             c == A1 do A2        '''
#         alpha_arg = (a**2 + self.b**2 -c**2)/(2*a*self.b)
#         # print("alfa")
#         #print(f"Alpha arg:: {alpha_arg}")
#         return acos(alpha_arg)

#     def calc_beta(self, x, y):
#         ''' Beta kąt między RIS a A2-T
#             x == A2 do T
#             y == A0 do T        '''
#         beta_arg = (x**2 + self.b**2 - y**2)/(2*x*self.b)
#         # print("beta")
#         #print(f"Beta arg:: {beta_arg}")
#         return acos(beta_arg)
    
#     def calc_m(self, x, b, beta):
#         return sqrt(x**2 + b**2 - 2*x*b*cos(beta))
    
#     def calc_n(self, a, b, alpha):
#         return sqrt(a**2 + b**2 - 2*a*b*cos(alpha))
    
#     def calc_theta(self, x, b, m):
#         theta_arg = (m**2 + b**2 - x**2)/(2*m*b)
#         # print("teta")
#         #print(f"theta_arg:: {theta_arg}")
#         return acos(theta_arg)
    
#     def calc_omega(self, a, b, n):
#         omega_arg = (n**2 + b**2 - a**2)/(2*n*b)
#         # print("omega")
#         #print(f"Omega_arg:: {omega_arg}")
#         return acos(omega_arg)
    
#     def get_distances(self):
#         self.Tag_dist, self.Anchor_dists = self.Anchor.get_distances()
#         return
    
#     def calc_triangle_side_opposite_angle(a, b, alpha):
#         return sqrt(a**2 + b**2 - 2*a*b*cos(alpha))

#     def calc_triangle_angle(a,b,c):
#         arg = (a**2 + b**2 - c**2)/(2*a*b)
#         #print(f"ARG:: {arg}")
#         return acos(arg)

#     def get_angles(self, Print_vals = False):
#         '''
#         DISTANCES ARE IN mm BY DEFAULT
#         ANGLES IN RADIANS        
#         '''
#         self.get_distances()
#         a = self.Anchor_dists[1]
#         c = self.Anchor_dists[3]
#         y = self.Tag_dist[0]
#         x = self.Tag_dist[2]
#         alpha = self.calc_alpha(a=a, c=c)
#         beta = self.calc_beta(x=x, y=y)
#         m = self.calc_m(x=x, b=self.half_of_b, beta=beta)
#         n = self.calc_n(a=a, b=self.half_of_b, alpha=alpha)
#         theta = self.calc_theta(x=x, b=self.half_of_b, m=m)
#         omega = self.calc_omega(a=a, b=self.half_of_b, n=n)
#         Rx, Tx = degrees((pi/2) - theta), degrees((pi/2) - omega)*(-1)
#         if Print_vals:
#             print(f"Tx Dystance a = {a/1000} \nTx Dystance c = {c/1000} \nRx Dystance  x = {x/1000} \nRx Dystance  y = {y/1000}\nTx angle = {Tx} \nRx angle = {Rx}\n\n")
#         return Rx, Tx, a, c, y, x, self.ris_dist
    
# class Antenna_Geometry_dummy():
#     def __init__(self, Anchor: str, ris_dist):
#         self.ris_dist = ris_dist

#     def get_angles(self, Print_vals = False):
#         Rx = -48
#         Tx = 80
#         a = 3000
#         c = 2000
#         y = 1000
#         x = 500
#         return Rx, Tx, a, c, y, x, self.ris_dist

class Antenna_Geometry_MDEK1001():
    def __init__(self, tag, tx_id, ris_id, a1_id, a2_id):
        """
        Init, takes:
        tag, tx_id, ris_id, a1_id, a2_id
        """
        #Init TAG device
        self.tag = tag
        #Init ID of devices
        self.tx_id = tx_id
        self.ris_id = ris_id
        self.a1_id = a1_id
        self.a2_id = a2_id
        #Init localisation [X,Y] of devices
        self.loc_a1 = None
        self.loc_a2 = None
        self.loc_tx = None
        self.loc_ris = None
        self.loc_tag = None
        #Init distances (see UWB_draft.png)
        self.a = None
        self.b = None
        self.c = None
        self.d = None
        self.e = None
        self.f = None
        #Init angles (see UWB_draft.png)
        self.alfa = None
        self.beta = None

    def print_values(self):
        print("A1:    ", self.loc_a1)
        print("A2:    ", self.loc_a2)
        print("TX:    ", self.loc_tx)
        print("RIS:   ", self.loc_ris)
        print("RX_tag:", self.loc_tag)
        print("a", self.a)
        print("b", self.b)
        print("c", self.c)
        print("d", self.d)
        print("e", self.e)
        print("f", self.f)
        return

    def calc_distances(self):
        '''
        calculate distances of devices from locations
        '''
        #dist = np.linalg.norm(a-b)
        self.a = np.linalg.norm(self.loc_a1 - self.loc_ris)
        self.b = np.linalg.norm(self.loc_ris - self.loc_a2)
        self.c = np.linalg.norm(self.loc_ris - self.loc_tx)
        self.d = np.linalg.norm(self.loc_ris - self.loc_tag)
        self.e = np.linalg.norm(self.loc_a1 - self.loc_tx)
        self.f = np.linalg.norm(self.loc_a2 - self.loc_tag)
        return

    def calc_angles(self, degrees=True):
        '''
        calculate angles of tx and rx to tag from locations
        '''
        self.alfa = angle_from_points(self.loc_ris, self.loc_a1, self.loc_tx)
        self.beta = angle_from_points(self.loc_ris, self.loc_a2, self.loc_tag)
        return

    def get_angles(self, Print_vals=False):
        """
        function does and invoke all logic to get angles and distaces of devices
        """
        while True:
            #!!return only one localisation in one program run!!
            line = self.tag.read_line(save_to_file=False)
            self.loc_a1, self.loc_a2, self.loc_ris, self.loc_tx, self.loc_tag = \
                self.tag.parse_line(line, self.a1_id, self.a2_id, self.ris_id, self.tx_id)

            if (self.loc_tag.all()):
                print(self.loc_tag)
                print(type(self.loc_tag))
                break

            if Print_vals:
                self.print_values()

        self.calc_distances()
        self.calc_angles()
        if Print_vals:
            self.print_values()
        return self.alfa, self.beta, self.a, self.b, self.c, self.d, self.e, self.f

if __name__ == "__main__":
    uwb = New_UWB_module()
    #ID order: tx,ris,a1,a2
    devices_ids = ["0F83", "D599", "870B", "4F96"]
    geo = Antenna_Geometry_MDEK1001(uwb, *devices_ids)
    while True:
        try:
            angle = geo.get_angles(Print_vals=True)
            print(angle)
        except Exception as e:
            print(e)
        sleep(1)
        # if os.name == "nt":
        #     os.system("cls")
        # else:
        #     os.system("clear")
        

