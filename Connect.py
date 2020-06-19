import serial
a=None

def connect():

    i = 0

    listusb = ['COM%s' % (i + 1) for i in range(20)]

    while i < len(listusb):
        try:
            receiver = serial.Serial(listusb[i], 9600,timeout=3)

            return receiver

        except serial.serialutil.SerialException:
            i += 1

    return a