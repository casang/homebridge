from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer

class http_server:
    def __init__(self):
        server = HTTPServer(('', 8088), myHandler)
        server.luzOn = [0,0,0,0,0,0];
        server.luzBrightness = [0,0,0,0,0,0];
        server.serve_forever()

class myHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        b = False
        for i in range (0, 6):
            b = self.path.endswith("/DI" + str (i))
            if (b):
                break
        if b == True:
            self.wfile.write(str(self.server.luzBrightness[i]))
            return
        b = False
        for i in range (0, 6):
            b = self.path.endswith("/DS" + str (i))
            if b:
                break
        if b == True:
            self.wfile.write(str(self.server.luzOn[i]))
            return
        pos = -1
        for i in range (0, 6):
            pos = self.path.find("/DI" + str (i) + "=")
            if (pos >= 0):
                break
        if pos >= 0 :
            s = int(self.path[pos + 5 : pos + 7])
            if i > 0:
                self.server.luzBrightness[i] = s
            else:
                for j in range (0, 6):
                    self.server.luzBrightness[j] = s
            self.wfile.write(str(self.server.luzBrightness[i]))
            return
        pos = -1
        for i in range (0, 6):
            pos = self.path.find("/DS" + str (i) + "=")
            if (pos >= 0):
                break
        if pos >= 0 :
            if (self.path[pos + 5 : pos + 7] == "01") :
                s = 1
            else :
                s = 0
            if i > 0:
                self.server.luzOn[i] = s
            else:
                for j in range (0, 6):
                    self.server.luzOn[j] = s
            self.wfile.write(str(self.server.luzOn[i]))
            return
        self.wfile.write("x")
        return

class main:
    def __init__(self):
        self.server = http_server()

if __name__ == '__main__':
    m = main()