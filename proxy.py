import socket
import select
import time
import sys
import re
def main():
    try:
        buffer_size = 4096
        delay = 0.005
        forward_to = ('127.0.0.1', 9387)
        class Forward:
            def __init__(self):
                self.forward = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            def start(self, host, port):
                try:
                    self.forward.connect((host, port))
                    return self.forward
                except:
                    return False
        class sock:
            input_list = []
            channel = {}
            def __init__(self, host, port):
                self.s = None
                self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.server.bind((host, port))
                self.server.listen(200)
            def main_loop(self):
                self.input_list.append(self.server)
                while 1:
                    time.sleep(delay)
                    ss = select.select
                    inputready, outputready, exceptready = ss(self.input_list, [], [])
                    for self.s in inputready:
                        if self.s == self.server:
                            self.on_accept()
                            break
                        self.data = self.s.recv(buffer_size)
                        if len(self.data) == 0:
                            self.on_close()
                            break
                        else:
                            self.on_recv()
            def on_accept(self):
                forward = Forward().start(forward_to[0], forward_to[1])
                clientsock, clientaddr = self.server.accept()
                if forward:
                    self.input_list.append(clientsock)
                    self.input_list.append(forward)
                    self.channel[clientsock] = forward
                    self.channel[forward] = clientsock
                else:
                    clientsock.close()
            def on_close(self):
                self.input_list.remove(self.s)
                self.input_list.remove(self.channel[self.s])
                out = self.channel[self.s]
                self.channel[out].close()
                self.channel[self.s].close()
                del self.channel[out]
                del self.channel[self.s]
            def on_recv(self):
                data = self.data
                self.channel[self.s].send(data)
        try:
            try:
                server = sock('0.0.0.0', 5000)
                server.main_loop()
            except:
                pass
        except:
            pass
    except:
        pass     
if __name__ == '__main__':
    try:
        main()
    except:
        sys.exit()