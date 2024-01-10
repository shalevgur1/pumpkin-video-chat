

"""
This file is one of the main files of the application.
This file handles the GUI.
This file is the main file which use the all other files.
"""


#Handle the initial size
from kivy.config import Config
Config.set('graphics', 'width', '1148')
Config.set('graphics', 'height', '626')
Config.set('graphics', 'resizable', True)
#Config.write()

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
import kivy.uix.gridlayout as GridLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.graphics.texture import Texture
from kivy.uix.relativelayout import RelativeLayout


import os
import time
import json
import cv2
import socket
import thread
import threading


from pumpkin_client import Pumpkin_client
from video import Video
from audio import Audio



#Constants:

#Screens names
LOGIN_SCREEN_NAME = 'login_screen'
REGISTER_SCREEN_NAME = 'register_screen'
MAIN_SCREEN_NAME = 'main_screen'
CALL_SCREEN_NAME = 'call_screen'

FIRST_SCREEN_NAME = 'login_screen'



#The object which handle the connection with server
#(send and receive data)
CLIENT_OBJECT = Pumpkin_client()





#The images data

IMAGES_FILE = 'gui_images'

#Login screen images path
LOGIN_SCREEN_IMAGES_FILE = 'login_screen'

LOGIN_SCREEN_IMG_NAME = 'login_screen.jpg'
LOGIN_SCREEN_IMG_PATH = os.path.dirname(os.path.abspath(__file__)) + '\\' + IMAGES_FILE + '\\' + LOGIN_SCREEN_IMAGES_FILE + '\\' + LOGIN_SCREEN_IMG_NAME



#Rregiste screen images path
REGISTER_SCREEN_IMAGES_FILE = 'register_screen'

REGISTER_SCREEN_IMG_NAME = 'sine_up_screen_1.jpg'
REGISTER_SCREEN_IMG_PATH = os.path.dirname(os.path.abspath(__file__)) + '\\' + IMAGES_FILE + '\\' + REGISTER_SCREEN_IMAGES_FILE + '\\' + REGISTER_SCREEN_IMG_NAME



#Main screen images path
MAIN_SCREEN_IMAGES_FILE = 'main_screen'

MESSAGES_IMAGE_NAME = 'messages_part.png'    #'messages_img.jpg'     'farmer9.jpg'
MESSAGES_IMAGE_PATH = os.path.dirname(os.path.abspath(__file__)) + '\\' + IMAGES_FILE + '\\' + MAIN_SCREEN_IMAGES_FILE + '\\' + MESSAGES_IMAGE_NAME
CALL_PART_IMAGE_NAME = 'call_part.png'
CALL_PART_IMAGE_PATH = os.path.dirname(os.path.abspath(__file__)) + '\\' + IMAGES_FILE + '\\' + MAIN_SCREEN_IMAGES_FILE + '\\' + CALL_PART_IMAGE_NAME
CALL_BUTTON_IMAGE_NAME = 'call_button2.png'
CALL_BUTTON_IMAGE_PATH = os.path.dirname(os.path.abspath(__file__)) + '\\' + IMAGES_FILE + '\\' + MAIN_SCREEN_IMAGES_FILE + '\\' + CALL_BUTTON_IMAGE_NAME
CALL_BUTTON_PRESSED_IMAGE_NAME = 'call_button3.png'
CALL_BUTTON_PRESSED_IMAGE_PATH = os.path.dirname(os.path.abspath(__file__)) + '\\' + IMAGES_FILE + '\\' + MAIN_SCREEN_IMAGES_FILE + '\\' + CALL_BUTTON_PRESSED_IMAGE_NAME
ADD_FRIEND_PART_IMAGE_NAME = 'add_friend_part.png'    #'messages_img.jpg'     'farmer9.jpg'
ADD_FRIEND_PART_IMAGE_PATH = os.path.dirname(os.path.abspath(__file__)) + '\\' + IMAGES_FILE + '\\' + MAIN_SCREEN_IMAGES_FILE + '\\' + ADD_FRIEND_PART_IMAGE_NAME
ADD_FRIEND_BUTTON_IMAGE_NAME = 'add_friend_button3.png'
ADD_FRIEND_BUTTON_IMAGE_PATH = os.path.dirname(os.path.abspath(__file__)) + '\\' + IMAGES_FILE + '\\' + MAIN_SCREEN_IMAGES_FILE + '\\' + ADD_FRIEND_BUTTON_IMAGE_NAME
V_IMG_NAME = 'v.png'
V_IMG_PATH = os.path.dirname(os.path.abspath(__file__)) + '\\' + IMAGES_FILE + '\\' + MAIN_SCREEN_IMAGES_FILE + '\\' + V_IMG_NAME
X_IMG_NAME = 'x.png'
X_IMG_PATH = os.path.dirname(os.path.abspath(__file__)) + '\\' + IMAGES_FILE + '\\' + MAIN_SCREEN_IMAGES_FILE + '\\' + X_IMG_NAME
FRIEND_REQUEST_POPUP_IMG_NAME = 'friend_request_img.jpg'
FRIEND_REQUEST_POPUP_IMG_PATH = os.path.dirname(os.path.abspath(__file__)) + '\\' + IMAGES_FILE + '\\' + MAIN_SCREEN_IMAGES_FILE + '\\' + FRIEND_REQUEST_POPUP_IMG_NAME
CALL_HANG_UP_IMG_NAME = 'hang_up_img2.png'
CALL_HANG_UP_IMG_PATH = os.path.dirname(os.path.abspath(__file__)) + '\\' + IMAGES_FILE + '\\' + MAIN_SCREEN_IMAGES_FILE + '\\' + CALL_HANG_UP_IMG_NAME
GREEN_CALL_BUTTON_NAME = 'green_call_button.png'
GREEN_CALL_BUTTON_PATH = os.path.dirname(os.path.abspath(__file__)) + '\\' + IMAGES_FILE + '\\' + MAIN_SCREEN_IMAGES_FILE + '\\' + GREEN_CALL_BUTTON_NAME
BUCK_TO_CALL_BUTTON_IMG_NAME = 'back_to_call_button.png'
BUCK_TO_CALL_BUTTON_IMG_PATH = os.path.dirname(os.path.abspath(__file__)) + '\\' + IMAGES_FILE + '\\' + MAIN_SCREEN_IMAGES_FILE + '\\' + BUCK_TO_CALL_BUTTON_IMG_NAME

