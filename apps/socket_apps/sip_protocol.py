from twisted.internet import protocol
from models import GBDeviceModel
from models.base import db
from event import SipMessageData


class SIPProtocol(protocol.DatagramProtocol):
    def datagramReceived(self, data, address):
        sip_message = data.decode()
        if len(address) < 2 or not sip_message.strip():
            return
        remote_sip_ip = address[0]
        remote_sip_port = address[1]
        print(
            f"remote ip: {remote_sip_ip}\r\n remote port: {remote_sip_port}\r\n remote sip data: {sip_message}"
        )
        func = SipMessageData.sip_message_transfer(sip_message)
        device_info, res_str = func(sip_message)
        if device_info:
            with db:
                GBDeviceModel.create(**device_info)
        print(res_str)
        response = res_str.encode()
        self.transport.write(response, address)
