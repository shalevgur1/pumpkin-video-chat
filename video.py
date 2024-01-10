__author__ = 'Gur'

import cv2
import numpy as np
import socket
import time

class Video:

    def __init__(self, input_socket, output_socket, camera_port=0, video_quality=None):
        self.CAMERA_PORT = camera_port
        self.ENCODE_PARAM = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        self.LENGTH_RECV_NUM = 16

        if video_quality and type(video_quality) == int:
            self.VIDEO_QUALITY = video_quality
        else:
            self.VIDEO_QUALITY = 0

        self.input_socket = input_socket
        self.output_socket = output_socket
        self.cap = cv2.VideoCapture(self.CAMERA_PORT)
        self.output_frame = None
        self.input_frame = None


    def get_send_frame(self):

        """This function sends the all video to another user"""

        self.output_frame = self.get_frame()
        self.send_frame()
        return self.output_frame


    def send_frame(self):

        """This function sends the frame to server"""
        result, imgen_code = cv2.imencode('.jpg', self.output_frame, self.ENCODE_PARAM)
        data = np.array(imgen_code)
        str_frame = data.tostring()
        self.output_socket.sendall(str(len(str_frame)).ljust(16))
        self.output_socket.sendall(str_frame)
        time.sleep(self.VIDEO_QUALITY)


    def get_frame(self):

        """Reads frame from camera"""

        img = self.cap.read()[1]
        return img


    def receive_data(self, count):

        '''This function gets length of data and
        receive only the requested data.
        (for ex. if the data length is 10 the function
         receives 10 ?bytes? from client)'''

        buf = b''
        while count:
            new_buf = self.input_socket.recv(count)
            if not new_buf:
                return None
            buf += new_buf
            count -= len(new_buf)
        return buf


    def receive_frame(self):

        """This function recives the frame from client"""

        data = self.receive_data(self.LENGTH_RECV_NUM)
        data_len = int(data)

        client_video_data = self.receive_data(data_len)
        client_video_data = np.fromstring(client_video_data, dtype='uint8')
        decode_img = cv2.imdecode(client_video_data, 1)
        frame = decode_img
        self.input_frame = frame
        return self.input_frame


    def show_frame(self):

        '''This function display the frame on the screen'''

        cv2.imshow('frame', self.input_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            pass


    def close_video(self):
        self.input_socket.close()
        self.output_socket.close()
        self.cap.release()
        cv2.destroyAllWindows()