#friend buttons img:
FRIEND_BUTTONS_IMAGES_FILE = 'friend_buttons_imgs'
FRIEND_BUTTONS_IMAGES_BASE_NAME = 'friend_button_'
FRIEND_BUTTONS_IMAGES_PATH = []
TEMP_FRIEND_BUTTONS_IMAGES_PATH_LIST = []
for i in xrange(21):
    img_path = os.path.dirname(os.path.abspath(__file__)) + '\\' + IMAGES_FILE + '\\' + MAIN_SCREEN_IMAGES_FILE + '\\' + FRIEND_BUTTONS_IMAGES_FILE + '\\' + FRIEND_BUTTONS_IMAGES_BASE_NAME + str(i + 1) + '.png'
    FRIEND_BUTTONS_IMAGES_PATH.append(img_path)
    TEMP_FRIEND_BUTTONS_IMAGES_PATH_LIST.append(img_path)



#Call screen images path
CALL_SCREEN_IMAGES_FILE = 'call_screen'

BUTTONS_PART_IMAGE_NAME = 'buttons_img.jpg'
BUTTONS_PART_IMAGE_PATH = os.path.dirname(os.path.abspath(__file__)) + '\\' + IMAGES_FILE + '\\' + CALL_SCREEN_IMAGES_FILE + '\\' + BUTTONS_PART_IMAGE_NAME
HANG_UP_IMAGE_NAME = 'hangup_img.png'
HANG_UP_IMAGE_PATH =  os.path.dirname(os.path.abspath(__file__)) + '\\' + IMAGES_FILE + '\\' + CALL_SCREEN_IMAGES_FILE + '\\' + HANG_UP_IMAGE_NAME
BACK_BUTTON_IMAGE_NAME = 'back_button.png'
BACK_BUTTON_IMAGE_PATH = os.path.dirname(os.path.abspath(__file__)) + '\\' + IMAGES_FILE + '\\' + CALL_SCREEN_IMAGES_FILE + '\\' + BACK_BUTTON_IMAGE_NAME



#Error messages

MAX_LEN_ERROR_MESSAGE = 35

#Login screen errors:
LOGIN_ERROR_INCORRECT = 'Incorrect user name or password'
#Register screen errors:
REGISTER_ERROR_EMPTY_SLOTS = 'You must fill the all slots'
REGISTER_ERROR_EXIST_USER = 'User name already exists'
SIGN_ERROR_NOT_VALID_PASSWORD = 'Password must be at least 6 chars. need to include numbers and letters'
REGISTER_ERROR_EXIST_PASSWORD = 'Password already exists'
#Main screen errors:
FRIEND_REQUEST_ERROR_NOT_EXIST = 'The requested friend user name does not exists'
FRIEND_REQUEST_PERMISSION = 'The friend request was sent...'
FRIEND_REQUEST_TEXT = ' have sent you a friend request'
FRIEND_REQUEST_ACCEPT = ' have accepted your friend request'
FRIEND_REQUEST_REJECT = ' have rejected your friend request'
FRIEND_REQUEST_ERROR_CURRENT_USER_NAME = 'You can not add yourself as a friend'
FRIEND_REQUEST_ERROR_ALREADY_FRIENDS = 'You are already friend of '
FRIEND_REQUEST_ALREADY_SENT_NO_RESPONSE = 'You already sent friend request\nto %s and he did not respond yet.'
USER_TO_CALL_NOT_CONNECTED = '%s is not connected.\nTry calling him later.'
WAITING_FOR_CALL = 'Calling %s .....'
INCOMING_CALL = 'Incoming call'
YOU_ALREADY_IN_CALL = 'You already in a call'
FRIEND_ALREADY_IN_CALL = '%s already in call\nTry call him later'



#Headeres


#Send headers login:
HEADER_LOGIN_ERROR_INCORRECT = 'INC'    #Incorrenct password or user name
HEADER_LOGIN_PERMISSION = 'PER'         #The user name and password is correct
#Send headers sign up:
HEADER_SIGN_ERROR_EXIST_USER = 'USR'    #The user name already exists
HEADER_SIGN_ERROR_EXIST_PASSWORD = 'PAS'#The password already exists
HEADER_SIGN_ERROR_NOT_VALID_PASSWORD = 'NVP' #The requested users password is not valid
HEADER_SIGN_PERMISSION = 'PER'          #The user name and password does not exists
#Send headers main screen:
HEADER_FRIEND_REQUEST_ERROR_NOT_EXIST = 'FNE'   #The requested friend user name does not exists
HEADER_FRIEND_REQUEST_PERMISSION = 'FRP'        #The requested friend exists  -> send a friend request (this is permission which being sent to the applicant)
HEADER_FRIEND_REQUEST_ACCEPT = 'FRA'            #The friend request accepted
HEADER_FRIEND_REQUEST_REJECT = 'FRR'            #The friend tequest rejected
HEADER_FRIEND_REQUEST_ALREADY_SENT_NO_RESPONSE = 'FAN'   #A friend request as been already sent to user form same user and he did not responed yet.
HEADER_USER_TO_CALL_NOT_CONNECTED = 'UNC'       #The called user is not connected
HEADER_FRIEND_ALREADY_IN_CALL = 'FAC'           #The requested friend to call to is already in a call
HEADER_YOU_ALREADY_IN_CALL = 'UAC'              #The caller is already in a call and he can not call to another friend
HEADER_CALL_PERMISSION = 'CAP'                  #Permission to user which called
HEADER_CALL_REQUEST_STOP = 'CRS'                #The call request has been stopped or refused by one of the two sides
HEADER_START_CALL = 'SCL'                       #The user press the green call button after another user called him




