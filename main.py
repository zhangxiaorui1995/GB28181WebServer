from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.wsgi import WSGIResource
from server import create_web_app, create_socket_app

web_app = create_web_app()
socket_app = create_socket_app()
# 创建Twisted WSGI资源
resource = WSGIResource(reactor, reactor.getThreadPool(), web_app)
# 创建Twisted Web站点
site = Site(resource)

# 启动Twisted Web服务
reactor.listenTCP(8080, site)
# reactor.listenUDP(5060, socket_app)
# reactor.listenTCP(5060, socket_app)

# 启动Twisted事件循环
reactor.run()
