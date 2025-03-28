from math import acos, sqrt, cos, pi
from get_distances import UWB_module


class Antenna_Geometry():
    def __init__(self, Anchor_1: UWB_module, Anchor_2: UWB_module, ris_dist, no_of_tags = 2):
        self.Anchor_1 = Anchor_1
        self.Anchor_2 = Anchor_2
        self.ris_dist = ris_dist
        self.no_of_tags = 2

    def calc_alpha(self, a, d):
        #d^2 = a^2 + b^2 - 2*a*b*cos(alpha)
        #2*a*b*cos(alpha) = a^2 + b^2 - d^2 -> cos(alpha) = (a^2 + b^2 - d^2)/2ab
        b = self.ris_dist
        alpha_arg = (a**2 + b**2 - d**2)/2*a*b
        return acos(alpha_arg)
    
    def calc_c(self, a, alpha):
        b = self.ris_dist/2
        #c^2 = a^2 + b^2 - a*b*cos(alpha)
        c = sqrt(a**2 + b**2 - a*b*cos(alpha))
        return c

    def calc_beta(self, c, d):
        b = self.ris_dist/2
        # d^2 = b^2 + c^2 - 2*b*d*cos(beta) -> 2*b*d*cos(beta) = b^2 + c^2 - d^2
        # cos(beta) = (b^2 + c^2 - d^2)/2*b*d
        beta_arg = (b**2 + c**2 - d**2)/2*b*d
        return acos(beta_arg)

    def calc_angle(self):
        Anchor_1_dist = self.Anchor_1.get_distances()[:2]
        Anchor_2_dist = self.Anchor_2.get_distances()[:2]
        a = Anchor_1_dist[0]
        d = Anchor_2_dist[1]
        alpha = self.calc_alpha(a, d)
        c = self.calc_c(a, alpha)
        beta = self.calc_beta(c, d)
        gamma = pi/2 - pi - beta
        return gamma