#Ids (connection between the kv file and this file - the python file)

#Login ids:
ID_USER_NAME_TEXT_INPUT = 'user_name_text_input'
ID_PASSWORD_TEXT_INPUT = 'password_text_input'
ID_LOGIN_ERROR_MESSAGE = 'login_error_message'
#Register ids:
ID_REGISTER_USER_NAME_INPUT = 'user_name_input_register'
ID_REGISTER_PASSWORD_INPUT = 'password_input_register'
ID_REGISTER_ERROR_MESSAGE = 'register_error_message'
#Main screen ids:
ID_FRIENDS_LIST = 'friends_list'
ID_NAME_CALL_PART = 'name_call_part'
ID_FRIEND_SEARCH_TEXT_INPUT = 'friend_search_text_input'
ID_MESSAGE_POPUP_LABEL = 'message_popup_label'
ID_FRIEND_REQUEST_POPUP_LABEL = 'friend_request_popup_label'
ID_V_BUTTON = 'v_button'
ID_X_BUTTON = 'x_button'
ID_CALLER_POPUP_LABEL = 'caller_popup_label'
ID_POPUP_HANG_UP_BUTTON = 'popup_hang_up_button'
ID_CALL_POPUP_LABEL = 'call_popup_label'
ID_GREEN_CALL_BUTTON = 'green_call_button'
ID_RED_HANG_UP_BUTTON = 'red_hang_up_button'
#Call screen ids:
ID_OUTPUT_IMG = 'output_img'
ID_INPUT_IMG = 'input_img'



#Command headers
LOGIN_HEADER = 'LOG'
SIGN_UP_HEADER = 'SIN'
FRIEND_REQUEST_HEADER = 'FRE'
CALL_HEADER = 'CAL'
EXIT_HEADER = 'EXT'




#MainScreen data (constents and other variables)
CLOCK_SCHEDULE_INTERVAL_TIME = 0.5
CURRENT_USER_NAME = ''
CURRENT_FRIENDS_LIST = []
CURRENT_CALL_POPUP = None


#CallScreen data (constents and other variables)
CALLER_ROLL = 'CALLER'
RECEIVER_ROLL = 'RECEIVER'
CALL_PORT_1 = 50001
CALL_PORT_2 = 50002
CALL_PORT_3 = 50003
CALL_PORT_4 = 50004



#Screens objects
LOGIN_SCREEN_OBJECT = None
REGISTER_SCREEN_OBJECT = None
MAIN_SCREEN_OBJECT = None
CALL_SCREEN_OBJECT = None




class PumpkinApp(App):
    """
    This is the main app of the pumpkin application.
    The application is built here.
    """

    def build(self):
        """
        Build the application.
        """

        self.screen_manager = self.build_screen_manager()
        return self.screen_manager

    def build_screen_manager(self):
        """
        Build the screen manager.
        :return: the screen manager.
        :rtype: screen manager object.
        """

        global LOGIN_SCREEN_OBJECT, REGISTER_SCREEN_OBJECT, MAIN_SCREEN_OBJECT, CALL_SCREEN_OBJECT

        LOGIN_SCREEN_OBJECT = LoginScreen(name=LOGIN_SCREEN_NAME)
        REGISTER_SCREEN_OBJECT = RegisterScreen(name=REGISTER_SCREEN_NAME)
        MAIN_SCREEN_OBJECT = MainScreen(name=MAIN_SCREEN_NAME)
        CALL_SCREEN_OBJECT = CallScreen(name=CALL_SCREEN_NAME)

        screen_manager = ScreenManager() #transition=FadeTransition()
        screen_manager.add_widget(LOGIN_SCREEN_OBJECT)
        screen_manager.add_widget(REGISTER_SCREEN_OBJECT)
        screen_manager.add_widget(MAIN_SCREEN_OBJECT)
        screen_manager.add_widget(CALL_SCREEN_OBJECT)
        screen_manager.current = FIRST_SCREEN_NAME

        return screen_manager

    def on_stop(self):
        """
        When the application is stopped this function is called.
        Close the app properly.
        """

        if CALL_SCREEN_OBJECT.in_call:
            print 'Close call'
            CALL_SCREEN_OBJECT.close_call()
            CLIENT_OBJECT.send_data([HEADER_CALL_REQUEST_STOP])
        CLIENT_OBJECT.send_data([EXIT_HEADER])






