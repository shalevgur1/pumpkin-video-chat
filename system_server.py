
#Data base class.
from data_bace import Pumpkin_Database
from server_class import Server_management

import socket
import select
import json
import re


MAIN_ADDRESS = ('0.0.0.0', 1234)
CLIENTS_TO_LISTEN = 10

WAIT = True
HEADER_RECEIVE_SIZE = 3
DATA_LENGTH_SIZE = 5

#Command headers
LOGIN_HEADER = 'LOG'
SIGN_UP_HEADER = 'SIN'
FRIEND_REQUEST_HEADER = 'FRE'
CALL_HEADER = 'CAL'
EXIT_HEADER = 'EXT'

DATA_BASE_OBJECT = Pumpkin_Database()
SERVER_OBJECT = Server_management()


#send headers login:
LOGIN_ERROR_INCORRECT = 'INC'    #Incorrenct password or user name
LOGIN_PERMISSION = 'PER'         #The user name and password is correct
#send headers sign up:
SIGN_ERROR_EXIST_USER = 'USR'    #The user name already exists
SIGN_ERROR_EXIST_PASSWORD = 'PAS'#The password already exists
SIGN_ERROR_NOT_VALID_PASSWORD = 'NVP' #The requested users password is not valid
SIGN_PERMISSION = 'PER'          #The user name and password does not exists
#send headers main screen:
FRIEND_REQUEST_ERROR_NOT_EXIST = 'FNE'   #The requested friend user name does not exists
FRIEND_REQUEST_PERMISSION = 'FRP'        #The requested friend exists  -> send a friend request (this is permission which being sent to the applicant)
FRIEND_REQUEST_ACCEPT = 'FRA'            #The friend request accepted
FRIEND_REQUEST_REJECT = 'FRR'            #The friend request rejected
FRIEND_REQUEST_ALREADY_SENT_NO_RESPONSE = 'FAN'   #A friend request as been already sent to user form same user and he did not responed yet.
USER_TO_CALL_NOT_CONNECTED = 'UNC'       #The called user is not connected
FRIEND_ALREADY_IN_CALL = 'FAC'           #The requested friend to call to is already in a call
YOU_ALREADY_IN_CALL = 'UAC'              #The caller is already in a call and he can not call to another friend
CALL_PERMISSION = 'CAP'                  #Permission to user which called
CALL_REQUEST_STOP = 'CRS'                #The call request has been stopped or refused by one of the two sides
START_CALL = 'SCL'                       #The user press the green call button after another user called him


#Register valid constants
PASSWORD_VALID_LEN = 6



def receive_data(current_socket, count):

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


def receive_length_and_data(current_socket):

    '''Receive length of data and than
    receive only the requested data.
    (for ex. receives data length 10 the function
     receives 10 ?bytes? from client)'''

    len_data = receive_data(current_socket, DATA_LENGTH_SIZE)
    data = receive_data(current_socket, int(len_data))
    return data




def check_register_valid(user_name, password):

    if len(password) < PASSWORD_VALID_LEN:
        return False, SIGN_ERROR_NOT_VALID_PASSWORD

    elif not (re.search('[0-9]', password) and re.search('[a-z]', password)):
        return False, SIGN_ERROR_NOT_VALID_PASSWORD

    return True, ''



