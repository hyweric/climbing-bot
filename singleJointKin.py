import math

class offsetJointKinematics:
    def __init__(self, l1, l2, l4, l5, x4, y4): 
        self.l1 = l1
        self.l2 = l2
        self.l3 = None 
        self.l4 = l4
        self.l5 = l5
        self.p4 = (x4, y4)


    def pointThree(self, t1, t2):
        x2 = self.l1 * math.cos(math.radians(t1))
        y2 = self.l1 * math.sin(math.radians(t1))

        x3 = x2 + self.l2 * math.cos(math.radians(t2 + t1))
        y3 = y2 + self.l2 * math.sin(math.radians(t2 + t1))

        return (x2, y2), (x3, y3)
    
    def thetaThree(self, t1, t2):
        pointThree = self.pointThree(t1, t2)
        p3 = pointThree[1]
        l3 = math.dist(p3, self.p4)
        t3 = math.acos((self.l4**2 + l3**2 - self.l5**2) / (2 * self.l4 * l3))  
        t4 = math.acos((l3**2 + self.l5**2 - self.l4**2) / (2 * l3 * self.l5))  
        t5 = math.acos((self.l4**2 + self.l5**2 - l3**2) / (2 * self.l4 * self.l5)) 
        return t3, t4, t5

        

OJK1 = offsetJointKinematics(20, 10, 10, 20, 0, 5)
t1, t2 = 30, 110
print(OJK1.pointThree(t1, t2))
t3, t4, t5 = OJK1.thetaThree(t1, t2)

print(math.degrees(t3), math.degrees(t4), math.degrees(t5))