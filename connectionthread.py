from threading import Thread
from socket import socket
from connectionresult import ConnectionResult



class ConnectionThread(Thread):

    sock: socket
    dest_server_addr: tuple[str, int]
    result: ConnectionResult

    def __init__(self, sock: socket, dest_server_addr: tuple[str, int], result: ConnectionResult):
        Thread.__init__(self)
        self.sock = sock
        self.dest_server_addr = dest_server_addr
        self.result = result

    def run(self):
        # Start a thread to attempt a connection
        self.sock.settimeout(7.5)
        try:
            self.sock.connect(self.dest_server_addr)
            self.sock.settimeout(None)
            self.result.fail = False
        except TimeoutError:
            self.result.fail = True
        except ConnectionRefusedError:
            self.result.fail = True