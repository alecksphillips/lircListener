import socket
import sys
import re
from subprocess import call

UDP_PORT = 5006
UDP_IP = "0.0.0.0"

if len(sys.argv) > 0:
  UDP_PORT = int(sys.argv[1])

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # Internet,UDP
sock.bind((UDP_IP, UDP_PORT))

print("Listening on : "+str(UDP_IP)+":"+str(UDP_PORT)+"...")

while True:
  data = b''
  addr = ""
  data, addr = sock.recvfrom(1024)

  print("received message: ", data, " from: ", addr)
  print("length: ", len(data))
  print("decode: ", data.decode())

  m = data.decode()
  m = re.split("[^a-zA-Z0-9 _]", m)[0]
  call("irsend SEND_ONCE " + m,shell=True)