class LoginScreen(Screen):
    """
    This is the login screen.
    Handles the login screen functionality.
    """

    def reset_screen(self):
        """
        Reset the screen to original position (Ex.empty Text Inputs).
        """
        self.ids[ID_USER_NAME_TEXT_INPUT].text = ''
        self.ids[ID_PASSWORD_TEXT_INPUT].text = ''
        self.ids[ID_LOGIN_ERROR_MESSAGE].text = ''

    def text_filter(self):
        pass

    def get_source(self):
        """
        Returns the path to the login screen img.
        :return: login screen img path
        :rtype: str
        """
        return LOGIN_SCREEN_IMG_PATH

    def on_press_create_account(self):
        """
        When create account button is pressed the
        function are called and handle the situation.
        """
        self.manager.current = REGISTER_SCREEN_NAME
        self.manager.transition.direction = 'right'
        self.reset_screen()

    def on_press_login(self):
        """
        When login button is pressed the
        function are called and handle the situation.
        """

        global CURRENT_USER_NAME, CURRENT_FRIENDS_LIST

        if not (self.ids[ID_USER_NAME_TEXT_INPUT].text and self.ids[ID_PASSWORD_TEXT_INPUT].text):
            # One of the bars are empty
            self.ids[ID_LOGIN_ERROR_MESSAGE].text = LOGIN_ERROR_INCORRECT.ljust(MAX_LEN_ERROR_MESSAGE)
        else:
            # Send the user name and the password to server
            # and check if the user is correct.
            user_name = self.ids[ID_USER_NAME_TEXT_INPUT].text
            password = self.ids[ID_PASSWORD_TEXT_INPUT].text
            data_list = CLIENT_OBJECT.send_data_and_receive([LOGIN_HEADER, user_name, password])
            status_header = data_list[0]
            if status_header == HEADER_LOGIN_ERROR_INCORRECT:
                # The user (user name and password) is incorrect -> can not login to requested user.
                self.ids[ID_LOGIN_ERROR_MESSAGE].text = LOGIN_ERROR_INCORRECT.ljust(MAX_LEN_ERROR_MESSAGE)
            elif status_header == HEADER_LOGIN_PERMISSION:
                # The user (user name and password) is correct -> login to user
                # The login process here.
                friends_string = data_list[1]
                friends_list = friends_string.split('\n')
                if len(friends_list) == 1 and friends_list[0] == '':
                    friends_list = []
                CURRENT_FRIENDS_LIST = friends_list
                MAIN_SCREEN_OBJECT.set_friends_list_buttons(friends_list)
                self.manager.current = MAIN_SCREEN_NAME
                self.manager.transition.direction = 'right'
                self.reset_screen()
                CURRENT_USER_NAME = user_name

                #Show the user alerts
                alert_data_list = []
                user_alerts = json.loads(data_list[2])
                for alert in user_alerts:
                    alert_data_list = []
                    alert_data_list.append(alert[0])
                    for arg in alert[1]:
                        alert_data_list.append(arg)
                    print alert_data_list
                    MAIN_SCREEN_OBJECT.handle_data_receiving_data(alert_data_list)


                Clock.schedule_interval(MAIN_SCREEN_OBJECT.activate_receiving_schedule_interval, CLOCK_SCHEDULE_INTERVAL_TIME)




class RegisterScreen(Screen):
    """
    The register screen
    """

    def reset_screen(self):
        """
        Reset the screen to original position.
        """
        self.ids[ID_REGISTER_USER_NAME_INPUT].text = ''
        self.ids[ID_REGISTER_PASSWORD_INPUT].text = ''
        self.ids[ID_REGISTER_ERROR_MESSAGE].text = ''

    def get_source(self):
        """
        Returns the path to the screen image.
        :return: register screen image path
        :rtype: str
        """
        return REGISTER_SCREEN_IMG_PATH

    def on_press_already_have_an_account(self):
        """
        The function is called when the already have
        an account button is pressed.
        """
        self.manager.current = LOGIN_SCREEN_NAME
        self.manager.transition.direction = 'left'
        self.reset_screen()

    def on_press_sign_up(self):
        """
        The function is called when sign
        up button is pressed.
        :return:
        """
        if not (self.ids[ID_REGISTER_USER_NAME_INPUT].text and self.ids[ID_REGISTER_PASSWORD_INPUT].text):
            # The bars are empty.
            self.ids[ID_REGISTER_ERROR_MESSAGE].text = REGISTER_ERROR_EMPTY_SLOTS.ljust(MAX_LEN_ERROR_MESSAGE)
        else:
            # Send requested user name and password
            # to the system server.
            # Handles the register request.
            status_header = CLIENT_OBJECT.send_data_and_receive([SIGN_UP_HEADER, self.ids[ID_REGISTER_USER_NAME_INPUT].text, self.ids[ID_REGISTER_PASSWORD_INPUT].text])[0]
            if status_header == HEADER_SIGN_ERROR_EXIST_USER:
                self.ids[ID_REGISTER_ERROR_MESSAGE].text = REGISTER_ERROR_EXIST_USER.ljust(MAX_LEN_ERROR_MESSAGE)
            elif status_header == HEADER_SIGN_ERROR_EXIST_PASSWORD:
                self.ids[ID_REGISTER_ERROR_MESSAGE].text = REGISTER_ERROR_EXIST_PASSWORD.ljust(MAX_LEN_ERROR_MESSAGE)
            elif status_header == HEADER_SIGN_ERROR_NOT_VALID_PASSWORD:
                self.ids[ID_REGISTER_ERROR_MESSAGE].text = SIGN_ERROR_NOT_VALID_PASSWORD.ljust(MAX_LEN_ERROR_MESSAGE)
            elif status_header == HEADER_SIGN_PERMISSION:
                self.ids[ID_REGISTER_ERROR_MESSAGE].text = 'Sign up successfully!!!'.ljust(MAX_LEN_ERROR_MESSAGE)
        self.ids[ID_REGISTER_USER_NAME_INPUT].text = ''
        self.ids[ID_REGISTER_PASSWORD_INPUT].text = ''




