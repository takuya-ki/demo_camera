#!/usr/bin/env python

import rtsp
import PySimpleGUI as sg
from PIL import Image, ImageTk

import config


class TapoGUI():

    def __init__(
            self,
            user,
            password,
            ipaddr,
            port,
            stream,
            onvif_port):

        self.user = user
        self.password = password
        self.ipaddr = ipaddr
        self.port = port
        self.stream = stream
        self.onvif_port = onvif_port

    def open(self):
        sg.theme('Dark Brown')

        layout = [
            # camera communication info
            [sg.Text('IPADDR: ', size=(12, 1)),
             sg.InputText(default_text=self.ipaddr,
                          size=(20, 1), key='-ipaddr-'),
             sg.Text('PORT: ', size=(12, 1)),
             sg.InputText(default_text=self.port,
                          size=(20, 1), key='-port-'),
             sg.Text('STREAM: ', size=(12, 1)),
             sg.InputText(default_text=self.stream,
                          size=(20, 1), key='-stream-')],
            [sg.Text('ONVIF_PORT: ', size=(12, 1)),
             sg.InputText(default_text=self.onvif_port,
                          size=(20, 1), key='-onvif_port-')],
            [sg.Text('USER: ', size=(12, 1)),
             sg.InputText(default_text=self.user,
                          size=(20, 1), key='-user-'),
             sg.Text('PASS: ', size=(12, 1)),
             sg.InputText(default_text=self.password,
                          size=(20, 1), key='-pass-')],

            # display
            [sg.Image(filename='', key='image')],

            # connect and disconnect
            [sg.Button('Connect', size=(10, 1), key='-start-'),
             sg.Button('Disconnect', size=(10, 1), key='-stop-')],
        ]

        is_streaming = False
        window = sg.Window('cam viewer', layout, location=(0, 0))

        while True:
            event, values = window.read(timeout=20)
            if event in (None, '-exit-'):
                break

            elif event == '-start-':
                rtsp_url = \
                    "rtsp://" + \
                    str(values['-user-']) + ":" + \
                    str(values['-pass-']) + "@" + \
                    str(values['-ipaddr-']) + ":" + \
                    str(values['-port-']) + "/" + \
                    str(values['-stream-'])
                client = rtsp.Client(rtsp_server_uri=rtsp_url, verbose=True)
                is_streaming = True

            elif event == '-stop-':
                is_streaming = False
                client.close()
                img = Image.new("RGB", (640, 360), color=0)
                window['image'].update(data=ImageTk.PhotoImage(img))

            if is_streaming:
                frame = client.read()
                if frame is not None:
                    frame_resize = frame.resize(
                        (frame.width // 2, frame.height // 2))
                    window['image'].update(
                        data=ImageTk.PhotoImage(frame_resize))
                else:
                    print("none")

        window.close()


if __name__ == '__main__':
    c200 = TapoGUI(
        user=config.c200['USER'],
        password=config.c200['PASSWORD'],
        ipaddr=config.c200['IPADDR'],
        port=config.c200['PORT'],
        stream=config.c200['STREAM'],
        onvif_port=config.c200['ONVIF_PORT'])
    c225 = TapoGUI(
        user=config.c225['USER'],
        password=config.c225['PASSWORD'],
        ipaddr=config.c225['IPADDR'],
        port=config.c225['PORT'],
        stream=config.c225['STREAM'],
        onvif_port=config.c225['ONVIF_PORT'])
    c200.open()
    c225.open()
