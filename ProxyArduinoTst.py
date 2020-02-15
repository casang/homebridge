import http.server
#import BaseHTTPRequestHandler
import threading
import time
import socket
import sys

luzOn = [0,0,0,0,0,0];
luzOnSet = [1,1,1,1,1,1];
luzBrightness = [0,0,0,0,0,0];
luzBrightnessSet = [60,60,60,60,60,60];
message = str();

def get_status(num): 
# Create a TCP/IP socket
    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
        sock.connect(('192.168.0.177', 8088))
#try:
        # Send data
        message = 'GET /?C0'

        #C1=xxx&C2=xxx&C3=xxx&C4=xxx&C5=xxx
        #0123456789012345678901234567890123
        print ('sending "%s"' % message, file = sys.stderr)
        sock.sendall(bytes(message,"utf-8") + b"\n\n")

        # Look for the response
        data = sock.recv(1024)
        message = str (data)
        
        print ('received "%s"' % message, file = sys.stderr)
        #for i in range (0, 5):
            #luzBrightness[i + 1] = int(message[i * 7 + 5 : i * 7 + 8])
    
        sock.close()
        continue

        message = ''
        for i in range (1, 6):
            if luzBrightnessSet[i] != luzBrightness[i]:
                valor = str(luzBrightnessSet[i])
                if message != "":
                    message = message + "&"
                message = message + "A" + str(i) + "=" + valor
        
        if message != "":
            message = "GET /?" + message
        
            sockCmd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sockCmd.connect (('192.168.0.177', 8088))
        
            print ('sending "%s"' % message, file = sys.stderr)
            sockCmd.sendall(bytes(message,"utf-8") + b"\n\n")

        # Look for the response
            data = sockCmd.recv(1024)
            print ('received "%s"' % data, file = sys.stderr)
        
            sockCmd.close()

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
        sock.connect(('192.168.0.177', 8088))
#try:
        # Send data
        message = 'GET /?D0'

        #D1=x&D2=x&D3=x&D4=x&D5=x
        #012345678901234567890123
        print ('sending "%s"' % message, file = sys.stderr)
        sock.sendall(bytes(message,"utf-8") + b"\n\n")

        # Look for the response
        data = sock.recv(1024)
        message = str (data)
        
        print ('received "%s"' % message[5 : 8], file = sys.stderr)
        for i in range (0, 5):
            luzOn[i + 1] = int(message[i * 5 + 5 : i * 5 + 6])
    
        sock.close()

        message = ''
        for i in range (1, 6):
            if luzOnSet[i] != luzOn[i]:
                valor = str(luzOnSet[i])
                if message != "":
                    message = message + "&"
                message = message + "B" + str(i) + "=" + valor
        
        if message != "":
            message = "GET /?" + message
        
            sockCmd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sockCmd.connect (('192.168.0.177', 8088))
        
            print ('sending "%s"' % message, file = sys.stderr)
            sockCmd.sendall(bytes(message,"utf-8") + b"\n\n")

        # Look for the response
            data = sockCmd.recv(1024)
            print ('received "%s"' % data, file = sys.stderr)
        
            sockCmd.close()

        #time.sleep (num)

#finally:
#    print ('closing socket', file = sys.stderr)
#    sock.close()


class http_server:
    def __init__(self):
        server = http.server.HTTPServer(('', 8088), myHandler)
        server.serve_forever()

class myHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        b = False
        for i in range (0, 6):
            b = self.path.endswith("/?C" + str (i))
            if (b):
                break
        if b == True:
            self.wfile.write(bytes(str(luzBrightness[i]),"utf-8"))
            #self.wfile.write(str(luzBrightness[i]))
            #self.wfile.write(str(luzBrightness[i]))
            return
        b = False
        for i in range (0, 6):
            b = self.path.endswith("/?D" + str (i))
            if b:
                break
        if b == True:
            self.wfile.write(bytes(str(luzOn[i]),"utf-8"))
            #self.wfile.write(str(luzOn[i]))
            return
        pos = -1
        for i in range (0, 6):
            pos = self.path.find("/?A" + str (i) + "=")
            if (pos >= 0):
                break
        if pos >= 0 :
            s = int(self.path[pos + 5 : pos + 7])
            if i > 0:
                luzBrightnessSet[i] = s
            else:
                for j in range (0, 6):
                    luzBrightnessSet[j] = s
            self.wfile.write(b'1')
            return
        pos = -1
        for i in range (0, 6):
            pos = self.path.find("/?B" + str (i) + "=")
            if (pos >= 0):
                break
        if pos >= 0 :
            print ("valor::::::::::")
            print (self.path[pos + 5 : pos + 7])
            if (self.path[pos + 5 : pos + 7] == "1") :
                s = 1
            else :
                s = 0
            if i > 0:
                luzOnSet[i] = s
            else:
                for j in range (0, 6):
                    luzOnSet[j] = s
            self.wfile.write(b'1')
            return
        self.wfile.write(b"x")
        return

class main:
    t1 = threading.Thread(target=get_status, args=(1,))
    t1.start()
    #def __init__(self):
    #    self.server = http_server()

if __name__ == '__main__':
    m = main()