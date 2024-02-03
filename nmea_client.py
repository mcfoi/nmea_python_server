import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 2947  # The port used by the server

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        # s.sendall(b'?WATCH={"enable":true,"nmea":true,"raw":true};')
        data = s.recv(1024)
        print(data)

    print(f"Received {data!r}")
except Exception as e:
    print(e)