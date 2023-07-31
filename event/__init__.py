import re
from typing import Callable
from .register import RegisterEvent


class SipMessageData:
    @staticmethod
    def unknow_data(sip_message: str) -> None:
        print("unknow_data", sip_message)
        return {}, ""

    @staticmethod
    def remote_register_data(register_msg: str) -> dict:
        """
        未携带密码
        ---
        REGISTER sip:44010200492000000001@4401020049 SIP/2.0
        Via: SIP/2.0/UDP 192.168.10.204:5060;rport;branch=z9hG4bK1434213866
        From: <sip:44010200492000000001@4401020049>;tag=1890704200
        To: <sip:44010200492000000001@4401020049>
        Call-ID: 523724860
        CSeq: 1 REGISTER
        Contact: <sip:44010200492000000001@192.168.10.204:5060>
        Max-Forwards: 70
        User-Agent: IP Camera
        Expires: 3600
        Content-Length: 0
        ---
        携带密码
        ---
        REGISTER sip:44010200492000000001@4401020049 SIP/2.0
        Via: SIP/2.0/UDP 192.168.10.204:5060;rport;branch=z9hG4bK234453321
        From: <sip:37063400991327000011@4401020049>;tag=1965084906
        To: <sip:37063400991327000011@4401020049>
        Call-ID: 309601319
        CSeq: 2 REGISTER
        Contact: <sip:37063400991327000011@192.168.10.204:5060>
        Authorization: Digest username="44010200492000000001", realm="4401020049", nonce="ff224c7148a90848b6b98596224111b6", uri="sip:44010200492000000001@4401020049", response="5e17716de567f10d507c410dc924ca1b", algorithm=MD5, cnonce="0a4f113b", qop=auth, nc=00000001
        Max-Forwards: 70
        User-Agent: IP Camera
        Expires: 3600
        Content-Length: 0
        """
        plat_form_info_match = re.search(
            r"REGISTER sip:(.+)@(.+) SIP/2.0", register_msg
        )
        platform_gb_id = plat_form_info_match.group(1)
        platform_gb_domain = plat_form_info_match.group(2)
        device_via_match = re.search(r"Via: SIP/2.0/(.+) (.+)branch=(.+)", register_msg)
        sip_schema = device_via_match.group(1)
        device_branch = device_via_match.group(3)
        device_to_info_match = re.search(r"To: <sip:(.+)@(.+)>", register_msg)
        device_id = device_to_info_match.group(1)
        device_domain = device_to_info_match.group(2)
        remote_from_tag = re.search(r"tag=(.+)\r\n", register_msg).group(1)
        remote_call_id = re.search(r"Call-ID: (.+)", register_msg).group(1)
        remote_cseq = re.search(r"CSeq: (.+)", register_msg).group(1)
        remote_device_name = re.search(r"User-Agent: (.+)\r\n", register_msg).group(1)
        remote_device_expires_match = re.search(r"Expires: (.+)\r\n", register_msg)
        remote_device_expires = (
            remote_device_expires_match.group(1)
            if remote_device_expires_match
            else 3600
        )
        device_sip_info_match = (
            re.search(r"Contact: <sip:(.+)@(.+)>", register_msg).group(2).split(":")
        )
        device_sip_ip = device_sip_info_match[0]
        device_sip_port = device_sip_info_match[1]
        auth_match = re.search(r"Authorization: Digest (.+)\r\n", register_msg)
        if auth_match:
            auth_str = auth_match.group(1)
        auth_dict = {}
        if auth_match and auth_str:
            auth_list = auth_str.split(",")
            for auth_item in auth_list:
                kv = auth_item.split("=", 1)
                if len(kv) == 2:
                    auth_dict.update({kv[0].strip(): kv[1].strip().replace('"', "")})
        if auth_dict:
            auth_dict.update({"method": "REGISTER"})
        register_dict = dict(
            call_id=remote_call_id,
            cseq=remote_cseq,
            remote_device_name=remote_device_name,
            tag=remote_from_tag,
            platform_gb_id=platform_gb_id,
            platform_gb_domain=platform_gb_domain,
            device_id=device_id,
            device_domain=device_domain,
            device_sip_ip=device_sip_ip,
            device_sip_port=device_sip_port,
            device_branch=device_branch,
            sip_schema=sip_schema,
            auth_dict=auth_dict,
            device_expires=remote_device_expires,
        )
        return RegisterEvent.register_auth(
            register_dict, auth_flag=True, platform_password="admin123"
        )

    @staticmethod
    def remote_message_data(message_data: str):
        """
        MESSAGE sip:44010200492000000001@4401020049 SIP/2.0
        Via: SIP/2.0/UDP 192.168.10.204:5060;rport;branch=z9hG4bK1635477787
        From: <sip:37063400991327000011@4401020049>;tag=1399817579
        To: <sip:44010200492000000001@4401020049>
        Call-ID: 468291427
        CSeq: 20 MESSAGE
        Content-Type: Application/MANSCDP+xml
        Max-Forwards: 70
        User-Agent: IP Camera
        Content-Length:   181

        <?xml version="1.0" encoding="GB2312"?>
        <Notify>
        <CmdType>Keepalive</CmdType>
        <SN>136838</SN>
        <DeviceID>37063400991327000011</DeviceID>
        <Status>OK</Status>
        <Info>
        </Info>
        </Notify>
        """
        return {}, ""

    @classmethod
    def sip_message_transfer(cls, sip_message: str) -> Callable:
        sip_type = sip_message.split(" ")[0]
        return getattr(
            SipMessageData,
            f"remote_{sip_type.lower()}_data",
            SipMessageData.unknow_data,
        )
