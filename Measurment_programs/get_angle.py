from math import acos, sqrt, cos, pi, degrees
from get_distances import UWB_module_DWM1001
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


def angle_from_distances(a, b, c, degrees=True):
    """
    calculate ab angle from distances of triangle sides
    a,b,c
    """
    print(a,b,c)
    print(type(a), type(b), type(c))
    cos_theta = (a**2 + b**2 - c**2)/(2*a*b)    
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
    def __init__(self, tag, tx_id=None, ris_id=None, a1_id=None, a2_id=None, a3_id=None, lines_treshold=100, n_sigma=3, stat_mode="mean"):
        """
        Init, takes:
        tag, tx_id, ris_id, a1_id, a2_id

        lines_treshold: how many lines to collect to make stat function
        stat modes: 'mean', 'median'
        n_sigma: how much outliers is to delete
        """
        #Init TAG device
        self.tag = tag
        #Init ID of devices
        self.tx_id = tx_id
        self.ris_id = ris_id
        self.a1_id = a1_id
        self.a2_id = a2_id
        self.a3_id = a3_id
        #Parameters ()
        self.lines_treshold = lines_treshold
        self.n_sigma = n_sigma
        self.stat_mode = stat_mode
        #prepare list to measures
        self.prep_measures()

    def prep_measures(self, a=[],b=[],c=[],d=[],e=[],f=[],g=[],h=[]):
        #Init localisation [X,Y,Z] of devices
        # self.loc_a1 =  []
        # self.loc_a2 =  []
        # self.loc_a3 =  []
        # self.loc_tx =  []
        # self.loc_ris = []
        # self.loc_tag = []
        #Init distances (see UWB_draft.png)
        self.a = a
        # self.b = []
        self.c = c
        self.d = d
        self.e = e
        # self.f = []
        self.g = g
        self.h = h
        #Init angles (see UWB_draft.png)
        self.Tx = None
        self.Rx = None

    def print_values(self):
        # print("A1:    ", self.loc_a1)
        # print("A2:    ", self.loc_a2)
        # print("TX:    ", self.loc_tx)
        # print("RIS:   ", self.loc_ris)
        # print("RX_tag:", self.loc_tag)
        print("a_mean", np.mean(self.a))
        print("b_mean", np.mean(self.b))
        print("c_mean", np.mean(self.c))
        print("d_mean", np.mean(self.d))
        print("e_mean", np.mean(self.e))
        print("f_mean", np.mean(self.f))
        print("Tx_angle: ", self.Tx)
        print("Rx_angle: ", self.Rx)
        return

    def calc_distances(self):
        '''
        calculate distances of devices from last locations and append them to store
        '''
        #dist = np.linalg.norm(a-b)
        # self.a.append(np.linalg.norm(self.loc_a1[-1]  - self.loc_ris[-1]))
        # self.b.append(np.linalg.norm(self.loc_ris[-1] - self.loc_a2[-1]))
        # self.c.append(np.linalg.norm(self.loc_ris[-1] - self.loc_tx[-1]))
        # self.d.append(np.linalg.norm(self.loc_ris[-1] - self.loc_tag[-1]))
        # self.e.append(np.linalg.norm(self.loc_a1[-1]  - self.loc_tx[-1]))
        # self.f.append(np.linalg.norm(self.loc_a2[-1]  - self.loc_tag[-1]))
        # self.g.append(np.linalg.norm(self.loc_a3[-1]  - self.loc_tag[-1]))
        # self.h.append(np.linalg.norm(self.loc_ris[-1] - self.loc_a3[-1]))
        return

    def mean_sigma(self, vals, ddof=0):
        """
        Metoda klasy. Używa self.n_sigma (float) i self.stat_mode ('mean' lub 'median').
        vals: lista lub array 1D (N,) albo 2D (N,D).
        ddof: dla std (0 populacyjne, 1 estymator próbki).
        Zwraca: (stat_kept) - stat_kept: skalar dla 1D, array(D,) dla ND;
        """
        arr = np.asarray(vals, dtype=float)
        if arr.size == 0:
            if arr.ndim <= 1:
                return np.nan, np.array([], dtype=bool)
            return np.full((arr.shape[1],), np.nan), np.array([], dtype=bool)

        # normy: dla 1D używamy wartości, dla ND norma wektorów
        norms = arr if arr.ndim == 1 else np.linalg.norm(arr, axis=1)

        mu = norms.mean()
        sigma = norms.std(ddof=ddof)

        if sigma == 0:
            mask = np.ones(len(norms), dtype=bool)
        else:
            mask = np.abs(norms - mu) <= (self.n_sigma * sigma)

        if not mask.any():
            # brak zachowanych punktów -> NaN odpowiedniego kształtu
            if arr.ndim == 1:
                return np.nan, mask
            return np.full((arr.shape[1],), np.nan), mask

        kept = arr[mask]
        if self.stat_mode == 'median':
            if arr.ndim == 1:
                stat_kept = np.median(kept)
            else:
                stat_kept = np.median(kept, axis=0)
        else:  # domyślnie 'mean'
            if arr.ndim == 1:
                stat_kept = kept.mean()
            else:
                stat_kept = kept.mean(axis=0)

        return stat_kept


    def calc_angles(self, degrees=True):
        '''
        calculate angles of tx and rx to tag from locations
        '''
        self.alfa = -1 * (90 - angle_from_distances(self.mean_sigma(self.c), self.mean_sigma(self.a), self.mean_sigma(self.e)))
        self.beta = angle_from_distances(self.mean_sigma(self.h), self.mean_sigma(self.d), self.mean_sigma(self.g))
        return

    def mes_angles(self):
        """
        function does and invoke all logic to get angles and distaces of devices
        """
        while True:
            parsed_line = (self.tag.parse_line(self.a3_id, self.ris_id))
            try:
                parsed_line = np.array(parsed_line)
                #print(parsed_line)
            except:
                #print("line skipped")
                continue
            #print(parsed_line, "\n LEN OF LINE = ",len(parsed_line))
            if len(parsed_line)<2 :
                #print("line skipped") 
                continue
            else:
                self.d.append(parsed_line[1])
                self.g.append(parsed_line[0])
                self.calc_distances()        
            return

    # def calc_angles_one_triangle_set(l_ris, l_a1, l_tx, l_tag, l_a3):
    #     self.beta = angle_from_points(l_ris, l_tag, l_a3)
    #     self.alfa = angle_from_points(l_ris, l_a1, l_tx)

    def get_angles(self, Print_vals=False, a=[],b=[],c=[],d=[],e=[],f=[],g=[],h=[]):
        self.prep_measures(a,b,c,d,e,f,g,h)
        i = 0
        while i< self.lines_treshold:

            self.mes_angles()
            #print(i)
            i+=1  
        #get mean locs
        # l_ris = self.mean_sigma(self.loc_ris)
        # l_a1 = self.mean_sigma(self.loc_a1)
        # l_tx = self.mean_sigma(self.loc_tx)
        # l_a2 = self.mean_sigma(self.loc_a2)
        # l_tag = self.mean_sigma(self.loc_tag)    
        # l_a3 = self.mean_sigma(self.loc_a3)
        self.calc_angles()
        # self.calc_angles_one_triangle_set(l_ris, l_a1, l_tx, l_tag, la3)
        a = self.mean_sigma(self.a)
        # b = self.mean_sigma(self.b)
        c = self.mean_sigma(self.c)
        d = self.mean_sigma(self.d)
        e = self.mean_sigma(self.e)
        # f = self.mean_sigma(self.f)
        g = self.mean_sigma(self.g)
        h = self.mean_sigma(self.h)
        if Print_vals:
            self.print_values()
        
        return self.alfa, self.beta, a, c, d, e, g, h
        #return self.alfa, self.beta, self.a, self.b, self.c, self.d, self.e, self.f

if __name__ == "__main__":
    uwb = UWB_module_DWM1001()
    #ID order: tx,ris,a1,a2
    #devices_ids = ["0F83", "D599", "870B", "4F96", "2D15", "9D15"]
    geo = Antenna_Geometry_MDEK1001(uwb, a3_id="9D15", ris_id="D599")
    geo.lines_treshold = 100
    geo.n_sigma = 2
    geo.stat_mode = 'mean'
    i = 0
    while True:
        try:
            res = geo.get_angles(Print_vals=False, a=[5], c=[4], e=[3], h=[4.4])
            print(f"POMIAR {i}, \n {res}")
        except Exception as e:
            print(e)
        sleep(1)
        # if os.name == "nt":
        #     os.system("cls")
        # else:
        #     os.system("clear")
        

