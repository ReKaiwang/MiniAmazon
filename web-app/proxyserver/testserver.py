import socket 
import commu_pb2
import amazon_pb2
from threading import Thread 
from parser import WebRequestParser
from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.encoder import _EncodeVarint


def recv_response(sock):
        """recv message from world
        Return byte string as result
        """
        var_int_buff = []
        count = 0

        while True:     # get the length of the message
            try:
                count += 1
                buf = sock.recv(1)
                var_int_buff += buf
                
                msg_len, new_pos = _DecodeVarint32(var_int_buff, 0)
                if new_pos != 0:
                    break
            except:                # broken connection
                # sock.connect(self.addr)
                continue
        print(msg_len)
        whole_message = sock.recv(msg_len)
        # response = amazon_pb2.AConnected()
        # response.ParseFromString(whole_message)
        return whole_message

# from SocketServer import ThreadingMixIn 

# Multithreaded Python server : TCP Server Socket Thread Pool
class ClientThread(Thread): 
 
    def __init__(self,ip,port): 
        Thread.__init__(self) 
        self.ip = ip 
        self.port = port 
        # print "[+] New server socket thread started for " + ip + ":" + str(port) 
 
    def run(self): 
        while True : 
            data = conn.recv(2048) 
            # print "Server received data:", data
            MESSAGE = input("Multithreaded Python server : Enter Response from Server/Enter exit:")
            if MESSAGE == 'exit':
                break
            conn.send(MESSAGE.encode())  # echo 

# Multithreaded Python server : TCP Server Socket Program Stub
TCP_IP = '10.0.0.243' 
TCP_PORT = 5678
BUFFER_SIZE = 20  # Usually 1024, but we need quick response 

tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
tcpServer.bind(('', TCP_PORT)) 
threads = []


 
while True: 
    tcpServer.listen(4) 
    # print "Multithreaded Python server : Waiting for connections from TCP clients..." 
    (conn, (ip,port)) = tcpServer.accept() 
    print("connected")
    # recv request from front end
    message = recv_response(conn)
    request = commu_pb2.ACommunicate()
    request.ParseFromString(message)
    print(request)
    
    wp = WebRequestParser(request)
    wp.getAPurchaseMore(0)
    wp.getAPack(1)
    wp.getAOrderPlaced(2)
    print("ACommands")
    print(wp.getACommands())
    print("UCommunicates")
    print(wp.getUCommunicate())
    
    # newthread = ClientThread(ip,port) 
    # newthread.start() 
    # threads.append(newthread) 
 
# for t in threads: 
#     t.join()