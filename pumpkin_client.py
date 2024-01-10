__author__ = 'Gur'

import socket
import select


SYSTEM_SERVER_ADDRESS = ('127.0.0.1', 1234)
RECEIVE_HEADER_LENGTH = 3
DATA_LENGTH_SIZE = 5


class Pumpkin_client():

    def __init__(self):

        self.client_socket = self.build_client_socket()

    def build_client_socket(self):

        client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client_socket.connect(SYSTEM_SERVER_ADDRESS)

        return client_socket

    def send_data_and_receive(self, data_lst):

        data_list = []

        self.client_socket.send(data_lst[0])
        del data_lst[0]

        for data in data_lst:
            self.client_socket.send(str(len(data)).ljust(DATA_LENGTH_SIZE))
            self.client_socket.send(data)

        data_parts_length = self.receive_data(self.client_socket, DATA_LENGTH_SIZE)
        for i in xrange(int(data_parts_length)):
            data_list.append(self.receive_length_and_data(self.client_socket))

        return data_list

    def receive_length_and_data(self, current_socket):

        '''Receive length of data and than
        receive only the requested data.
        (for ex. receives data length 10 the function
         receives 10 ?bytes? from client)'''

        len_data = self.receive_data(current_socket, DATA_LENGTH_SIZE)
        data = self.receive_data(current_socket, int(len_data))
        return data

    def receive_data(self, current_socket, count):

        '''This function gets length of data and
        receive only the requested data.
        (for ex. if the data length is 10 the function
         receives 10 ?bytes? from client)'''

        buf = b''
        while count:
            new_buf = current_socket.recv(count)
            if not new_buf:
                return None
            buf += new_buf
            count -= len(new_buf)
        return buf

    def send_data(self, data_lst):

        self.client_socket.send(data_lst[0])
        del data_lst[0]

        for data in data_lst:
            self.client_socket.send(str(len(data)).ljust(DATA_LENGTH_SIZE))
            self.client_socket.send(data)

    def main_screen_data_receiving(self):

        data_list = []

        rlist, wlist, xlist = select.select([self.client_socket], [], [], 0)

        if rlist:
            data_parts_length = self.receive_data(self.client_socket, DATA_LENGTH_SIZE)
            for i in xrange(int(data_parts_length)):
                data_list.append(self.receive_length_and_data(rlist[0]))

        return data_list