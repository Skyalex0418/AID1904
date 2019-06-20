"""
httpserver.py
功能：httpserver 部分的主程序
"""

from socket import *
from threading import Thread
from config import *
import re
import json

ADDR = (HOST, PORT)


def connect_frame(env):
    """

    :param env: 得到要发送给frame的请求字典
    :return: 从frame得到得数据
    """
    s = socket()
    try:
        s.connect((frame_ip, frame_port))
    except Exception as e:
        print(e)
        return
    data = json.dumps(env)
    s.send(data.encode())
    data = s.recv(1024 * 1024).decode()
    return json.loads(data)


class HTTPServer:
    def __init__(self):
        self.address = ADDR
        self.create_socket()
        self.bind()

    def create_socket(self):
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, DEBUG)

    def bind(self):
        self.sockfd.bind(self.address)
        self.ip = self.address[0]
        self.port = self.address[1]

    def serve_forever(self):
        self.sockfd.listen(3)
        print("Listen the port %d" % self.port)
        while True:
            connfd, addr = self.sockfd.accept()
            print("Connect from", addr)
            client = Thread(target=self.handle, args=(connfd,))
            client.setDaemon(True)
            client.start()

    # 处理浏览器请求
    def handle(self, connfd):
        request = connfd.recv(4096).decode()
        pattern = r"(?P<method>[A-z]+)\s+(?P<info>/\S*)"
        try:
            env = re.match(pattern, request).groupdict()
        except:
            connfd.close()
            return
        else:
            data=connect_frame(env)
            if data:
                self.response(connfd,data)

    def response(self,connfd,data):
        if data["status"] == '200':
            responseHeaders = "HTTP/1.1 200 OK\r\n"
            responseHeaders += "Content-Type:text/html\r\n"
            responseHeaders += '\r\n'
            responseBody = data["data"]
        elif data['status'] == '404':
            responseHeaders = "HTTP/1.1 404 Not Found\r\n"
            responseHeaders += "Content-Type:text/html\r\n"
            responseHeaders += '\r\n'
            responseBody = data["data"]
        elif data['status'] == '500':
            pass

        response_data =responseHeaders+responseBody
        connfd.send(response_data.encode())


httpd = HTTPServer()
httpd.serve_forever()
