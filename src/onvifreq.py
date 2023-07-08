#!/usr/bin/env python3

import os
import base64
import hashlib
from datetime import datetime


class OnvifRequest:

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def absolute_move(self, x, y):
        command = """
        <AbsoluteMove xmlns="http://www.onvif.org/ver20/ptz/wsdl">
            <ProfileToken>profile_1</ProfileToken>
            <Position>
                <PanTilt x="{x}" y="{y}" xmlns="http://www.onvif.org/ver10/schema" space="http://www.onvif.org/ver10/tptz/PanTiltSpaces/PositionGenericSpace"></PanTilt>
                <Zoom x="0.0" xmlns="http://www.onvif.org/ver10/schema" space="http://www.onvif.org/ver10/tptz/ZoomSpaces/PositionGenericSpace"></Zoom>
            </Position>
            <Speed>
                <PanTilt x="1" y="1" xmlns="http://www.onvif.org/ver10/schema" space="http://www.onvif.org/ver10/tptz/PanTiltSpaces/GenericSpeedSpace"/>
                <Zoom x="1.0" xmlns="http://www.onvif.org/ver10/schema" space="http://www.onvif.org/ver10/tptz/ZoomSpaces/ZoomGenericSpeedSpace"/>
            </Speed>
        </AbsoluteMove>
        """
        return self.request(self.username, self.password, command.format(x=x, y=y))

    def request(self, username, password, command):
        created = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z")
        raw_nonce = os.urandom(20)
        nonce = base64.b64encode(raw_nonce)
        sha1 = hashlib.sha1()
        sha1.update(raw_nonce + created.encode("utf8") + password.encode("utf8"))
        raw_digest = sha1.digest()
        digest = base64.b64encode(raw_digest)

        request = """
        <s:Envelope xmlns:s="http://www.w3.org/2003/05/soap-envelope">
        <s:Header>
            <Security xmlns="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" s:mustUnderstand="1">
            <UsernameToken>
                <Username>{username}</Username>
                <Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordDigest">{digest}</Password>
                <Nonce EncodingType="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-soap-message-security-1.0#Base64Binary">{nonce}</Nonce>
                <Created xmlns="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">{created}</Created>
            </UsernameToken>
            </Security>
        </s:Header>
        <s:Body xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
            {command}
        </s:Body>
        </s:Envelope>
        """
        return request.format(
            username=username,
            nonce=nonce.decode("utf8"),
            created=created,
            digest=digest.decode("utf8"),
            command=command,
        )