def handle_data(current_socket, header):
    data_to_send = []#[(None, None, None)]

    if header == LOGIN_HEADER:
        user_name = receive_length_and_data(current_socket)
        password = receive_length_and_data(current_socket)

        if DATA_BASE_OBJECT.exist_user(user_name, password):
            SERVER_OBJECT.login_user(user_name, current_socket)
            user_friends_list = DATA_BASE_OBJECT.get_user_friends(user_name)
            user_friends_str = '\n'.join(user_friends_list)
            user_alerts = DATA_BASE_OBJECT.get_user_alerts(user_name)
            json_user_alerts = json.dumps(user_alerts)
            data_to_send.append((current_socket, [current_socket], [LOGIN_PERMISSION, user_friends_str, json_user_alerts]))
            DATA_BASE_OBJECT.remove_user_alerts(user_name)
        else:
            data_to_send.append((current_socket, [current_socket], [LOGIN_ERROR_INCORRECT]))

    elif header == SIGN_UP_HEADER:
        user_name = receive_length_and_data(current_socket)
        password = receive_length_and_data(current_socket)

        #If real_password is empty so the user name does not exist
        real_password = DATA_BASE_OBJECT.get_password(user_name)

        if not real_password:
            '''The user_name does not exist'''
            valid, validate_error = check_register_valid(user_name, password)
            if valid:
                '''The password and user name are valid'''
                if not DATA_BASE_OBJECT.is_password_exists(password):
                    '''The password does not exist'''
                    DATA_BASE_OBJECT.add_account(user_name, password)
                    data_to_send.append((current_socket, [current_socket], [SIGN_PERMISSION]))
                else:
                    '''The password exists'''
                    data_to_send.append((current_socket, [current_socket], [SIGN_ERROR_EXIST_PASSWORD]))
            else:
                '''The password or user name are not valid'''
                data_to_send.append((current_socket, [current_socket], [validate_error]))
        else:
            '''The user name exists'''
            data_to_send.append((current_socket, [current_socket], [SIGN_ERROR_EXIST_USER]))

    elif header == FRIEND_REQUEST_HEADER:
        friend_user_name = receive_length_and_data(current_socket)
        current_user_name = SERVER_OBJECT.get_user_name_by_socket(current_socket)

        if not DATA_BASE_OBJECT.is_user_name_exist(friend_user_name):
            '''Friend user name does not exsist'''
            data_to_send.append((current_socket, [current_socket], [FRIEND_REQUEST_ERROR_NOT_EXIST]))
        elif friend_user_name in DATA_BASE_OBJECT.get_user_waiting_friend_requests(current_user_name):
            '''A friend request as been already sent to the friend user'''
            data_to_send.append((current_socket, [current_socket], [FRIEND_REQUEST_ALREADY_SENT_NO_RESPONSE, friend_user_name]))
        else:
            '''Friend exists -> sending friend request'''
            data_to_send.append((current_socket, [current_socket], [FRIEND_REQUEST_PERMISSION]))
            friend_socket = SERVER_OBJECT.get_socket_by_user_name(friend_user_name)
            if friend_socket:
                data_to_send.append((current_socket, [friend_socket], [FRIEND_REQUEST_HEADER, current_user_name]))
            else:
                DATA_BASE_OBJECT.add_alert(friend_user_name, header, [current_user_name])
            DATA_BASE_OBJECT.add_waiting_friend_request(current_user_name, friend_user_name)

    elif header == FRIEND_REQUEST_ACCEPT:
        friend_user_name = receive_length_and_data(current_socket)
        friend_socket = SERVER_OBJECT.get_socket_by_user_name(friend_user_name)
        current_user_name = SERVER_OBJECT.get_user_name_by_socket(current_socket)
        DATA_BASE_OBJECT.add_friends(friend_user_name, current_user_name)
        DATA_BASE_OBJECT.remove_waiting_friend_request(friend_user_name, current_user_name)
        if friend_socket:
            data_to_send.append((current_socket, [friend_socket], [FRIEND_REQUEST_ACCEPT, current_user_name]))
        else:
            DATA_BASE_OBJECT.add_alert(friend_user_name, header, [current_user_name])

    elif header == FRIEND_REQUEST_REJECT:
        friend_user_name = receive_length_and_data(current_socket)
        current_user_name = SERVER_OBJECT.get_user_name_by_socket(current_socket)
        friend_socket = SERVER_OBJECT.get_socket_by_user_name(friend_user_name)
        DATA_BASE_OBJECT.remove_waiting_friend_request(friend_user_name, current_user_name)
        if friend_socket:
            data_to_send.append((current_socket, [friend_socket], [FRIEND_REQUEST_REJECT, current_user_name]))
        else:
            DATA_BASE_OBJECT.add_alert(friend_user_name, header, [current_user_name])

    elif header == CALL_HEADER:
        friend_user_name = receive_length_and_data(current_socket)
        friend_socket = SERVER_OBJECT.get_socket_by_user_name(friend_user_name)
        current_user_name = SERVER_OBJECT.get_user_name_by_socket(current_socket)
        current_ip = SERVER_OBJECT.get_user_ip_by_user_name(current_user_name)
        if friend_socket:
            if SERVER_OBJECT.is_user_in_call(current_user_name):
                data_to_send.append((current_socket, [current_socket], [YOU_ALREADY_IN_CALL]))
            elif SERVER_OBJECT.is_user_in_call(friend_user_name):
                data_to_send.append((current_socket, [current_socket], [FRIEND_ALREADY_IN_CALL, friend_user_name]))
            else:
                SERVER_OBJECT.make_in_call_state(current_user_name, friend_user_name)
                data_to_send.append((current_socket, [current_socket], [CALL_PERMISSION, friend_user_name]))
                data_to_send.append((current_socket, [friend_socket], [CALL_HEADER, current_user_name, current_ip]))
        else:
            data_to_send.append((current_socket, [current_socket], [USER_TO_CALL_NOT_CONNECTED, friend_user_name]))

    elif header == CALL_REQUEST_STOP:
        current_user_name = SERVER_OBJECT.get_user_name_by_socket(current_socket)
        friend_user_name = SERVER_OBJECT.get_call_friend_user_name(current_user_name)
        friend_socket = SERVER_OBJECT.get_socket_by_user_name(friend_user_name)
        data_to_send.append((current_socket, [friend_socket], [CALL_REQUEST_STOP]))
        SERVER_OBJECT.stop_call_by_user_name(current_user_name)

    elif header == START_CALL:
        current_user_name = SERVER_OBJECT.get_user_name_by_socket(current_socket)
        current_ip = SERVER_OBJECT.get_user_ip_by_user_name(current_user_name)
        friend_user_name = SERVER_OBJECT.get_call_friend_user_name(current_user_name)
        friend_socket = SERVER_OBJECT.get_socket_by_user_name(friend_user_name)
        data_to_send.append((current_socket, [friend_socket], [START_CALL, current_ip]))


    if data_to_send:
        SERVER_OBJECT.add_data_to_send_list(data_to_send)




