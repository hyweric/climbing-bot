import serial
import time

from matplotlib.widgets import Slider

import matplotlib.pyplot as plt

arduino = serial.Serial(port='/dev/cu.usbserial-10', baudrate=9600, timeout=.1)

# end 
oneInitPos = 110
twoInitPos = 150
threeInitPos = 28

import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

threeInitPos = 28

def send_angle(servo_id, angle):
    message = f"{servo_id}{angle}\n"
    arduino.write(message.encode())
    time.sleep(0.05) # small delay to ensure data is sent

def reset_servos():
    send_angle('1', oneInitPos)
    send_angle('2', twoInitPos)
    send_angle('3', threeInitPos)

print("Resetting servos...")
time.sleep(2)
reset_servos()
time.sleep(2)
print("Servos reset")

# Create a new figure and three sliders
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.25)

axcolor = 'lightgoldenrodyellow'
ax1 = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
ax2 = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)
ax3 = plt.axes([0.25, 0.2, 0.65, 0.03], facecolor=axcolor)

s1 = Slider(ax1, '1', 0, 180, valinit=oneInitPos, valstep=1)
s2 = Slider(ax2, '2', 0, 180, valinit=twoInitPos, valstep=1)
s3 = Slider(ax3, '3', 0, 180, valinit=threeInitPos, valstep=1)

# Define an update function that will be called when the sliders are changed
def update(val):
    send_angle('1', s1.val)
    send_angle('2', s2.val)
    send_angle('3', s3.val)

# Call the update function when the sliders are changed
s1.on_changed(update)
s2.on_changed(update)
s3.on_changed(update)

plt.show()