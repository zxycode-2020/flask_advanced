# 这是一个官方提供的仅用于测试的wsgi程序
from wsgiref.simple_server import make_server

# 导入自己写框架
from webapp import application

# 创建一个服务
# 参数：host port 执行的任务
server = make_server('10.0.142.34', 5000, application)

# 启动服务
server.serve_forever()


