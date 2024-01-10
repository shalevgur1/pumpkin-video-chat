__author__ = 'Gur'

import socket
from con_user import Connected_user

class Server_management:

    def __init__(self):

        self.data_to_send = []
        self.entry_users = []
        self.online_users = []
        self.waiting_for_or_in_call = [] # list[tuple(,)]


    def get_data_to_send(self):
        return self.data_to_send

    def get_entry_users(self):
        return self.entry_users

    def get_online_users(self):
        return self.online_users

    def get_waiting_for_or_in_call(self):
        return self.waiting_for_or_in_call


    def set_data_to_send(self, data_to_send):
        self.data_to_send = data_to_send

    def set_entry_users(self, entry_users):
        self.entry_users = entry_users

    def set_online_users(self, online_users):
        self.online_users = online_users

    def set_waiting_for_or_in_call(self, waiting_for_or_in_call):
        self.waiting_for_or_in_call = waiting_for_or_in_call


    def add_data_to_send(self, data):
        self.data_to_send.append(data)

    def add_entry_user(self, user_socket, user_address):
        user = Connected_user('', user_socket, user_address)
        self.entry_users.append(user)

    def add_online_user(self, user_name, user_socket, user_address):
        user = Connected_user(user_name, user_socket, user_address)
        self.online_users.append(user)

    def make_in_call_state(self, user_name, friend_user_name):
        user = self.get_user_by_user_name(user_name)
        friend_user = self.get_user_by_user_name(friend_user_name)
        self.waiting_for_or_in_call.append((user, friend_user))


    def add_data_to_send_list(self, data_to_send):
        self.data_to_send += data_to_send


    def remove_from_entry_users(self, user_socket):

        for user in self.entry_users:
            if user_socket == user.get_user_socket():
                self.entry_users.remove(user)
                break

    def remove_from_online_users(self, user_socket):

        for user in self.online_users:
            if user_socket == user.get_user_socket():
                self.online_users.remove(user)
                break

    def stop_call_by_user_name(self, user_name):

        for users_tuple in self.waiting_for_or_in_call:
            for user in users_tuple:
                if user_name == user.get_user_name():
                    self.waiting_for_or_in_call.remove(users_tuple)
                    break


    def is_user_in_call(self, user_name):

        for users_tuple in self.waiting_for_or_in_call:
            for user in users_tuple:
                if user_name == user.get_user_name():
                    return True

        return False

    def get_call_friend_user_name(self, user_name):

        for users_tuple in self.waiting_for_or_in_call:
            for i in xrange(len(users_tuple)):
                if user_name == users_tuple[i].get_user_name():
                    if i == 0:
                        return users_tuple[1].get_user_name()
                    else:
                        return users_tuple[0].get_user_name()

        return None


    def get_socket_by_user_name(self, user_name):

        for user in self.online_users:
             if user_name == user.get_user_name():
                 return user.get_user_socket()

        return None


    def get_user_name_by_socket(self, user_socket):

        for user in self.online_users:
            if user_socket == user.get_user_socket():
                return user.get_user_name()

        return None

    def get_user_address_by_socket(self, user_socket): #only for entry_users

        for user in self.entry_users:
            if user_socket == user.get_user_socket():
                return user.get_user_address()

        return None

    def get_user_address_by_user_name(self, user_name):

        for user in self.online_users:
            if user_name == user.get_user_name():
                return user.get_user_address()

        return None

    def get_user_by_user_name(self, user_name):

        for user in self.online_users:
            if user_name == user.get_user_name():
                return user

    def login_user(self, user_name, user_socket):

        user_address = self.get_user_address_by_socket(user_socket)
        self.add_online_user(user_name, user_socket, user_address)
        self.remove_from_entry_users(user_socket)


    def get_entry_users_sockets(self):

        socket_lst = []
        for entry_user in self.entry_users:
            socket_lst.append(entry_user.get_user_socket())

        return socket_lst


    def get_online_users_sockets(self):

        socket_lst = []
        for online_user in self.online_users:
            socket_lst.append(online_user.get_user_socket())

        return socket_lst


    def remove_user_socket_from_data_to_send(self, user_socket):

        remove_data = []
        for data_index in xrange(len(self.data_to_send)):
            data = self.data_to_send[data_index]
            if data[0] == user_socket:
                remove_data.append(data)
            elif user_socket in data[1]:
                self.data_to_send[data_index][1].remove(user_socket)

        for data in remove_data:
            self.data_to_send.remove(data)


    def stop_call_request(self, user_socket, CALL_REQUEST_STOP):

        if self.is_user_in_call(self.get_user_name_by_socket(user_socket)):
            current_user_name = self.get_user_name_by_socket(user_socket)
            friend_user_name = self.get_call_friend_user_name(current_user_name)
            friend_socket = self.get_socket_by_user_name(friend_user_name)
            self.data_to_send.append((friend_socket, [friend_socket], [CALL_REQUEST_STOP]))
            self.stop_call_by_user_name(current_user_name)


    def get_user_ip_by_user_name(self, user_name):

        return self.get_user_address_by_user_name(user_name)[0]


    def close_user_connection(self, user_socket, CALL_REQUEST_STOP):

        self.stop_call_request(user_socket, CALL_REQUEST_STOP)
        self.remove_from_entry_users(user_socket)
        self.remove_from_online_users(user_socket)
        self.remove_user_socket_from_data_to_send(user_socket)
        user_socket.close()
