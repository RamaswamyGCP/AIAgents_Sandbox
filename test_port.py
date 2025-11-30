import socket
import sys

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

print(f"Port 6006 in use: {is_port_in_use(6006)}")
print(f"Python executable: {sys.executable}")