class MainScreen(Screen):
    """
    The main screen of the app
    When the user in 'connect' position.
    """

    def __init__(self, **kwargs):
        """
        Build screen function.
        """
        super(MainScreen, self).__init__(**kwargs)

        self.popupWindow = None

    def get_messages_img_source(self):
        """
        Return the messages image path.
        :return: messages image path
        :rtype: str
        """
        return MESSAGES_IMAGE_PATH

    def get_call_part_img_source(self):
        """
        Returns the call part image path.
        :return: call part image path.
        :rtype: str
        """
        return CALL_PART_IMAGE_PATH

    def get_add_friend_part_img_source(self):
        """
        Returns the add friend part image path.
        :return: add friend part image path.
        :rtype: str
        """
        return ADD_FRIEND_PART_IMAGE_PATH

    def get_call_button_img_source(self):
        """
        Returns the call button image path.
        :return: call button image path.
        :rtype: str
        """
        return CALL_BUTTON_IMAGE_PATH

    def get_call_button_pressed_img_source(self):
        """
        Returns the call button pressed image path.
        :return: call button pressed image path.
        :rtype: str
        """
        return CALL_BUTTON_PRESSED_IMAGE_PATH

    def get_back_to_call_button_source(self):
        """
        Returns the buck to call button image path.
        :return: buck to call button image path.
        :rtype: str
        """
        return BUCK_TO_CALL_BUTTON_IMG_PATH

    def get_add_friend_button(self):
        """
        Returns the add friend button image path.
        :return: add friend button image path.
        :rtype: str
        """
        return ADD_FRIEND_BUTTON_IMAGE_PATH


    def on_press_friend_button(self, pressed_button):
        """
        The function is called when a friend button pressed.
        When pressed -> display the friend user name on call part.
        :param pressed_button: the friend button object which pressed.
        """
        self.ids[ID_NAME_CALL_PART].text = pressed_button.text

    def on_press_call_button(self):
        """
        Called when the call button is pressed.
        Sends a call request to the system server (which passes
        it to the requested user).
        """
        friend_to_call_to = self.ids[ID_NAME_CALL_PART].text
        if friend_to_call_to:
            CLIENT_OBJECT.send_data([CALL_HEADER, friend_to_call_to])

    def on_press_add_friend_button(self):
        """
        Called when the add friend button is pressed.
        """
        friend_user_name = self.ids[ID_FRIEND_SEARCH_TEXT_INPUT].text
        if friend_user_name:
            # The add friend bar is not empty.
            if friend_user_name == CURRENT_USER_NAME:
                # The requested friend the name is the current
                # user name (the user send request to himself).
                self.message_popup('Error', FRIEND_REQUEST_ERROR_CURRENT_USER_NAME)
            elif friend_user_name in CURRENT_FRIENDS_LIST:
                # The request is for an existing friend
                # (the user and the requested friend are already friends)
                self.message_popup('Error', FRIEND_REQUEST_ERROR_ALREADY_FRIENDS + friend_user_name)
            else:
                # Sends the requested freind user name to the system server
                # (which send a friend request to the requested user).
                CLIENT_OBJECT.send_data([FRIEND_REQUEST_HEADER, self.ids[ID_FRIEND_SEARCH_TEXT_INPUT].text])
            self.ids[ID_FRIEND_SEARCH_TEXT_INPUT].text = ''

    def on_press_back_to_call_button(self):
        """
        Called when back to call button is pressed.
        Returns the the current screen to the call screen.
        """
        if CALL_SCREEN_OBJECT.in_call:
            self.manager.current = CALL_SCREEN_NAME

    def message_popup(self, title, text):
        """
        Build and show on the screen a message popup.
        :param title: the popup title.
        :param text: the popup text.
        """
        show = MessagePopup()
        show.ids[ID_MESSAGE_POPUP_LABEL].text = text
        popupWindow = Popup(title=title, title_size=20, content=show, size_hint=(None, None), size=(400, 200),
                            background=FRIEND_REQUEST_POPUP_IMG_PATH)
        popupWindow.open()

    def reset_temp_friend_buttons_images_path_list(self):
        """
        Reset the friend buttons images
        path list to initial position.
        """

        global TEMP_FRIEND_BUTTONS_IMAGES_PATH_LIST

        if not TEMP_FRIEND_BUTTONS_IMAGES_PATH_LIST:
            for path in FRIEND_BUTTONS_IMAGES_PATH:
                TEMP_FRIEND_BUTTONS_IMAGES_PATH_LIST.append(path)

    def set_friends_list_buttons(self, friends_list):
        """
        Sets the friend list button.
        Called when the user login.
        :param friends_list: the users friends list.
        """

        for friend in friends_list:
            self.reset_temp_friend_buttons_images_path_list()
            button_id = friend + '_button'
            button = FriendButton(
                button_id,
                TEMP_FRIEND_BUTTONS_IMAGES_PATH_LIST.pop(0),
                friend
            )
            self.ids[ID_FRIENDS_LIST].add_widget(button)
            self.ids[button_id] = button
            button.set_on_release(function=self.on_press_friend_button)

    def add_friend_button(self, friend_user_name):
        """
        Add friend button to the user's friend list buttons.
        :param friend_user_name: the friend user name.
        """
        self.reset_temp_friend_buttons_images_path_list()
        button_id = friend_user_name + '_button'
        button = FriendButton(
                button_id,
                TEMP_FRIEND_BUTTONS_IMAGES_PATH_LIST.pop(0),
                friend_user_name
            )
        self.ids[ID_FRIENDS_LIST].add_widget(button)
        self.ids[button_id] = button
        button.set_on_release(function=self.on_press_friend_button)

    def activate_receiving_schedule_interval(self, *args):
        """
        When user login the function called
        every amount of time (the schedule time).
        Receives data from the system server and handle it.
        :param args: dt of the schedule function in kivy (not important).
        """

        data_list = CLIENT_OBJECT.main_screen_data_receiving()
        self.handle_data_receiving_data(data_list)

    def handle_data_receiving_data(self, data_list):
        """
        Handle all the data which received from the system server.
        Performs a certain action for every data from system server.
        :param data_list: the data list from system server.
        """

        global CURRENT_FRIENDS_LIST, CURRENT_CALL_POPUP

        def on_press_popup_v_button(a):
            """
            Called when the v button on popup is pressed.
            Handles the situation.
            :param a: data from popup
            """
            popupWindow.dismiss()
            CLIENT_OBJECT.send_data([HEADER_FRIEND_REQUEST_ACCEPT, friend_user_name])
            self.add_friend_button(friend_user_name)
            CURRENT_FRIENDS_LIST.append(friend_user_name)

        def on_press_popup_x_button(a):
            """
            Called when the x button on popup is pressed.
            Handles the situation.
            :param a: data from popup
            """
            popupWindow.dismiss()
            CLIENT_OBJECT.send_data([HEADER_FRIEND_REQUEST_REJECT, friend_user_name])

        def on_press_popup_hang_up_button(a):
            """
            Called when the hang up button on popup is pressed.
            Handles the situation.
            :param a: data from popup
            """

            global CURRENT_CALL_POPUP

            if CURRENT_CALL_POPUP:
                CURRENT_CALL_POPUP.dismiss()
                CURRENT_CALL_POPUP = None
                CLIENT_OBJECT.send_data([HEADER_CALL_REQUEST_STOP])

        def on_press_popup_green_call_button(a):
            """
            Called when the green call button on popup is pressed.
            Handles the situation.
            :param a: data from popup
            """

            global CURRENT_CALL_POPUP

            if CURRENT_CALL_POPUP:
                CURRENT_CALL_POPUP.dismiss()
                CURRENT_CALL_POPUP = None
                CLIENT_OBJECT.send_data([HEADER_START_CALL])
                CALL_SCREEN_OBJECT.make_connection(CALLER_ROLL)



        if data_list:
            # The data list is not empty.
            # Received data from system server.
            status_header = data_list[0]

            if status_header == HEADER_FRIEND_REQUEST_ERROR_NOT_EXIST:
                # Handles friend request error.
                # Display an friend request error to screen.
                self.message_popup('Error', FRIEND_REQUEST_ERROR_NOT_EXIST)
                self.ids[ID_FRIEND_SEARCH_TEXT_INPUT].text = ''

            elif status_header == HEADER_FRIEND_REQUEST_PERMISSION:
                # Handles friend request permission.
                # Display an friend request permission to the screen.
                text = FRIEND_REQUEST_PERMISSION
                title = 'Friend request permission'
                self.message_popup(title, text)
                self.ids[ID_FRIEND_SEARCH_TEXT_INPUT].text = ''

            elif status_header == FRIEND_REQUEST_HEADER:
                # Handles a friend request which arrived from
                # different user. Display a friend request to the screen.
                friend_user_name = data_list[1]
                show = FriendRequestPopup()
                show.ids[ID_FRIEND_REQUEST_POPUP_LABEL].text = friend_user_name + FRIEND_REQUEST_TEXT
                show.ids[ID_V_BUTTON].bind(on_release=on_press_popup_v_button)
                show.ids[ID_X_BUTTON].bind(on_release=on_press_popup_x_button)
                popupWindow = Popup(title='Friend Request', title_size=20, content=show, size_hint=(None, None),
                                         size=(400, 200), auto_dismiss=False, background=FRIEND_REQUEST_POPUP_IMG_PATH)
                popupWindow.open()

            elif status_header == HEADER_FRIEND_REQUEST_ACCEPT:
                # Handles a friend request accept.
                # Display an accept to friend request message
                # to the screen.
                friend_user_name = data_list[1]
                text = friend_user_name + FRIEND_REQUEST_ACCEPT
                title = 'Friend request accepted'
                self.message_popup(title, text)
                if friend_user_name not in CURRENT_FRIENDS_LIST:
                    self.add_friend_button(friend_user_name)
                    CURRENT_FRIENDS_LIST.append(friend_user_name)

            elif status_header == HEADER_FRIEND_REQUEST_REJECT:
                # Handles a friend request reject.
                # Display an reject to friend request message
                # to the screen.
                friend_user_name = data_list[1]
                text = friend_user_name + FRIEND_REQUEST_REJECT
                title = 'Friend request rejected'
                self.message_popup(title, text)

            elif status_header == HEADER_FRIEND_REQUEST_ALREADY_SENT_NO_RESPONSE:
                # Display an error message to the screen.
                # The user which received a friend request
                # did not respond yet. (The current user already sent
                # him a friend request).
                friend_user_name = data_list[1]
                text = FRIEND_REQUEST_ALREADY_SENT_NO_RESPONSE % (friend_user_name)
                title = 'Error'
                self.message_popup(title, text)

            elif status_header == HEADER_USER_TO_CALL_NOT_CONNECTED:
                # The current user try to call another user which not
                # connected. Display an error message.
                friend_user_name = data_list[1]
                text = USER_TO_CALL_NOT_CONNECTED%(friend_user_name)
                title = 'Not connected'
                self.message_popup(title, text)

            elif status_header == HEADER_YOU_ALREADY_IN_CALL:
                # If current user already in a call it can not
                # call another user. Display an error message.
                text = YOU_ALREADY_IN_CALL
                title = 'Call request error'
                self.message_popup(title, text)

            elif status_header == HEADER_FRIEND_ALREADY_IN_CALL:
                # Current user try to call to another user but can not
                # because the user already in a call. Display an error
                # message to screen.
                friend_user_name = data_list[1]
                text = FRIEND_ALREADY_IN_CALL % (friend_user_name)
                title = 'Friend not available'
                self.message_popup(title, text)

            elif status_header == HEADER_CALL_PERMISSION:
                # Current user gets permission to call his friend.
                # Display a call situation popup.
                friend_user_name = data_list[1]
                show = CallerPopup()
                show.ids[ID_CALLER_POPUP_LABEL].text = WAITING_FOR_CALL%(friend_user_name)
                show.ids[ID_POPUP_HANG_UP_BUTTON].bind(on_release=on_press_popup_hang_up_button)
                popupWindow = Popup(title='Calling', title_size=20, content=show, size_hint=(None, None),
                                    size=(400, 200), auto_dismiss=False, background=FRIEND_REQUEST_POPUP_IMG_PATH)
                CURRENT_CALL_POPUP = popupWindow
                CURRENT_CALL_POPUP.open()

            elif status_header == CALL_HEADER:
                # The current user gets a call from another user.
                # Display a call situation popup.
                friend_user_name = data_list[1]
                friend_ip = data_list[2]
                show = CallPopup()
                show.ids[ID_CALL_POPUP_LABEL].text = friend_user_name
                show.ids[ID_GREEN_CALL_BUTTON].bind(on_release=on_press_popup_green_call_button)
                show.ids[ID_RED_HANG_UP_BUTTON].bind(on_release=on_press_popup_hang_up_button)
                popupWindow = Popup(title=INCOMING_CALL, title_size=20, content=show, size_hint=(None, None),
                                    size=(400, 200), auto_dismiss=False, background=FRIEND_REQUEST_POPUP_IMG_PATH)
                CURRENT_CALL_POPUP = popupWindow
                CURRENT_CALL_POPUP.open()

            elif status_header == HEADER_CALL_REQUEST_STOP:
                # The call request was stopped by the other side
                # of the call request. Raise the call situation popup.
                if CURRENT_CALL_POPUP:
                    CURRENT_CALL_POPUP.dismiss()
                    CURRENT_CALL_POPUP = None
                if CALL_SCREEN_OBJECT.in_call:
                    CALL_SCREEN_OBJECT.close_call()
                CALL_SCREEN_OBJECT.set_data()

            elif status_header == HEADER_START_CALL:
                # The call request was approved.
                # Start video call.
                if CURRENT_CALL_POPUP:
                    CURRENT_CALL_POPUP.dismiss()
                    CURRENT_CALL_POPUP = None

                friend_ip = data_list[1]
                CALL_SCREEN_OBJECT.make_connection(RECEIVER_ROLL, friend_ip)




