import xml.etree.ElementTree as ET


class XmlHelper:
    @staticmethod
    def xmlstr_to_dict(xlm_str: str) -> dict:
        xlm_str = xlm_str.strip()
        # 找到字符串中的第一个"<"的索引
        start_index = xlm_str.index("<")
        # 使用字符串切片获取XML部分
        xml_string = xlm_str[start_index:]
        # 将XML字符串解析为Element对象
        root = ET.fromstring(xml_string)
        # 将Element对象转换为字典
        xml_dict = {}
        for child in root:
            xml_dict[child.tag] = child.text
        return xml_dict
