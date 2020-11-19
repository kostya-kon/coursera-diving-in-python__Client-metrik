import time
import socket


class ClientError(Exception):
    """custom error"""
    def __init__(self, text=None):
        self.txt = text


class Client:
    """class of client"""
    def __init__(self, host, port, timeout=None):
        self.host = host
        self.port = port
        self.timeout = timeout or None
        self.sock = socket.create_connection((host, port))

    def put(self, metric, value, timestamp=None):
        try:
            if timestamp is None:
                timestamp = int(time.time())
            data = "put " + metric + " " + str(value) + " " + str(timestamp) + "\n"
            data = bytes(data, encoding="utf-8")
            self.sock.sendall(data)
            indata = self.sock.recv(2048).decode("utf-8")
            print(indata)
            if indata[:5:] == "error":
                raise ClientError
        except Exception:
            raise ClientError

    def get(self, metric):
        try:
            data = "get " + metric + "\n"
            data = bytes(data, encoding="utf-8")
            self.sock.sendall(data)
            indata = self.sock.recv(1024)
            if indata.decode()[:5:] == "error":
                raise ClientError
            answer = (indata.decode()[3::]).split()
            dict_ans = dict()
            for i in range(len(answer)):
                if i == 0 or i % 3 == 0:
                    if answer[i] not in dict_ans:
                        dict_ans[answer[i]] = [(int(answer[i+2]), float(answer[i+1]))]
                    else:
                        dict_ans[answer[i]].append((int(answer[i+2]), float(answer[i+1])))
                        dict_ans[answer[i]].sort()
            return dict_ans
        except Exception:
            raise ClientError

    def __del__(self):
        self.sock.close()

"""
x = Client("127.0.0.1", 8181)
x.put("key", 1, 1)
x.get("key")
for i in range(3):
    x.put("key", i+5, i)
"""
sock = socket.create_connection(("127.0.0.1", 8888))

commands = ["put test_multivalue_key 12.0 1503319740", "put test_multivalue_key 12.5 1503319743", "put test_multivalue_key 10.678 1503319748", "put test_multivalue_key 10.666 1503319748"]

for command in commands:
    sock.sendall(command.encode())
    data = sock.recv(2048).decode("utf-8")
    print(data)