# This is the all popup objects.
class MessagePopup(FloatLayout):
    """
    This is the message popup object.
    Create popup which display only text and messages.
    (have no buttons).
    """
    pass

class FriendRequestPopup(FloatLayout):
    """
    This is the friend request popup object
    Create popup which display friend requests.
    """

    def ger_v_img_source(self):
        """
        Returns the v image path.
        :return: v image path.
        :rtype: str
        """
        return V_IMG_PATH

    def get_x_img_source(self):
        """
        Returns the x image path.
        :return: x image path.
        :rtype: str.
        """
        return X_IMG_PATH

class CallerPopup(FloatLayout):
    """
    The caller popup object.
    Create popup which display hangup button
    and text.
    """

    def get_hang_up_button_source(self):
        """
        Returns the hang up button path.
        :return: hang up button path.
        :rtype: str.
        """
        return CALL_HANG_UP_IMG_PATH

class CallPopup(FloatLayout):
    """
    The call popup object.
    Create popup which display hangup
    and green call buttons and text.
    """

    def get_hang_up_button(self):
        """
        Returns the hang up button path.
        :return: hang up button path.
        :rtype: str.
        """
        return CALL_HANG_UP_IMG_PATH

    def get_green_call_button(self):
        """
        Returns the green call button path.
        :return: green call button path.
        :rtype: str.
        """
        return GREEN_CALL_BUTTON_PATH




