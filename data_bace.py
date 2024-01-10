__author__ = 'Gur'

import sqlite3
from sqlite3 import Error
import os
import json
import hashlib


DB_FILE_NAME = os.path.dirname(os.path.abspath(__file__)) + '\\' + 'pumpkin_data_base.db'

CREATE_GENERAL_TABLE_SQL = """ CREATE TABLE IF NOT EXISTS general (
                                        user_name text PRIMARY KEY,
                                        password text
                                        ); """

CREATE_FRIENDS_TABLE_SQL = """ CREATE TABLE IF NOT EXISTS friends (
                                        current_user text,
                                        friend text,
                                        PRIMARY KEY(current_user, friend)
                                        FOREIGN KEY (current_user, friend) REFERENCES general(user_name, user_name)
                                        ); """

CREATE_ALERTS_TABLE_SQL = """ CREATE TABLE IF NOT EXISTS user_data (
                                        user_name text PRIMARY KEY,
                                        alerts text,
                                        waiting_friend_requests text,
                                        FOREIGN KEY(user_name) REFERENCES general(user_name)
                                        ); """ # The alerts is json -> [[string, [string(*args)]]]
                                               # The waiting_friend_requests_users_list is json -> []

ALERTS_OBJECT = []                 # list
WAITING_FRIEND_REQUESTS_OBJECT = []# list

CREATE_TABLES = [CREATE_GENERAL_TABLE_SQL, CREATE_FRIENDS_TABLE_SQL, CREATE_ALERTS_TABLE_SQL]


