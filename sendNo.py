import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.17.134", 1235))
s.sendall("No")
s.close()
