import serial
import time
from matplotlib.widgets import Slider

import matplotlib.pyplot as plt

arduino = serial.Serial(port='/dev/cu.usbserial-10', baudrate=9600, timeout=.1)

# end 
# oneInitPos = 100
twoInitPos = 150
threeInitPos = 60

def send_angle(servo_id, angle):
    message = f"{servo_id}{angle}\n"
    arduino.write(message.encode())
    time.sleep(0.05) # small delay to ensure data is sent

def reset_servos():
    # send_angle('1', oneInitPos)
    send_angle('2', twoInitPos)
    send_angle('3', threeInitPos)

print("Resetting servos...")
time.sleep(2)
reset_servos()
time.sleep(2)
print("Servos reset")

path1 = {
    # '1': [130, 150, 10],
    '1': [150, 10],
#     '2': [80, 132, 10],
    # '3': [50, 110, 30],
#     '4': [35, 98, 30],
#     '6': [10, 80, 30],
    # '22': [50, 182, 10],
#     '23': [80, 152, 30],
    # '12': [140, 150, 30],
}

def travel_path(path):
    for key in path:
        print(f"Travelling to {key}...")
        angles = path[key]
        # send_angle('1', angles[0])
        send_angle('2', angles[0])
        send_angle('3', angles[1])
        time.sleep(0.4)

print("Pre Travelling path 1...")
time.sleep(3)
print("Travelling path 1...")
for _ in range(5):
    travel_path(path1)
    time.sleep(1)


# while True:
#     servo_id = input("SERVOID (1, 2, 3) [or reset]: ")
#     if servo_id not in ['1', '2', '3', 'reset']:
#         print("invalid (1,2, or 3)")
#         continue
#     if servo_id == 'reset':
#         reset_servos()
#         continue
#     try:
#         angle = int(input("Enter angle (0-180): "))
#         if 0 <= angle <= 180:
#             send_angle(servo_id, angle)
#         else:
#             print("invalid (0-180)")
#     except ValueError:
#         print("invalid")