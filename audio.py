__author__ = 'Gur'


import pyaudio


class Audio:

    def __init__(self, input_socket, output_socket):
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.RECORD_SECONDS = 1
        self.WIDTH = 2
        self.AUDIO_OBJECT = pyaudio.PyAudio()
        self.LENGTH_RECV_NUM = 16

        self.input_socket = input_socket
        self.output_socket = output_socket
        self.output_audio_frames = []

        self.output_stream = self.AUDIO_OBJECT.open(format=self.AUDIO_OBJECT.get_format_from_width(self.WIDTH),
                                               channels=self.CHANNELS,
                                               rate=self.RATE,
                                               output=True,
                                               frames_per_buffer=self.CHUNK)

        self.input_stream = self.AUDIO_OBJECT.open(format=self.FORMAT,
                                               channels=self.CHANNELS,
                                               rate=self.RATE,
                                               input=True,
                                               frames_per_buffer=self.CHUNK)


    def send_audio(self):

        '''
        Send the audio frames
        '''

        self.output_audio_frames = self.get_audio()
        self.send_audio_frames()


    def get_audio(self):

        """Reads the audio data from the voice input device."""

        audio_frames = []
        for i in range(0, int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):
            data = self.input_stream.read(self.CHUNK)
            audio_frames.append(data)
        return audio_frames


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

    def send_audio_frames(self):

        """Sends the audio data frames."""

        self.output_socket.sendall(str(len(self.output_audio_frames)).ljust(16))

        for frame in self.output_audio_frames:
            self.output_socket.sendall(str(len(frame)).ljust(16))
            self.output_socket.sendall(frame)


    def receive_audio(self):

        """receives the audio.
            #recives first the data len and then the audio data"""

        input_audio_frames = []

        frame_num = self.receive_data(self.LENGTH_RECV_NUM)
        frame_num = int(frame_num)

        for i in xrange(frame_num):
            data_len = self.receive_data(self.LENGTH_RECV_NUM)
            data_len = int(data_len)

            client_audio_data = self.receive_data(data_len)
            input_audio_frames.append(client_audio_data)

        return True, input_audio_frames


    def hear_audio(self, audio_frames):

        """Sounds the audio to the hearing device connected to the computer."""

        for frame in audio_frames:
            self.output_stream.write(frame)
        return


    def close_audio(self):
        self.input_socket.close()
        self.output_socket.close()

        self.input_stream.stop_stream()
        self.input_stream.close()
        self.output_stream.stop_stream()
        self.output_stream.close()

        self.AUDIO_OBJECT.terminate()

#frame - audio_frames
#handle_input