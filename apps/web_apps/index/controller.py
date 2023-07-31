from . import index_blueprint


@index_blueprint.route("/")
@index_blueprint.route("/index")
def device_index():
    # 获取所有的设备
    return "hello, index"
