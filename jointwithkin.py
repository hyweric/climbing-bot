import math
import matplotlib.pyplot as plt
import time 

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
        # C is the angle opposite to side c and the angle we want to find
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
        p3= self.getP3()
        l3 = math.dist(p3, self.p4)
        l7 = self.getL7()
        Q4partComplementBottom = self.lawOfCosines(self.l6, l7, self.l1)
        Q4partComplementTop = self.lawOfCosines(l3, l7, self.l2)
        q4 = math.pi - (Q4partComplementBottom + Q4partComplementTop)
        return q4

    def getThetaThree(self):
        p3 = self.getP3()
        l3 = math.dist(p3, self.p4) # Q3 
        t3 = math.acos((self.l4**2 + l3**2 - self.l5**2) / (2 * self.l4 * l3))  
        arb4 = math.acos((l3**2 + self.l5**2 - self.l4**2) / (2 * l3 * self.l5))  # unimportant other angle
        arb5 = math.acos((self.l4**2 + self.l5**2 - l3**2) / (2 * self.l4 * self.l5)) # unimportant other angle
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

def inverseKinematics(x, y, len1, len2):
    temp = (x ** 2 + y ** 2 - len1 ** 2 - len2 ** 2) / (2 * len1 * len2)

    if -1 <= temp <= 1:
        a = math.acos(temp)
        angle2 = math.pi - a
        b = math.acos((len1 ** 2 + x ** 2 + y ** 2 - len2 ** 2) / (2 * len1 * math.sqrt(x ** 2 + y ** 2)))
        angle1 = -(math.atan2(y, x) - b) # try neg for reflection
        return angle1, angle2
    
class Plot:
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.points = {}
        self.lines = []

    def add_or_update_point(self, identifier, x, y):
        if identifier in self.points:
            self.points[identifier].set_data(x, y)
        else:
            self.points[identifier], = self.ax.plot(x, y, 'o', label=identifier)

    def add_line(self, point1_id, point2_id):
        if point1_id in self.points and point2_id in self.points:
            point1 = self.points[point1_id].get_data()
            point2 = self.points[point2_id].get_data()
            line, = self.ax.plot([point1[0], point2[0]], [point1[1], point2[1]], 'r-')
            self.lines.append(line)

    def show(self):
        self.ax.legend()
        plt.show()

while True:
    (x, y) = input("Enter the x and y coordinates of the end effector: ").split(',')
    (x, y) = (int(x), int(y))

    # Leg Lengths
    upperLeg = 23 
    lowerLeg = 15

    t1, t2 = inverseKinematics(x, y, upperLeg, lowerLeg)
    print("Theta 1: ", math.degrees(t1), "Theta 2: ", math.degrees(t2))
    # OJK1otherprogram = offsetJointKinematics(23, 10, 10, 18, 0, 5, 30, 50)
    # other = def __init__(self, l1, l2, l4, l5, x4, y4, t1, t2): 

    OJK1 = offsetJointKinematics(upperLeg, 10, 10, 18, lowerLeg, 0, 5, math.degrees(t1), math.degrees(t2))
    # this def __init__(self, l1, l2, l4, l5, l7, x4, y4, t1, t2): 

    print("Theta 3: ", math.degrees(OJK1.getThetaThree()))
    print("Theta 4: ", math.degrees(OJK1.getthetaFour()))
    print("Theta 5: ", math.degrees(OJK1.getThetaFive()))

    print('p1:', OJK1.p1)
    print('p2:', OJK1.p2)
    print('p3:', OJK1.p3)
    print('p4:', OJK1.p4)
    print('p5:', OJK1.p5)

    plot = Plot()
    plot.add_or_update_point('p1', OJK1.p1[0], OJK1.p1[1])
    plot.add_or_update_point('p2', OJK1.p2[0], OJK1.p2[1])
    plot.add_or_update_point('p3', OJK1.p3[0], OJK1.p3[1])
    plot.add_or_update_point('p4', OJK1.p4[0], OJK1.p4[1])
    plot.add_or_update_point('p5', OJK1.p5[0], OJK1.p5[1])
    plot.add_or_update_point('p6', OJK1.p6[0], OJK1.p6[1])
    plot.add_or_update_point('endpoint', x, y)
    plot.add_line('p1', 'p2')
    plot.add_line('p2', 'p3')
    plot.add_line('p1', 'p4')
    plot.add_line('p4', 'p5')
    plot.add_line('p3', 'p5')

    plot.add_line('p2', 'endpoint')
    plot.add_line('p2', 'p6')

    plot.show()
    time.sleep(1)
    plt.close()