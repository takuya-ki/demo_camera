#!/usr/bin/env python3

import sys
import rtsp
import urllib.request
import PySimpleGUI as sg
from onvif import ONVIFCamera
from PIL import Image, ImageTk

import config
from onvifreq import OnvifRequest

sg.theme('Dark Brown')


class TapoGUI():

    def __init__(
            self,
            user,
            password,
            ipaddr,
            port,
            stream,
            onvif_port):

        self._user = user
        self._password = password
        self._ipaddr = ipaddr
        self._port = port
        self._stream = stream
        self._onvif_port = onvif_port

        # parameters for pan-tilt control
        self._X_MIN, self._X_MAX, self._X_STP = -1, 1, 0.1
        self._Y_MIN, self._Y_MAX, self._Y_STP = -1, 1, 0.1
        self._cur_x = 0
        self._cur_y = 0
        self._inited_ptz = False

    def get_config_info(self):
        mycam = ONVIFCamera(
            self._ipaddr, self._onvif_port, self._user, self._password)
        # Create media service object
        media = mycam.create_media_service()
        # Create ptz service object
        ptz = mycam.create_ptz_service()
        # Get target profile
        media_profile = media.GetProfiles()[0]
        print("media_profile:", media_profile)
        print("\n")

    def open(self):
        layout = [
            # camera connection information
            [sg.Text('IPADDR: ', size=(12, 1)),
             sg.InputText(default_text=self._ipaddr,
                          size=(20, 1), key='-ipaddr-'),
             sg.Text('PORT: ', size=(12, 1)),
             sg.InputText(default_text=self._port,
                          size=(20, 1), key='-port-'),
             sg.Text('STREAM: ', size=(12, 1)),
             sg.InputText(default_text=self._stream,
                          size=(20, 1), key='-stream-')],
            [sg.Text('ONVIF_PORT: ', size=(12, 1)),
             sg.InputText(default_text=self._onvif_port,
                          size=(20, 1), key='-onvif_port-')],
            [sg.Text('USER: ', size=(12, 1)),
             sg.InputText(default_text=self._user,
                          size=(20, 1), key='-user-'),
             sg.Text('PASS: ', size=(12, 1)),
             sg.InputText(default_text=self._password,
                          size=(20, 1), key='-pass-')],

            # diplay
            [sg.Image(filename='', key='image')],

            # connect and disconnect
            [sg.Button('Connect', size=(10, 1), key='-start-'),
             sg.Button('Disconnect', size=(10, 1), key='-stop-')],

            # pan-tilt control
            [sg.Button('↖', size=(4, 1),
                       font='Helvetica 14', key='-pt_topleft-'),
             sg.Button('↑', size=(4, 1),
                       font='Helvetica 14', key='-pt_topcenter-'),
             sg.Button('↗', size=(4, 1),
                       font='Helvetica 14', key='-pt_topright-')],
            [sg.Button('←', size=(4, 1),
                       font='Helvetica 14', key='-pt_left-'),
             sg.Button('〇', size=(4, 1),
                       font='Helvetica 14', key='-pt_center-'),
             sg.Button('→', size=(4, 1),
                       font='Helvetica 14', key='-pt_right-')],
            [sg.Button('↙', size=(4, 1),
                       font='Helvetica 14', key='-pt_btmleft-'),
             sg.Button('↓', size=(4, 1),
                       font='Helvetica 14', key='-pt_btmcenter-'),
             sg.Button('↘', size=(4, 1),
                       font='Helvetica 14', key='-pt_btmright-')],
        ]

        is_streaming = False
        window = sg.Window('cam viewer', layout, location=(0, 0))

        while True:
            event, values = window.read(timeout=20)
            if event in (None, '-exit-'):
                break

            elif event == '-start-':
                rtsp_url = "rtsp://" + \
                    str(values['-user-']) + ":" + \
                    str(values['-pass-']) + "@" + \
                    str(values['-ipaddr-']) + ":" + \
                    str(values['-port-']) + "/" + \
                    str(values['-stream-'])
                client = rtsp.Client(rtsp_server_uri=rtsp_url, verbose=True)
                onvif_request = OnvifRequest(
                    username=values['-user-'], password=values['-pass-'])
                url = f"http://{values['-ipaddr-']}:{values['-onvif_port-']}/"
                headers = {'Content-Type': 'text/xml; charset=utf-8'}
                is_streaming = True
                self._inited_ptz = True

            elif event == '-stop-':
                is_streaming = False
                img = Image.new("RGB", (640, 360), color=0)
                window['image'].update(data=ImageTk.PhotoImage(img))

            elif "-pt_" in event or self._inited_ptz:
                x, y = self._cur_x, self._cur_y
                x = (x + self._X_STP) if "right" in event else x
                x = (x - self._X_STP) if "left" in event else x
                y = (y + self._Y_STP) if "top" in event else y
                y = (y - self._Y_STP) if "btm" in event else y
                x = self._X_MAX if x > self._X_MAX else x
                self._cur_x = self._X_MIN if x < self._X_MIN else x
                y = self._Y_MAX if y > self._Y_MAX else y
                self._cur_y = self._Y_MIN if y < self._Y_MIN else y

                print(event, "x:", self._cur_x, "y:", self._cur_y)
                if is_streaming:
                    oreq = onvif_request.absolute_move(
                        self._cur_x, self._cur_y)
                    req = urllib.request.Request(
                        url,
                        data=oreq.encode(),
                        method='POST',
                        headers=headers)
                    try:
                        with urllib.request.urlopen(req) as response:
                            pass
                            # obody = response.read()
                            # oheaders = response.getheaders()
                            # ostatus = response.getcode()
                            # print(oheaders)
                            # print(ostatus)
                            # print(obody)
                    except urllib.error.URLError as e:
                        print(e.reason)
                    self._inited_ptz = False

            if is_streaming:
                frame = client.read()
                if frame is not None:
                    frame_resized = frame.resize(
                        (frame.width // 2, frame.height // 2))
                    window['image'].update(
                        data=ImageTk.PhotoImage(frame_resized))
                else:
                    print("none")

        window.close()


if __name__ == '__main__':

    camera_type = sys.argv[-1]
    if camera_type not in list(config.tapo.keys()):
        print("Please one of these options: ",
              list(config.tapo.keys()))
        exit()
    tapocfg = config.tapo[camera_type]

    tapogui = TapoGUI(
        user=tapocfg['USER'],
        password=tapocfg['PASSWORD'],
        ipaddr=tapocfg['IPADDR'],
        port=tapocfg['PORT'],
        stream=tapocfg['STREAM'],
        onvif_port=tapocfg['ONVIF_PORT'])
    tapogui.open()
