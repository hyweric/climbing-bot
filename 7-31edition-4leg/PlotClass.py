import matplotlib.pyplot as plt

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

    def plotLines(self, OJKClass, x, y):
        self.add_or_update_point('p1', OJKClass.p1[0], OJKClass.p1[1])
        self.add_or_update_point('p2', OJKClass.p2[0], OJKClass.p2[1])
        self.add_or_update_point('p3', OJKClass.p3[0], OJKClass.p3[1])
        self.add_or_update_point('p4', OJKClass.p4[0], OJKClass.p4[1])
        self.add_or_update_point('p5', OJKClass.p5[0], OJKClass.p5[1])
        self.add_or_update_point('p6', OJKClass.p6[0], OJKClass.p6[1])
        self.add_or_update_point('endpoint', x, y)

        self.add_or_update_line('p1', 'p2')
        self.add_or_update_line('p2', 'p3')
        self.add_or_update_line('p1', 'p4')
        self.add_or_update_line('p4', 'p5')
        self.add_or_update_line('p3', 'p5')
        self.add_or_update_line('p2', 'endpoint')
        self.add_or_update_line('p2', 'p6')
        
        self.ax.set_xlim(-300, 300)
        self.ax.set_ylim(-300, 300)

        plt.draw()