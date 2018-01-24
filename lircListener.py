import socket
import http.server
import socketserver
import urllib.request
import sys
import re
from subprocess import call
import threading


UDP_PORT = 5006
UDP_IP = "0.0.0.0"

HTTP_PORT = 5007
HTTP_PORT = "0.0.0.0"

if len(sys.argv) > 1:
  UDP_PORT = int(sys.argv[1])
if len(sys.argv) > 2:
  HTTP_PORT = int(sys.argv[2])

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # Internet,UDP
sock.bind((UDP_IP, UDP_PORT))

def lircCommand(message):
  m = re.split("[^a-zA-Z0-9 _]", message)[0]
  #print("Lirc: " + m + "\n")
  call("irsend SEND_ONCE " + m,shell=True)

class HTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
  def _set_headers(self):
    self.send_header('Content-type', 'text/html')
    self.end_headers()  

  def do_GET(self):
    if(self.path == '/'):
      self._set_headers()
      self.wfile.write("<html><body><h1>Test</h1></body></html>")
      self.send_response(200)
   
  def do_POST(self):
    content_length = int(self.headers['Content-Length'])
    post_data = self.rfile.read(content_length)
    #print(post_data)
    m = post_data.decode('utf-8')
    #lircCommand(urllib.request.unquote(m))
    lircCommand(m)
    #self.send_header('Content-type','text/html')
    #self.wfile.write("<html><body><h1>Post!</h1></body></html>".encode('utf-8'))
    self.send_response(200)
    self.end_headers()
      

class HTTPHandler (threading.Thread):
  def __init__(self,threadLock):
    threading.Thread.__init__(self)
    self.lock = threadLock

  def run(self):
    httpd = socketserver.TCPServer(("", HTTP_PORT),HTTPRequestHandler)
    httpd.serve_forever()

class UDPHandler (threading.Thread):
  def __init__(self,threadLock):
    threading.Thread.__init__(self)
    self.lock = threadLock

  def run(self):
    data = b''
    addr = ""
    while True:
      data, addr = sock.recvfrom(1024)
      self.lock.acquire()
      #print("received message: ", data, " from: ", addr)
      #print("length: ", len(data))
      m = data.decode()
      #print("decode: ", m)
      lircCommand(m)
      self.lock.release()


my_lock = threading.Lock()

httpThread = HTTPHandler(my_lock)
udpThread = UDPHandler(my_lock)

httpThread.start()
udpThread.start()
