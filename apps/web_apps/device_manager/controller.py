from flask import render_template
from playhouse.shortcuts import model_to_dict
from models import GBDeviceModel
from . import device_blueprint


@device_blueprint.route("/", methods=["GET", "POST"])
def device_index():
    # 获取所有的设备
    devices = [
        model_to_dict(_device_info)
        for _device_info in GBDeviceModel.select()
        if _device_info
    ]
    return render_template("index.html", devices=devices)
