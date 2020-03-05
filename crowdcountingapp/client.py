# encoding: utf-8
import threading
import socket
from presenter_types import *


SEND_BUF_SIZE = 102400
RECV_BUF_SIZE = 102400


class PresenterSocketClient(object):
    def __init__(self, server_address, reconnectiontime=5,recvCallback=None):
        self._server_address = server_address
        self._reconnectiontime = reconnectiontime
        self.__recvCallback = recvCallback
        self._sock_client = None
        self._bstart = True
        # threading.Thread(target=self.start_connect()).start()

    def start_connect(self):
        print("创建socket对象...")
        self._sock_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock_client.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, SEND_BUF_SIZE)
        self._sock_client.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, RECV_BUF_SIZE)
        try:
            print("连接服务器...")
            self._sock_client.connect(self._server_address)
        except Exception as e:
            print(e)
            self.close()
            #print("正在重新连接...")
            #time.sleep(self._reconnectiontime)
            #self.start_connect()
            return
        self._bstart = True
        print("监听数据接受中...")
        threading.Thread(target=self.__start_listenning()).start()

    def __start_listenning(self):
        while self._bstart:
            try:
                # print("等待数据到达...")
                data = self._sock_client.recv(RECV_BUF_SIZE)
                if data:
                    if self.__recvCallback:
                        self.__recvCallback(data)
                    #print(data)
                    # self.send_data("hello".encode())
                else:
                    print("close")
                    self.close()
                    #self._sock_client.close()
                    #self.start_connect()
                    break
            except Exception as e:
                print(e)
                self.close()
                #self._sock_client.close()
                #self.start_connect()
                break

    def send_data(self, data):
	# print(data)
        self._sock_client.sendall(data)

    def close(self):
        self._bstart = False
        self._sock_client.shutdown(socket.SHUT_RDWR)
        self._sock_client.close()


class Head(object):
    def __init__(self):
        self.left = None
        self.right = None

class Node(object):
    def __init__(self, value):
        self.value = value
        self.next = None

class Queue(object):
    def __init__(self):
        #初始化节点
        self.head = Head()
        self.count = 0

    def put(self, value):
        #插入一个元素
        if self.count > 3:
            return
        newnode = Node(value)
        p = self.head
        if p.right:
            #如果head节点的右边不为None
            #说明队列中已经有元素了
            #就执行下列的操作
            temp = p.right
            p.right = newnode
            temp.next = newnode
            self.count += 1
        else:
            #这说明队列为空，插入第一个元素
            p.right = newnode
            p.left = newnode
            self.count += 1

    def get(self):
        #取出一个元素
        p = self.head
        if p.left and (p.left == p.right):
            #说明队列中已经有元素
            #但是这是最后一个元素
            temp = p.left
            p.left = p.right = None
            self.count -= 1
            return temp.value
        elif p.left and (p.left != p.right):
            #说明队列中有元素，而且不止一个
            temp = p.left
            p.left = temp.next
            self.count -= 1
            return temp.value

    def is_empty(self):
        if self.head.left:
            return False
        else:
            return True

    def top(self):
        #查询目前队列中最早入队的元素
        if self.head.left:
            return self.head.left.value
