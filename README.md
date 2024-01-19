# GB28181WebServer

- version:
- python >= 3.9

基于 flask+socket 实现 GB28181 服务

### TODO LIST

1. - [√] 作为上级级联注册、心跳保活
2. - [ ] 作为上级级联通道同步、目录同步
3. - [ ] 作为上级进行级联拉取实时流
4. - [ ] 适配流媒体服务(zlmedikit)

```yaml
# .env
database_name=gb28181  # 替换为你的数据库名称
database_engine=peewee.MySQLDatabase  # 使用Peewee的MySQLDatabase引擎
database_config={'user': 'root', 'password': 'gb28181', 'host': '192.168.0.18'}  # 替换为你的数据库连接配置
```
