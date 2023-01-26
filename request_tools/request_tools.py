# Version: 5
# Written by Tim Hanewich
# This is from https://github.com/TimHanewich/MicroPython-Collection/tree/master/request_tools

import socket

def read_all(s:socket.socket, buffer_size:int = 100, timeout_seconds:float = 0.50) -> bytearray:
    s.settimeout(timeout_seconds)
    full_data:bytearray = bytearray()
    while True:
        try:
            data = s.recv(buffer_size)
            for b in data:
                full_data.append(b)
        except:
            break
    return full_data

class request:

    method:str = None
    path:str = None
    body:str = None
    headers:dict = {}

    @staticmethod
    def parse(full_request:str):
        ToReturn = request()
        
        # split
        parts = full_request.split("\r\n")

        # get the method
        p1 = parts[0]
        loc1 = p1.index(" ")
        tr = p1[0:loc1]
        ToReturn.method = tr

        # path
        p1 = parts[0]
        loc1 = p1.index(" ")
        loc2 = p1.index(" ", loc1 + 1)
        tr = p1[loc1+1:loc2]
        ToReturn.path = tr

        # body
        bs = full_request.split("\r\n\r\n")
        ToReturn.body = bs[1]

        # headers dictionary
        #get part before body
        before_body = bs[0]
        bb_parts = before_body.split("\r\n")
        for x in range(1, len(bb_parts)):
            this_header = bb_parts[x]
            cl = this_header.index(":")
            k = this_header[0:cl]
            v = this_header[cl+1:9999].strip()
            ToReturn.headers[k] = v

        return ToReturn
    

# Tests below!
#data = b'POST /odata HTTP/1.1\r\nContent-Type: application/json\r\nUser-Agent: PostmanRuntime/7.29.2\r\nAccept: */*\r\nPostman-Token: 5be68124-31a2-48bb-8399-ed11aee876ab\r\nHost: 10.0.0.122\r\nAccept-Encoding: gzip, deflate, br\r\nConnection: keep-alive\r\nContent-Length: 50\r\n\r\n{\r\n    "Name": "Tim",\r\n    "FavoriteNumber": 10\r\n}'
#data = b'POST / HTTP/1.1\r\nContent-Type: application/json\r\nUser-Agent: PostmanRuntime/7.29.2\r\nAccept: */*\r\nPostman-Token: 7e87d8d0-f434-4e22-92e3-8012a3698937\r\nHost: 10.0.0.122\r\nAccept-Encoding: gzip, deflate, br\r\nConnection: keep-alive\r\nContent-Length: 50\r\n\r\n{\r\n    "Name": "Tim",\r\n    "FavoriteNumber": 10\r\n}'
#datas = data.decode()
#r = request.parse(datas)