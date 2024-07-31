import math
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider, Button
import serial
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

class Plot:
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.points = {}
        self.lines = []

    def add_or_update_point(self, identifier, x, y):
        if identifier in self.points:
            self.points[identifier].set_data((x,), (y,))
        else:
            self.points[identifier], = self.ax.plot(x, y, 'o', label=identifier)

    def add_or_update_line(self, point1_id, point2_id):
        for line in self.lines:
            if line.get_label() == f"{point1_id}-{point2_id}":
                point1 = self.points[point1_id].get_data()
                point2 = self.points[point2_id].get_data()
                line.set_data([point1[0][0], point2[0][0]], [point1[1][0], point2[1][0]])
                return

        if point1_id in self.points and point2_id in self.points:
            point1 = self.points[point1_id].get_data()
            point2 = self.points[point2_id].get_data()
            line, = self.ax.plot([point1[0][0], point2[0][0]], [point1[1][0], point2[1][0]], 'r-', label=f"{point1_id}-{point2_id}")
            self.lines.append(line)

    def show(self):
        self.ax.legend()
        plt.show()

def transform_angle1(angle):
    return angle + 90

def transform_angle2(angle):
    return angle + 90

arduino = serial.Serial(port='/dev/cu.usbserial-10', baudrate=9600, timeout=.1)

def send_angle(servo_id, angle):
    message = f"{servo_id}{angle}\n"
    arduino.write(message.encode())
    time.sleep(0.05) # small delay to ensure data is sent

# Initial values
x, y = 10, -70
upperLeg = 80
lowerLeg = 128

plot = Plot()

t1Stack = []
t2Stack = []

def moving_avg(theta, stack):
    stack.append(theta)
    if len(stack) == 0:
        return theta
    if len(stack) > 6:
        stack.pop(0)
    return sum(stack) / len(stack)


def update_plot(x, y):
    result = inverseKinematics(x, y, upperLeg, lowerLeg)
    if result == "No solution":
        return
    else:
        t1, t2 = result

    OJK1 = offsetJointKinematics(upperLeg, 68, 80, 125, lowerLeg, 0, 70, math.degrees(t1), math.degrees(t2))

    # offsetjoint kinematics parameters: l1, l2, l4, l5, l8, x4, y4, t1, t2
    
    print("Angle 1 (Theta 1): ", moving_avg(transform_angle1(OJK1.t1), t1Stack)) 
    send_angle('3', moving_avg(transform_angle1(OJK1.t1), t1Stack))
    
    print("Angle 5 (Theta 5): ", moving_avg(transform_angle2(math.degrees(OJK1.getThetaFive())), t2Stack))
    send_angle('2', moving_avg(transform_angle2(math.degrees(OJK1.getThetaFive())), t2Stack))

    plot.add_or_update_point('p1', OJK1.p1[0], OJK1.p1[1])
    plot.add_or_update_point('p2', OJK1.p2[0], OJK1.p2[1])
    plot.add_or_update_point('p3', OJK1.p3[0], OJK1.p3[1])
    plot.add_or_update_point('p4', OJK1.p4[0], OJK1.p4[1])
    plot.add_or_update_point('p5', OJK1.p5[0], OJK1.p5[1])
    plot.add_or_update_point('p6', OJK1.p6[0], OJK1.p6[1])
    plot.add_or_update_point('endpoint', x, y)

    plot.add_or_update_line('p1', 'p2')
    plot.add_or_update_line('p2', 'p3')
    plot.add_or_update_line('p1', 'p4')
    plot.add_or_update_line('p4', 'p5')
    plot.add_or_update_line('p3', 'p5')
    plot.add_or_update_line('p2', 'endpoint')
    plot.add_or_update_line('p2', 'p6')
    
    plot.ax.set_xlim(-300, 300)
    plot.ax.set_ylim(-300, 300)

    plt.draw()

# Sliders setup
axcolor = 'lightgoldenrodyellow'
ax_x = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
ax_y = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)

def trace_path(equation, x_range, x_direction):
    if (x_direction > 0):
        current_x = x_range[0]
        while(current_x <= x_range[1]):
            y = equation(current_x)
            print("X: ", current_x, "Y: ", y)
            update_plot(current_x, y)
            plt.pause(0.0005)
            current_x += x_direction
            # time.sleep(0.01)
    elif (x_direction < 0):
        current_x = x_range[1]
        while(current_x >= x_range[0]):
            y = equation(current_x)
            print("X: ", current_x, "Y: ", y)
            update_plot(current_x, y)
            plt.pause(0.0005)
            current_x += x_direction
            # time.sleep(0.01)

def sin_step(x):
    return (70/2) * math.sin(2*math.pi / 140 * x + math.pi/2)-135

def semi_circle(x):
    return math.sqrt(70**2 - x**2) - 170

def flat_line(x):
    return -170

# Initial plot (servo init pos determined by arduino program)
for x in range(5):
    trace_path(sin_step, (-70, 70), 20)
    # trace_path(semi_circle, (-70, 70), 5)
    trace_path(flat_line, (-70, 70), -30)