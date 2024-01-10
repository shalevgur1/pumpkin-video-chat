__author__ = 'Gur'

import socket

class Connected_user:
    """
    This class is represent a connected user.
    """

    def __init__(self, user_name, user_socket, user_address):
        """
        Build connected user.
        :param user_name: the connected user's user name.
        :param user_socket: the connected user's socket.
        :param user_address: the connected user's address.
        """

        self.user_name = user_name
        self.user_socket = user_socket
        self.user_address = user_address

    def get_user_name(self):
        """
        Returns the connected user's user name.
        :return: user name.
        :rtype: str
        """
        return self.user_name

    def get_user_socket(self):
        """
        Returns the connected user's socket.
        :return: user socket.
        :rtype: socket object
        """
        return self.user_socket

    def get_user_address(self):
        """
        Returns the connected user's address.
        :return: user address.
        :rtype: tuple
        """
        return self.user_address

    def set_user_name(self, user_name):
        """
        Sets the connected user's user name.
        :param user_name: the requested user name.
        """
        self.user_name = user_name

    def set_user_socket(self, user_socket):
        """
        Sets the connected user's socket.
        :param user_socket: the requested user socket.
        """
        self.user_socket = user_socket

    def set_user_address(self, user_address):
        """
        Sets the connected user's address.
        :param user_address: the requested user address.
        """
        self.user_address = user_address