import math 

def inverseKinematics(x, y, len1, len2):
    y = -y # temp fix since leg is facing down
    temp = (x ** 2 + y ** 2 - len1 ** 2 - len2 ** 2) / (2 * len1 * len2)
    if -1 <= temp <= 1:
        a = math.acos(temp)
        angle2 = math.pi - a
        b = math.acos((len1 ** 2 + x ** 2 + y ** 2 - len2 ** 2) / (2 * len1 * math.sqrt(x ** 2 + y ** 2)))
        angle1 = -(math.atan2(y, x) - b)
        return angle1, angle2
    else:
        return "No solution"

class offsetJointKinematics:
    def __init__(self, l1, l2, l4, l5, l8, x4, y4, t1, t2): 
        self.t1 = t1
        self.t2 = t2
        self.l1 = l1
        self.l2 = l2
        self.l3 = None 
        self.l4 = l4
        self.l5 = l5
        self.l6 = math.dist((0, 0), (x4, y4))
        self.l8 = l8  
        
        self.p1 = (0, 0)
        self.p2 = self.getP2()
        self.p3 = self.getP3()
        self.p4 = (x4, y4)
        self.p5 = (self.p4[0] - l4 * math.sin(self.getThetaFive()), self.p4[1] + l4 * math.cos(self.getThetaFive()))
        self.p6 = self.getP6()
    
    def getL7(self):
        return math.dist(self.getP2(), self.p4)
    
    def lawOfCosines(self, a, b, c):
        return math.acos((a**2 + b**2 - c**2) / (2 * a * b))
    
    def getP2(self):
        x2 = self.l1 * math.cos(math.radians(self.t1))
        y2 = self.l1 * math.sin(math.radians(self.t1))
        return x2, y2

    def getP3(self):
        x2, y2 = self.getP2()
        x3 = x2 + self.l2 * math.cos(math.radians(self.t2 + self.t1))
        y3 = y2 + self.l2 * math.sin(math.radians(self.t2 + self.t1))
        return (x3, y3)

    def getP6(self):
        x2, y2 = self.getP2()
        x6 = x2 - self.l8 * math.cos(math.radians(self.t2 + self.t1))
        y6 = y2 - self.l8 * math.sin(math.radians(self.t2 + self.t1))
        return (x6, y6)
    
    def getthetaFour(self):
        p3 = self.getP3()
        l3 = math.dist(p3, self.p4)
        l7 = self.getL7()
        Q4partComplementBottom = self.lawOfCosines(self.l6, l7, self.l1)
        Q4partComplementTop = self.lawOfCosines(l3, l7, self.l2)
        q4 = math.pi - (Q4partComplementBottom + Q4partComplementTop)
        return q4

    def getThetaThree(self):
        p3 = self.getP3()
        l3 = math.dist(p3, self.p4)
        t3 = math.acos((self.l4**2 + l3**2 - self.l5**2) / (2 * self.l4 * l3))  
        return t3

    def getThetaFive(self):
        q3 = self.getThetaThree()
        q4 = self.getthetaFour()
        q5 = q3 - q4
        return q5
        
    def update(self, t1, t2):
        self.t1 = t1
        self.t2 = t2
        self.p2 = self.getP2()
        self.p3 = self.getP3()
