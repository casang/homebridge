from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import time
import socket

luzOn = [0,0,0,0,0,0];
luzBrightness = [60,60,60,60,60,60];

class http_server:
    def __init__(self):
        server = HTTPServer(('', 8088), myHandler)
        server.serve_forever()

class myHandler(BaseHTTPRequestHandler):
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
            self.wfile.write(str(luzBrightness[i]))
            return
        b = False
        for i in range (0, 6):
            b = self.path.endswith("/?D" + str (i))
            if b:
                break
        if b == True:
            self.wfile.write(str(luzOn[i]))
            return
        pos = -1
        for i in range (0, 6):
            pos = self.path.find("/?A" + str (i) + "=")
            if (pos >= 0):
                break
        if pos >= 0 :
            s = int(self.path[pos + 5 : pos + 7])
            if i > 0:
                luzBrightness[i] = s
            else:
                for j in range (0, 6):
                    luzBrightness[j] = s
            self.wfile.write(str(luzBrightness[i]))
            return
        pos = -1
        for i in range (0, 6):
            pos = self.path.find("/?B" + str (i) + "=")
            if (pos >= 0):
                break
        if pos >= 0 :
            if (self.path[pos + 5 : pos + 7] == "1") :
                s = 1
            else :
                s = 0
            if i > 0:
                luzOn[i] = s
            else:
                for j in range (0, 6):
                    luzOn[j] = s
            self.wfile.write(str(luzOn[i]))
            return
        self.wfile.write("x")
        return

class main:
    def __init__(self):
        self.server = http_server()

if __name__ == '__main__':
    m = main()