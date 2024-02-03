from collections import namedtuple
import socket
import time
import socket
import struct

HOST = ""  # Standard loopback interface address (localhost)
PORT = 2947  # Port to listen on (non-privileged ports are > 1023)

# https://web.archive.org/web/20110718125612/http://gpsd.berlios.de/gpsd.html

# Pytohon Sockets
# https://realpython.com/python-sockets/

# Good overview over gpsd
# https://gpsd.io/client-howto.html

# Creatinga gpsd Client in C and Python
# https://gpsd.gitlab.io/gpsd/gpsd-client-example-code.html
# NOTE gps.py is installed witn gpsd in /usr/lib/python3/dist-packages/gps/gps.py

# Documentazione del protocollo JSON di GPSD
# https://www.mankier.com/5/gpsd_json

# Definizione di GGA
# https://gpsd.gitlab.io/gpsd/NMEA.html#_gga_global_positioning_system_fix_data

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        s.bind((HOST, PORT))
        s.listen(5)

        NmeaFile = namedtuple('NmeaFile', 'file delay')
        nmeaFile1 = NmeaFile(file='NMEALog.nmea', delay=0.05)
        nmeaFile2 = NmeaFile(file='NMEALog_GGAonly.nmea', delay=1.0)
        nmeaFile = nmeaFile2

        file1 = open(nmeaFile.file, 'r', encoding='cp1252')
        Lines = file1.readlines()
        print(f'Founs {len(Lines)} Nmea sentences in {file1}!')

        print(f"Accepting connections on {HOST}:{PORT}")
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                # TESTS for interaction with GPSd
                # conn.sendall(b'{"class":"VERSION","release":"3.20","rev":"3.20","proto_major":3,"proto_minor":14};\r\n')
                # print(conn.type)
                # time.sleep(1)
                # data = conn.recv(1024)
                # if not data:
                #     continue
                # else:
                #     print(data)

                # nmeaCounter = 0
                # while True:
                #     time.sleep(1)
                #     nmeaEncoded = '$GPGGA,085232.00,4530.202688,N,00913.483391,E,1,08,1.6,148.0,M,48.1,M,,*66'.encode('ascii')
                #     print(f'{nmeaCounter:0000} Sending Nmea of {len(nmeaEncoded)}bytes...')
                #     conn.sendall(nmeaEncoded)
                #     # conn.sendall(b'{"class":"TPV","tag":"MID2","device":"/dev/pts/1","time":"2005-06-08T10:34:48.283Z","ept":0.005,"lat":46.498293369,"lon":7.567411672,"alt":1343.127,"eph":36.000,"epv":32.321,"track":10.3788,"speed":0.091,"climb":-0.085,"mode":3};\r\n')
                #     nmeaCounter += 1

                nmeaCounter = 1
                # Strips the newline character
                while (True):
                    for line in Lines:
                        nmeaEncoded = line.encode('ascii')
                        print("Line{}: {}".format(nmeaCounter, line.strip()))
                        conn.sendall(nmeaEncoded)
                        time.sleep(nmeaFile.delay)
                        nmeaCounter += 1
                    print(f'Rewind time and start over..')

except Exception as e:
    print(e)