class CallScreen(Screen):

    def __init__(self, **kwargs):
        super(CallScreen, self).__init__(**kwargs)

        self.main_video_input_address = None
        self.main_video_output_address = None

        self.main_audio_input_address = None
        self.main_audio_output_address = None

        self.VIDEO_OBJECT = None
        self.AUDIO_OBJECT = None

        self.output_img = self.ids[ID_OUTPUT_IMG]
        self.input_img = self.ids[ID_INPUT_IMG]

        self.in_call = False
        self.current_close = True
        self.video_sending_event = None
        self.video_receiving_event = None
        self.audio_sending_event = None
        self.audio_receiving_event = None


    def set_data(self):

        self.main_video_input_address = None
        self.main_video_output_address = None

        self.main_audio_input_address = None
        self.main_audio_output_address = None

        self.VIDEO_OBJECT = None
        self.AUDIO_OBJECT = None

        self.output_img = self.ids[ID_OUTPUT_IMG]
        self.input_img = self.ids[ID_INPUT_IMG]

        self.in_call = False
        self.current_close = True
        self.video_sending_event = None
        self.video_receiving_event = None
        self.audio_sending_event = None
        self.audio_receiving_event = None


    def get_buttons_part_img_source(self):
        return BUTTONS_PART_IMAGE_PATH

    def get_hangup_img_source(self):
        return HANG_UP_IMAGE_PATH

    def get_back_button_img_source(self):
        return BACK_BUTTON_IMAGE_PATH


    def make_connection(self, roll, ip=None):

        self.manager.current = CALL_SCREEN_NAME

        permission_to_start_call = False

        if roll == CALLER_ROLL:
            self.make_connection_caller()
            permission_to_start_call = True
        elif roll == RECEIVER_ROLL and ip:
            self.make_connection_receiver(ip)
            permission_to_start_call = True

        if permission_to_start_call:
            self.start_conversation()


    def make_connection_receiver(self, ip):

        self.main_video_input_address = (ip, CALL_PORT_1)
        self.main_video_output_address = (ip, CALL_PORT_2)

        self.main_audio_input_address = (ip, CALL_PORT_3)
        self.main_audio_output_address = (ip, CALL_PORT_4)

        output_video_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        input_video_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        output_audio_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        input_audio_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        output_video_socket.connect(self.main_video_input_address)
        input_video_socket.connect(self.main_video_output_address)

        output_audio_socket.connect(self.main_audio_input_address)
        input_audio_socket.connect(self.main_audio_output_address)

        self.VIDEO_OBJECT = Video(input_video_socket, output_video_socket, 1)
        self.AUDIO_OBJECT = Audio(input_audio_socket, output_audio_socket)

    def make_connection_caller(self):

        self.main_video_input_address = ('0.0.0.0', CALL_PORT_1)
        self.main_video_output_address = ('0.0.0.0', CALL_PORT_2)

        self.main_audio_input_address = ('0.0.0.0', CALL_PORT_3)
        self.main_audio_output_address = ('0.0.0.0', CALL_PORT_4)

        video_input_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        video_output_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        audio_input_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        audio_output_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print 'Sockets created'

        video_input_socket.bind(self.main_video_input_address)
        video_output_socket.bind(self.main_video_output_address)

        audio_input_socket.bind(self.main_audio_input_address)
        audio_output_socket.bind(self.main_audio_output_address)
        print 'Sockets bind complete'

        video_input_socket.listen(1)
        video_output_socket.listen(1)

        audio_input_socket.listen(1)
        audio_output_socket.listen(1)
        print 'Sockets now listening'

        (input_video_socket, receiver_input_video_address) = video_input_socket.accept()
        print 'Connected video input socket....'
        (output_video_socket, receiver_output_video_address) = video_output_socket.accept()
        print 'Connected video output socket....'
        (input_audio_socket, receiver_input_audio_address) = audio_input_socket.accept()
        print 'Connected audio input socket....'
        (output_audio_socket, receiver_output_audio_address) = audio_output_socket.accept()
        print 'Connected audio output socket....'

        video_input_socket.close()
        video_output_socket.close()
        audio_input_socket.close()
        audio_output_socket.close()

        self.VIDEO_OBJECT = Video(input_video_socket, output_video_socket)
        self.AUDIO_OBJECT = Audio(input_audio_socket, output_audio_socket)

    def start_conversation(self):

        self.in_call = True
        self.current_close = False

        self.video_sending_event = Clock.schedule_interval(self.video_handle_sending, 1.0 / 33.0)
        self.video_receiving_event = Clock.schedule_interval(self.video_handle_receiving, 1.0 / 33.0)

        self.audio_sending_event = AudioSendingThread(self.AUDIO_OBJECT)
        self.audio_receiving_event = AudioReceivingThread(self.AUDIO_OBJECT)
        self.audio_sending_event.start()
        self.audio_receiving_event.start()

    def video_handle_sending(self, *args):
        try:
            output_frame = self.VIDEO_OBJECT.get_send_frame()
            self.show_output_frame(output_frame)
        except:
            print 'Error'
            self.close_call()


    def video_handle_receiving(self, *args):
        try:
            input_frame = self.VIDEO_OBJECT.receive_frame()
            self.show_input_frame(input_frame)
        except:
            print 'Error'
            self.close_call()

    def show_frame(self, frame):
        buf_img = cv2.flip(frame, 0)
        buf_string_img = buf_img.tostring()
        texture_img = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture_img.blit_buffer(buf_string_img, colorfmt='bgr', bufferfmt='ubyte')
        return texture_img


    def show_output_frame(self, frame):
        texture_img = self.show_frame(frame)
        self.output_img.texture = texture_img


    def show_input_frame(self, frame):
        texture_img = self.show_frame(frame)
        self.input_img.texture = texture_img


    def on_press_hang_up_button(self):
        self.close_call()
        CLIENT_OBJECT.send_data([HEADER_CALL_REQUEST_STOP])


    def close_call(self):
        if not self.current_close:
            self.current_close = True
            self.in_call = False

            if not self.audio_sending_event.stopped():
                self.audio_sending_event.stop()
            if not self.audio_receiving_event.stopped():
                self.audio_receiving_event.stop()

            self.audio_sending_event.join()
            self.audio_receiving_event.join()

            self.video_sending_event.cancel()
            self.video_receiving_event.cancel()
            self.VIDEO_OBJECT.close_video()
            self.AUDIO_OBJECT.close_audio()
            self.manager.current = MAIN_SCREEN_NAME


    def on_press_back_button(self):
        self.manager.current = MAIN_SCREEN_NAME