class Pumpkin_Database():

    def __init__(self):

        self.conn = self.create_connection()
        self.cur = self.conn.cursor()
        self.create_tables()

    def create_connection(self):
        """
        Create a database connection to the pumpkin database
        specified by db_file
        :param db_file: database file
        :return: Connection object
        """
        conn = sqlite3.connect(DB_FILE_NAME)
        return conn

    def create_tables(self):
        """
        Create all the tables in the database
        if they do not exist
        :return:
        """
        for table in CREATE_TABLES:
            self.cur.execute(table)
        self.conn.commit()

    def get_password(self, user_name):
        """
        :param user_name: the user_name of user to
        get the requested password
        :return: return the password of the requested user
                *if this user name does not exist returns None
        """
        try:
            self.cur.execute('SELECT * FROM general WHERE user_name=?', (user_name,))
            return self.cur.fetchall()[0][1]
        except:
            return None

    def add_account(self, user_name, password):
        """
        Add an account to the database
        :param user_name: new user's user_name
        :param password: new user's password
        :return: if the account was added successfully
        :rtype: bool
        """
        sql_general = ''' INSERT INTO general(user_name, password)
                          VALUES(?,?) '''
        sql_user_data = ''' INSERT INTO user_data(user_name, alerts, waiting_friend_requests)
                            VALUES(?,?,?) '''

        md5_password = hashlib.md5(password).hexdigest()

        try:
            self.cur.execute(sql_general, (user_name, md5_password))
            self.conn.commit()
            self.cur.execute(sql_user_data, (user_name, json.dumps(ALERTS_OBJECT), json.dumps(WAITING_FRIEND_REQUESTS_OBJECT)))
            self.conn.commit()
            return True
        except:
            return False

    def is_user_name_exist(self, user_name):
        """
        Checks if the inserted user_name exist
        :param user_name: checked user name
        :return: True if exist False if not
        """
        general_list = self.get_general_table()
        while general_list:
            if user_name == general_list[0][0]:
                return True
            del general_list[0]

        return False

    def exist_user(self, user_name, password):
        """
        Checks if the requested user name exist and
        if the requested password is equals to the requested
        user's password (Check if this user with this password
        and user name is exist).
        :param user_name: the requested user name.
        :param password: the requested password
        :return: True if exist False if not
        :rtype: bool
        """

        md5_password = hashlib.md5(password).hexdigest()
        real_password = self.get_password(user_name)

        if real_password and real_password == md5_password:
            return True
        return False

    def is_password_exists(self, password):
        """
        Checks if the inserted password exists
        :param password: checked password
        :return: True if exist False if not
        """
        general_list = self.get_general_table()

        md5_password = hashlib.md5(password).hexdigest()

        while general_list:
            if md5_password == general_list[0][1]:
                return True
            del general_list[0]

        return False

    def get_general_table(self):
        """
        Returns the general table.
        :return: the general table.
        """
        self.cur.execute('SELECT * FROM general')
        return self.cur.fetchall()

    def get_friends_table(self):
        """
        Returns the friends table.
        :return:  the friends table
        """
        self.cur.execute('SELECT * FROM friends')
        return self.cur.fetchall()

    def get_user_data_table(self):
        """
        Returns the user_data table.
        :return: the user_data table
        """
        self.cur.execute('SELECT * FROM user_data')
        return self.cur.fetchall()

    def get_user_friends(self, user_name):
        """
        Gets the requested user friends users.
        :param user_name: the requested user name.
        :return: the user friends users.
        :rtype: list[]
        """
        friends_list = self.get_friends_table()
        current_user_friends_list = []
        for friends in friends_list:
            if user_name == friends[0]:
                current_user_friends_list.append(friends[1])
            elif user_name == friends[1]:
                current_user_friends_list.append(friends[0])
        return current_user_friends_list

    def add_friends(self, user_name, friend_name):
        """
        Add user and his friend to the friends table.
        :param user_name: the requested user name.
        :param friend_name: the requested friend name.
        :return: if the action succeeded
        :rtype: bool
        """
        sql = ''' INSERT INTO friends(current_user, friend)
                  VALUES(?,?) '''
        try:
            self.cur.execute(sql, (user_name, friend_name))
            self.conn.commit()
            return True
        except:
            return False

    def remove_friends(self, user_name, friend_name):
        """
        Remove the requested friends from friends list.
        :return: if the action succeeded
        :rtype: bool
        """
        sql = 'DELETE FROM friends WHERE current_user=? and friend=?'
        try:
            self.cur.execute(sql, (user_name, friend_name))
            self.conn.commit()
            return True
        except:
            return False

    def get_user_alerts(self, user_name):
        """
        Returns the alerts of the requested user name.
        :param user_name: the requested user name.
        :return: dict of alerts
        :rtype: list[[string, [string(*args)]]]
        """
        try:
            self.cur.execute('SELECT * FROM user_data WHERE user_name=?', (user_name, ))
            user_data = self.cur.fetchall()
            user_alerts = json.loads(user_data[0][1])
            return user_alerts
        except:
            return None

    def set_alerts(self, user_name, alerts):
        """
        Sets the alerts dict of a requested user.
        :param user_name: the requested user name.
        :param alerts: the alert dict.
        :return: if the action succeeded
        :rtype: bool
        """
        sql = ''' UPDATE user_data SET alerts=? WHERE user_name=?'''
        try:
            self.cur.execute(sql, (alerts, user_name))
            self.conn.commit()
            return True
        except:
            return False

    def alert_exist(self, user_name, alert_list):
        """
        Checks if the requested alert is exist.
        :param user_name: the requested user name to check.
        :param alert_list: alert in the list form.
        :return: if the alert exists
        :rtype: bool
        """
        user_alerts = self.get_user_alerts(user_name)
        json_alert_list = json.dumps(alert_list)
        for alert in user_alerts:
            if json.dumps(alert) == json_alert_list:
                return True
        return False

    def add_alert(self, user_name, alert, args_list=None):
        """
        Add alert to a requested user.
        :param user_name: the requested user name.
        :param alert: the alert to the requested user name.
        :param *args: the args of the alert
        :return: if the action succeeded.
        :rtype: bool
        """
        if args_list:
            new_alert = [alert, args_list]
        else:
            new_alert = [alert, []]

        if not self.alert_exist(user_name, new_alert):
            user_alerts = self.get_user_alerts(user_name)
            user_alerts.append(new_alert)
            if self.set_alerts(user_name, json.dumps(user_alerts)):
                return True

        return False

    def remove_user_alerts(self, user_name):
        """
        Remove the alerts of the requested user name.
        :param user_name: the requested user name.
        :return: if the action succeeded
        :rtype: bool
        """
        if self.set_alerts(user_name, json.dumps(ALERTS_OBJECT)):
            return True
        return False

    def remove_alert(self, user_name, alert):
        """
        Remove a requested alert.
        :param user_name: the requested user name of the alert.
        :param alert: the requested alert of the alert.
        :return: if the action succeeded
        :rtype: bool
        """
        pass

    def get_user_waiting_friend_requests(self, user_name):
        """
        Returns the user waiting friend requests list.
        :param user_name: the requested user name.
        :return: waiting friend requests list.
        :rtype: list[]
        """
        try:
            self.cur.execute('SELECT * FROM user_data WHERE user_name=?', (user_name, ))
            user_data = self.cur.fetchall()
            user_waiting_friend_requests = json.loads(user_data[0][2])
            return user_waiting_friend_requests
        except:
            return None

    def set_user_waiting_friend_requests(self, user_name, waiting_friend_requests):
        """
        Sets the user waiting friend requests list.
        :param user_name: the requested user name.
        :param waiting_friend_requests: the waiting friend requests (as json text).
        :return: if the action succeeded
        :rtype: bool
        """
        sql = ''' UPDATE user_data SET waiting_friend_requests=? WHERE user_name=?'''
        try:
            self.cur.execute(sql, (waiting_friend_requests, user_name))
            self.conn.commit()
            return True
        except:
            return False

    def add_waiting_friend_request(self, user_name, requested_user_name):
        """
        Adds the requested user name to the waiting
        friend request list.
        :param user_name: the current user (the user which sent the
        friend request and wait for answer).
        :param requested_user_name: the user name of the user
        which need to give answer to the current user.
        :return: if the action succeeded.
        :rtype: bool
        """
        user_waiting_friend_requests = self.get_user_waiting_friend_requests(user_name)
        user_waiting_friend_requests.append(requested_user_name)
        if self.set_user_waiting_friend_requests(user_name, json.dumps(user_waiting_friend_requests)):
            return True
        else:
            return False

    def remove_waiting_friend_request(self, user_name, requested_user_name):
        """
        Removes the requested user name from the waiting
        friend request list.
        :param user_name: the current user (the user which sent the
        friend request and wait for answer).
        :param requested_user_name: the user name of the user
        which need to give answer to the current user.
        :return: if the action succeeded.
        :rtype: bool
        """
        user_waiting_friend_requests = self.get_user_waiting_friend_requests(user_name)
        user_waiting_friend_requests.remove(requested_user_name)
        if self.set_user_waiting_friend_requests(user_name, json.dumps(user_waiting_friend_requests)):
            return True
        else:
            return False