import serial
import struct
import time

def crear_comando_velocidad(speed, radius):
    subpayload = struct.pack('<BBhh', 0x01, 0x04, speed, radius)
    longitud = len(subpayload)
    paquete = bytes([0xAA, 0x55, longitud]) + subpayload
    checksum = 0
    for b in paquete[2:]:
        checksum ^= b
    return paquete + bytes([checksum])

def mover(ser, speed, radius, duracion):
    t_inicio = time.time()
    while time.time() - t_inicio < duracion:
        cmd = crear_comando_velocidad(speed, radius)
        ser.write(cmd)
        time.sleep(0.1)

ser = serial.Serial('/dev/ttyUSB0', baudrate=115200, timeout=1)
print("Iniciando cuadrado...")

for i in range(4):
    print(f"Lado {i+1}...")
    mover(ser, 200, 0, 2.0)   # Avanza recto
    print(f"Giro {i+1}...")
    mover(ser, 100, 1, 3.0)   # Gira 90 grados

# Detener
mover(ser, 0, 0, 0.5)
ser.close()
print("Cuadrado completado")