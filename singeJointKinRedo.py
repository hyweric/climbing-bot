import math
import matplotlib.pyplot as plt

class offsetJointKinematics:
    def __init__(self, l1, l2, l4, l5, x4, y4, t1, t2): 
        self.t1 = t1
        self.t2 = t2
        self.l1 = l1
        self.l2 = l2
        self.l3 = None 
        self.l4 = l4 
        self.l5 = l5
        self.l6 = math.dist((0, 0), (x4, y4))
        
        self.p1 = (0, 0)
        self.p2 = self.getP2()
        self.p3 = self.getP3()
        self.p4 = (x4, y4)
        self.p5 = (self.p4[0] - l4 * math.sin(self.getThetaFive()), self.p4[1] + l4 * math.cos(self.getThetaFive()))
    
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
    
    def getthetaFour(self):
        p3= self.getP3()
        l3 = math.dist(p3, self.p4)
        l7 = self.getL7()
        print("l6: ", self.l6, "l7: ", l7, "l1: ", self.l1, "l3: ", l3, "l2: ", self.l2)
        Q4partComplementBottom = self.lawOfCosines(self.l6, l7, self.l1)
        Q4partComplementTop = self.lawOfCosines(l3, l7, self.l2)
        q4 = math.pi- (Q4partComplementBottom + Q4partComplementTop)
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

class InteractivePlot:
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

OJK1 = offsetJointKinematics(23, 10, 10, 18, 0, 5, 25.55469378478778, 113.03568410594136)
print("Theta 3: ", math.degrees(OJK1.getThetaThree()))
print("Theta 4: ", math.degrees(OJK1.getthetaFour()))
print("Theta 5: ", math.degrees(OJK1.getThetaFive()))

plot = InteractivePlot()
plot.add_or_update_point('p1', OJK1.p1[0], OJK1.p1[1])
plot.add_or_update_point('p2', OJK1.p2[0], OJK1.p2[1])
plot.add_or_update_point('p3', OJK1.p3[0], OJK1.p3[1])
plot.add_or_update_point('p4', OJK1.p4[0], OJK1.p4[1])
plot.add_or_update_point('p5', OJK1.p5[0], OJK1.p5[1])
plot.add_line('p1', 'p2')
plot.add_line('p2', 'p3')
plot.add_line('p1', 'p4')
plot.add_line('p4', 'p5')
plot.add_line('p3', 'p5')

plot.show()