def handle_sending(wlist):
    temp_list = []
    for data_to_send in SERVER_OBJECT.get_data_to_send():

        (sender_socket, receiver_socket, data) = data_to_send

        for user_socket in receiver_socket:

            if user_socket in wlist:
                data_parts_length = str(len(data)).ljust(DATA_LENGTH_SIZE)
                user_socket.send(data_parts_length)
                for data_part in data:
                    data_length = str(len(data_part)).ljust(DATA_LENGTH_SIZE)
                    user_socket.send(data_length)
                    user_socket.send(data_part)

                wlist.remove(user_socket)
                receiver_socket.remove(user_socket)

        if receiver_socket:
            temp_list.append((sender_socket, receiver_socket, data))

    SERVER_OBJECT.set_data_to_send(temp_list)



def main():
    global WAIT

    main_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    main_socket.bind(MAIN_ADDRESS)
    main_socket.listen(CLIENTS_TO_LISTEN)

    while WAIT:
        rlist, wlist, xlist = select.select([main_socket] + SERVER_OBJECT.get_entry_users_sockets() + SERVER_OBJECT.get_online_users_sockets(),
                                            SERVER_OBJECT.get_entry_users_sockets() + SERVER_OBJECT.get_online_users_sockets(),
                                            [], 0)
        for current_socket in rlist:

            if current_socket is main_socket:
                #Open new socket with new user
                (new_socket, address) = main_socket.accept()
                print "New connection.........."
                SERVER_OBJECT.add_entry_user(new_socket, address)

            else:
                #Receive new information from clients

                header = receive_data(current_socket, HEADER_RECEIVE_SIZE)

                if header:
                    handle_data(current_socket, header)
                elif not header or header == EXIT_HEADER:
                    #Connection was lost -> close connection
                    SERVER_OBJECT.close_user_connection(current_socket, CALL_REQUEST_STOP)
                    print "Connection lost.........."

        handle_sending(wlist)




if __name__ == '__main__':
    main()


#print SERVER_OBJECT.get_online_users()
#print SERVER_OBJECT.get_entry_users()
#print SERVER_OBJECT.get_data_to_send()