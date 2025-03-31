from math import acos, sqrt, cos, pi, degrees
from get_distances import UWB_module

class Antenna_Geometry():
    def __init__(self, Anchor: UWB_module, ris_dist):
        self.Anchor = Anchor
        self.ris_dist = ris_dist
        self.Anchor_dists = None
        self.Tag_dist = None
    
    def calc_alpha(self, a, c):
        '''Alpha czyli kąt między RIS a dystansem od Anchora 0 do Anchora 1
        a to właśnie dsystans A0 do A1, a c to dystans A1 do A2'''
        b = self.ris_dist
        alpha_arg = (a**2 + b**2 -c**2)/(2*a*b)
        return acos(alpha_arg)

    def calc_beta(self, x, y):
        '''Beta czyli kąt między RIS a odcinkiem A2 do T (czyli x) y to odcinek A0 do T'''
        b = self.ris_dist
        beta_arg = (x**2 + b**2 - y**2)/(2*x*b)
        return acos(beta_arg)
    
    def calc_gamma(self, x, b, beta):
        return sqrt(x**2 + b**2 - 2*x*b*cos(beta))
    
    def calc_kappa(self, a, b, alpha):
        return sqrt(a**2 + b**2 - 2*a*b*cos(alpha))
    
    def calc_theta(self, x, b, gamma):
        theta_arg = (gamma**2 + b**2 - x**2)/(2*gamma*b)
        return acos(theta_arg)
    
    def calc_omega(self, a, b, kappa):
        omega_arg = (kappa**2 + b**2 - a**2)/(2*kappa*b)
        return acos(omega_arg)
    
    def get_distances(self):
        self.Tag_dist, self.Anchor_dists = self.Anchor.get_distances()
        return
    
    def get_angles(self):
        self.get_distances()
        half_of_b = self.ris_dist/2
        a = self.Anchor_dists[1]
        c = self.Anchor_dists[3]
        y = self.Tag_dist[0]
        x = self.Tag_dist[2]
        alpha = self.calc_alpha(a, c)
        beta = self.calc_beta(x, y)
        gamma = self.calc_gamma(x, half_of_b, beta)
        kappa = self.calc_kappa(a, half_of_b, alpha)
        theta = self.calc_theta(x, half_of_b, gamma)
        omega = self.calc_omega(a, half_of_b, kappa)
        return degrees((pi/2) - theta), ((pi/2) - omega)


# class Antenna_Geometry():
#     def __init__(self, Anchor_1: UWB_module, Anchor_2: UWB_module, ris_dist, no_of_tags = 2):
#         self.Anchor_1 = Anchor_1
#         self.Anchor_2 = Anchor_2
#         self.ris_dist = ris_dist
#         self.no_of_tags = 2

#     def calc_alpha(self, a, d):
#         #d^2 = a^2 + b^2 - 2*a*b*cos(alpha)
#         #2*a*b*cos(alpha) = a^2 + b^2 - d^2 -> cos(alpha) = (a^2 + b^2 - d^2)/2ab
#         b = self.ris_dist
#         alpha_arg = (a**2 + b**2 - d**2)/(2*a*b)
#         return acos(alpha_arg)
    
#     def calc_c(self, a, alpha):
#         b = self.ris_dist/2
#         #c^2 = a^2 + b^2 - a*b*cos(alpha)
#         c = sqrt(a**2 + b**2 - a*b*cos(alpha))
#         return c

#     def calc_beta(self, c, d):
#         b = self.ris_dist/2
#         # d^2 = b^2 + c^2 - 2*b*d*cos(beta) -> 2*b*d*cos(beta) = b^2 + c^2 - d^2
#         # cos(beta) = (b^2 + c^2 - d^2)/2*b*d
#         beta_arg = (b**2 + c**2 - d**2)/(2*b*d)
#         return acos(beta_arg)

#     def calc_angle(self):
#         Anchor_1_dist = input("distance 1 ")#self.Anchor_1.get_distances()[:2]
#         Anchor_2_dist = input("distance 2 ") #self.Anchor_2.get_distances()[:2]
#         a = float(Anchor_1_dist)#[0]
#         d = float(Anchor_2_dist)#[1]
#         alpha = self.calc_alpha(a, d)
#         print(degrees(alpha))
#         c = self.calc_c(a, alpha)
#         beta = self.calc_beta(c, d)
#         gamma = pi/2 - pi - beta
#         return gamma
    

if __name__ == "__main__":
    a = Antenna_Geometry(None, None, 0.3)
    print(degrees(a.calc_angle()))