class AudioSendingThread(threading.Thread):

    def __init__(self, AUDIO_OBJECT):
        super(AudioSendingThread, self).__init__()
        self.stop_event = threading.Event()
        self.AUDIO_OBJECT = AUDIO_OBJECT

    def stop(self):
        self.stop_event.set()

    def stopped(self):
        return self.stop_event.is_set()

    def run(self):
        while not self.stopped():
            try:
                self.AUDIO_OBJECT.send_audio()
            except:
                if not self.stopped():
                    self.stop()
                break

class AudioReceivingThread(threading.Thread):

    def __init__(self, AUDIO_OBJECT):
        super(AudioReceivingThread, self).__init__()
        self.stop_event = threading.Event()
        self.AUDIO_OBJECT = AUDIO_OBJECT

    def stop(self):
        self.stop_event.set()

    def stopped(self):
        return self.stop_event.is_set()

    def run(self):
        while not self.stopped():
            try:
                ret, input_audio_frames = self.AUDIO_OBJECT.receive_audio()
                if ret:
                    self.AUDIO_OBJECT.hear_audio(input_audio_frames)
            except:
                if not self.stopped():
                    self.stop()
                break




class ImageButton(ButtonBehavior, Image):
    pass

class FriendButton(RelativeLayout):

    def __init__(self, button_id, image_source, friend_text):
        super(FriendButton, self).__init__()
        self.button_id = button_id
        self.image_source = image_source
        self.friend_text = friend_text

        self.set_button_id()
        self.set_image_source()
        self.set_friend_text()

    def get_button_id(self):
        return self.button_id

    def get_image_source(self):
        return self.image_source

    def get_friend_text(self):
        return self.friend_text


    def set_button_id(self):
        self.id = self.button_id

    def set_image_source(self):
        self.ids['friend_button_img'].source = self.image_source

    def set_friend_text(self):
        self.ids['friend_button_img'].text = self.friend_text
        self.ids['friend_name'].text = self.friend_text


    def set_on_release(self, function):
        self.ids['friend_button_img'].bind(on_release=function)

if __name__ == '__main__':
    PumpkinApp().run()