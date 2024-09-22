# Doesn't really need to be it's own class but easier to keep track of

import math

class legEquations:
    def sin_step(self, x):
        return (70/2) * math.sin(2 * math.pi / 140 * x + math.pi/2) - 135

    def semi_circle(self, x):
        return math.sqrt(70**2 - x**2) - 170

    def flat_line(self, x):
        return -170

    def upstep(self, x):
        return 1000 * (x + 70) - 170    