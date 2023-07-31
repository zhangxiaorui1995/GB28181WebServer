import hashlib
import random
import datetime
import inspect
from typing import Callable, Any


class RegisterEvent:
    @staticmethod
    def generate_nonce() -> str:
        """
        生成随机数
        :return: str
        """
        now_time = datetime.datetime.now().timestamp()
        rand = random.randint(1, 100)
        nonce_string = str(now_time) + str(rand)
        m = hashlib.md5()
        m.update(nonce_string.encode("GB2312"))
        return m.hexdigest()

    @staticmethod
    def authorized(
        cseq: str,
        call_id: str,
        tag: str,
        device_branch: str,
        device_sip_ip: str,
        device_sip_port: int,
        device_id: str,
        device_domain: str,
        device_expires: int,
        sip_schema: str = "UDP",
    ):
        """
        SIP/2.0 200 OK
        CSeq: 2 REGISTER
        Call-ID: 136407743
        From: <sip:44010200492000000001@3402000000>;tag=868343738
        To: <sip:44010200492000000001@3402000000>
        Via: SIP/2.0/UDP 192.168.10.204:5060;rport=5060;branch=z9hG4bK1882338342
        Date: 2023-07-28T09:06:08.397
        Contact: <sip:44010200492000000001@192.168.10.204:5060>
        Expires: 3600
        User-Agent: corerain
        Content-Length: 0
        """
        # 获取当前时间
        now = datetime.datetime.now()
        # 格式化时间字符串
        formatted_time = now.strftime("%Y-%m-%dT%H:%M:%S.%f")
        authorized_str = "SIP/2.0 200 OK\n"
        authorized_str += f"CSeq: {cseq}\n"
        authorized_str += f"Call-ID: {call_id}\n"
        authorized_str += f"From: <sip:{device_id}@{device_domain}>;tag={tag}\n"
        authorized_str += f"To: <sip:{device_id}@{device_domain}>\n"
        authorized_str += f"Via: SIP/2.0/{sip_schema} {device_sip_ip}:{device_sip_port};rport;branch={device_branch}\n"
        authorized_str += f"Date: {formatted_time}\n"
        authorized_str += (
            f"Contact: <sip:{device_id}@{device_sip_ip}:{device_sip_port}>\n"
        )
        authorized_str += f"Expires: {device_expires}\n"
        authorized_str += f"User-Agent: GB28181Server\n"
        authorized_str += f"Content-Length: 0\n"
        authorized_str += "\n"
        return authorized_str

    @staticmethod
    def unauthorized(
        device_id: str,
        device_domain: str,
        cseq: str,
        call_id: str,
        tag: str,
        device_sip_ip: str,
        device_sip_port: int,
        device_branch: str,
        platform_gb_domain: str,
        platform_nonce: str = generate_nonce(),
        sip_schema: str = "UDP",
    ):
        """
        :param sip_uri: SIP设备编码@源域名
        """
        unauthorized_str = "SIP/2.0 401 Unauthorized\n"
        unauthorized_str += f"CSeq: {cseq}\n"
        unauthorized_str += f"Call-ID: {call_id}\n"
        unauthorized_str += f"From: <sip:{device_id}@{device_domain}>;tag={tag}\n"
        unauthorized_str += f"To: <sip:{device_id}@{device_domain}>\n"
        unauthorized_str += f"""Via: SIP/2.0/{sip_schema.upper()} {device_sip_ip}:{device_sip_port};rport;branch={device_branch}\n"""
        unauthorized_str += f"""WWW-Authenticate: Digest realm="{platform_gb_domain}",qop="auth",nonce="{platform_nonce}",algorithm=MD5\n"""
        unauthorized_str += f"User-Agent: GB28181Server\n"
        unauthorized_str += f"Content-Length: 0\n"
        unauthorized_str += "\n"
        return unauthorized_str

    @staticmethod
    def do_auth(auth_data: dict, password: str = "admin123") -> bool:
        """
        {'username': '44010200492000000001', 'realm': '4401020049', 'nonce': 'ff224c7148a90848b6b98596224111b6',
        'uri': 'sip:44010200492000000001@4401020049', 'response': '5e17716de567f10d507c410dc924ca1b',
        'algorithm': 'MD5', 'cnonce': '0a4f113b', 'qop': 'auth', 'nc': '00000001', 'method': 'REGISTER'}
        """
        if not auth_data:
            return False
        username, realm, password, uri, method, nonce = (
            auth_data.get("username"),
            auth_data.get("realm"),
            password,
            auth_data.get("uri"),
            auth_data.get("method"),
            auth_data.get("nonce"),
        )
        nc = auth_data.get("nc").strip()
        qop = auth_data.get("qop").strip()
        cnonce = auth_data.get("cnonce").strip()
        A1 = "{}:{}:{}".format(username, realm, password)
        A2 = "{}:{}".format(method, uri)
        m = hashlib.md5(A1.encode("utf-8"))
        HA1 = m.digest().hex()
        m = hashlib.md5(A2.encode("utf-8"))
        HA2 = m.digest().hex()
        KD = "{}:{}:{}:{}:{}:{}".format(HA1, nonce, nc, cnonce, qop, HA2)
        m = hashlib.md5(KD.encode("utf-8"))
        md_string = m.digest().hex()
        response_value = auth_data.get("response")
        if md_string == response_value:
            return True
        return False

    @staticmethod
    def run_func__with_params(func: Callable, param: dict) -> Any:
        sig = inspect.signature(func)
        default_param_keys = sig.parameters.keys()
        new_params = {}
        for default_param_key in default_param_keys:
            if param.get(default_param_key, "__zero_data_flag") != "__zero_data_flag":
                new_params[default_param_key] = param.get(default_param_key)
        return func(**new_params)

    @classmethod
    def register_auth(
        cls, register_dict: dict, auth_flag: bool = True, platform_password: str = ""
    ):
        device_info = {}
        auth_data = register_dict.get("auth_dict", {})
        if not auth_flag or cls.do_auth(
            auth_data=auth_data, password=platform_password
        ):
            register_result = cls.run_func__with_params(cls.authorized, register_dict)
            device_info.update(
                dict(
                    device_name=register_dict.get("remote_device_name", "未命名"),
                    device_domain=register_dict.get(
                        "platform_gb_domain", "000000000000"
                    ),
                    socket_type=1
                    if register_dict.get("sip_schema", "UDP") == "UDP"
                    else 2,
                    device_id=register_dict.get("device_id", "0000000000000000000"),
                )
            )
        else:
            register_result = cls.run_func__with_params(cls.unauthorized, register_dict)

        return device_info, register_result
