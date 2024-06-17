import serial.tools.list_ports

ports = serial.tools.list_ports.comports()
serialInst = serial.Serial()
portsList = []

for onePort in ports:
    portsList.append(str(onePort))
    print(str(onePort))

com = input("Enter the port number: ")

for i in range(len(portsList)):
    if portsList[i].startswith(com):
        use = "COM" + com
        print(use)

serialInst.baudrate = 9600
serialInst.port = use
serialInst.open()

while True:
    command = input("Enter command: ")
    serialInst.write(command.encode('utf-8'))

    if command == 'exit':
        exit(0)

