import serial
import time

# Conectar al Kobuki
ser = serial.Serial('/dev/ttyUSB0', baudrate=115200, timeout=1)
print("Conectado al Kobuki")

# Leer datos del Kobuki
print("Leyendo datos...")
for i in range(10):
    data = ser.read(100)
    if data:
        print(f"Datos recibidos: {data.hex()}")
    time.sleep(0.5)

ser.close()
