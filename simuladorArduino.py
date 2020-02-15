import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the port
server_address = ('arduino1', 8081)
print ('starting up on %s port %s' % server_address, file = sys.stderr)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print ('waiting for a connection', file = sys.stderr)
    connection, client_address = sock.accept()

    try:
        print ('connection from', client_address, file = sys.stderr)

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(16)
            print ('received "%s"' % data, file = sys.stderr)
            if data:
                b = False
                for i in range (0, 6):
                    b = data.endswith("/?C" + str (i))
                    if (b):
                        break
                if b == True:
                    connection.sendall(str(luzBrightness[i]))
                    continue
                b = False
                for i in range (0, 6):
                    b = data.endswith("/?D" + str (i))
                    if b:
                        break
                if b == True:
                    connection.sendall(str(luzOn[i]))
                    continue
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
                    connection.sendall(str(luzBrightness[i]))
                    continue
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
                    connection.sendall(str(luzOn[i]))
                    continue
                
                connection.sendall("x")

    finally:
        # Clean up the connection
        connection.close()
