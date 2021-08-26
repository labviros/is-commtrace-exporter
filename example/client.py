import socket

def main():                                                                                                        
    msgFromClient       = "{ \"timestamp_send\": \"1580324321783303\", \"timestamp_rcvd\": \"1580324321816115\",\"x-b3-flags\": \"0\", \"x-b3-parentspanid\": \"0000000000000000\", \"x-b3-sampled\": \"1\", \"x-b3-spanid\": \"05d1f60ea497b2da\", \"x-b3-traceid\": \"c4ef28798e62f374\", \"spanname\": \"client-test\"}"
    bytesToSend         = str.encode(msgFromClient)
    # serverAddressPort   = ("127.0.0.1", 8951)
    serverAddressPort   = ("10.10.2.7", 31589)
    bufferSize          = 2048
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    print("sending")
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)
    msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    msg = "Message from Server {}".format(msgFromServer[0])
    print(msg)

if __name__ == '__main__':
    main()
