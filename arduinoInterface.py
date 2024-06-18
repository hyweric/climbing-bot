import serial
import time

arduino = serial.Serial(port='/dev/cu.usbserial-10', baudrate=9600, timeout=.1)

def send_angle(servo_id, angle):
    message = f"{servo_id}{angle}\n"
    arduino.write(message.encode())
    time.sleep(0.05) # small delay to ensure data is sent

while True:
    servo_id = input("SERVOID (1, 2, 3): ")
    if servo_id not in ['1', '2', '3']:
        print("invalid (1,2, or 3)")
        continue
    
    try:
        angle = int(input("Enter angle (0-180): "))
        if 0 <= angle <= 180:
            send_angle(servo_id, angle)
        else:
            print("invalid (0-180)")
    except ValueError:
        print("invalid")