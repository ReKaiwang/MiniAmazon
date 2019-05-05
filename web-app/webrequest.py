import commu_pb2
import socket
from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.encoder import _EncodeVarint

class WebRequest:
    def __init__(self, addr, whid, x, y, packageid, UPSuserid):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(addr)
        self.request = commu_pb2.AOrderPlaced()
        self.request.whid = whid
        self.request.x = x
        self.request.y = y
        self.request.packageid = packageid
        self.request.UPSuserid = UPSuserid
        self.request.seqnum = 0

    def add_products(self, name, description, count):
        product = self.request.things.add()
        product.name = name
        product.description = description
        product.count = count

    def send_request(self):
        message = self.request.SerializeToString()
        _EncodeVarint(self.sock.send, len(message), None)
        while True:
            try:
                self.sock.sendall(message)
            except socket.error as e:           # broken connection
                self.sock.connect(self.addr)
                continue
            else:
                break

def main():
    HOST = '192.168.1.18'
    PORT = 12345
    addr = (HOST, PORT)
    whid = 1
    x = 0
    y = 0
    packageid = 1
    UPSuserid = 1
    wp = WebRequest(addr, whid, x, y, packageid, UPSuserid)
    wp.send_request()

if __name__ == '__main__':
    main()