from flask import Flask, jsonify, abort, request, g
from flask_script import Manager
# 导入认证的类库
from flask_httpauth import HTTPBasicAuth
# 导入 restful类库
from flask_restful import Api, Resource
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'
manager = Manager(app)


# 创建Api对象
api = Api(app)

# 创建认证的对象
auth = HTTPBasicAuth()


# 生成token
def generate_token(expires_in=3600):
    s = Serializer(app.config['SECRET_KEY'], expires_in=expires_in)
    return s.dumps({'username': 'Jerry', 'password': '123456'})


# 校验token
def check_token(token):
    s = Serializer(app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except:
        return False
    g.username = data.get('username')
    return True


# 设置认证的回调函数，需要认证时自动回调，成功返回True，失败返回False
@auth.verify_password
def verify_password(username_or_token, password):
    # 这里是测试的假设数据，真实环境需要查询数据库
    if username_or_token == 'Jerry' and password == '123456':
        return True
    else:
        # 若用户名密码认证失败，再次尝试token认证
        if check_token(username_or_token):
            return True
        return False


# 认证的错误显示
@auth.error_handler
def unauthorized():
    return jsonify({'error': 'Unauthorized Access'}), 403


@app.route('/')
def index():
    return 'RESTful API 开发'


@app.route('/token')
@auth.login_required
def get_token():
    return generate_token()


@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'error': 'page not found'}), 404


@app.errorhandler(400)
def bad_request(e):
    return jsonify({'error': 'bad request'}), 400


# 创建资源，继承自Resource
class UserAPI(Resource):
    # 添加认证(资源保护)
    decorators = [auth.login_required]

    def get(self, id):
        #return {'User': 'GET'}
        return {'User': g.username}

    def put(self, id):
        return {'User': 'PUT'}

    def delete(self, id):
        return {'User': 'DELETE'}


class UserListAPI(Resource):
    def get(self):
        return {'UserList': 'GET'}

    def post(self):
        return {'UserList': 'POST'}


# 添加资源
# 参数1：资源的类名
# 参数2：路由地址，可以是多个
# endpoint：端点
api.add_resource(UserAPI, '/user/<int:id>', '/u/<int:id>', endpoint='user')
api.add_resource(UserListAPI, '/user', endpoint='users')


if __name__ == '__main__':
    manager.run()

