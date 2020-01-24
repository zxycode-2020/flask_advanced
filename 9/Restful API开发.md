# Restful API 开发

### 什么是Restful?

1. 简介

   ```
   REST即表述性状态传递（英文：Representational State Transfer，简称REST）是Roy Fielding博士在2000年他的博士论文中提出来的一种软件架构风格。它是一种针对网络应用的设计和开发方式，可以降低开发的复杂性，提高系统的可伸缩性。
   REST是一组架构约束条件和原则。满足这些约束条件和原则的应用程序或设计就是RESTful。需要注意的是，REST是设计风格而不是标准。
   ```

2. 资源

   ```
   RESTful接口就是围绕网络资源及相关动作展开的，所谓资源就是网络上的一个实体，或者是网络上的一个具体信息，总之用户能够使用的网络上的有效信息都称为资源。
   ```

3. 动作

   ```
   所谓动作就是数据的CURD。在良好的设计前提下，任何网络资源的操作都可以抽象为对网络资源的CURD动作。RESTful将网络资源的CURD操作抽象为HTTP的GET、POST、PUT、DELETE等动词的表达，具体的对照如下：
   ```

   | 方法     | 行为     | 示例                               |
   | ------ | ------ | -------------------------------- |
   | GET    | 获取资源信息 | http://127.0.0.1:5000/source     |
   | GET    | 获取指定资源 | http://127.0.0.1:5000/source/123 |
   | POST   | 创建新资源  | http://127.0.0.1:5000/source     |
   | PUT    | 更新资源   | http://127.0.0.1:5000/source/123 |
   | DELETE | 删除资源   | http://127.0.0.1:5000/source/123 |

   总结：使用一个资源时，通过不同的请求方法完成对资源不同的操作(CURD)

4. 数据

   通常RESTful风格的数据都采用json格式，有时通过url传参。

5. 测试工具

   说明：postman是一款非常优秀的http请求模拟工具

   下载：getpostman.com

   安装：无需安装，双击即可使用，跳过注册

   测试：见演示过程

### 原生实现RESTful API

1. CURD操作

   ```python
   # 添加RESTful的API接口
   # 获取资源列表
   @app.route('/posts', methods=['GET'])
   def get_posts_list():
       return 'GET：帖子列表展示'

   # 获取指定资源
   @app.route('/posts/<id>', methods=['GET'])
   def get_posts(id):
       return 'GET：%s号帖子详情' % id

   # 创建新资源
   @app.route('/posts', methods=['POST'])
   def create_posts():
       return 'POST：资源创建已完成'

   # 修改指定资源
   @app.route('/posts/<id>', methods=['PUT'])
   def update_posts(id):
       return 'PUT：%s号数据更新完成' % id

   # 删除指定资源
   @app.route('/posts/<id>', methods=['DELETE'])
   def delete_posts(id):
       return 'DELETE：%s号数据已删除' % id
   ```

2. 添加json数据并测试

   ```python
   posts = [
       {
           "id": 1,
           "title": "Python入门",
           "content": "很多人都认为Python的语法很简单，但是真正能够用好的又有几个"
       },
       {
           "id": 2,
           "title": "WEB开发入门",
           "content": "HTML看起来很简单，用起来也简单，但是写出优雅的页面还是有点难度的"
       }
   ]
   ```

   测试

   ```python
   # 获取资源列表
   @app.route('/posts', methods=['GET'])
   def get_posts_list():
       return jsonify({'posts': posts})

   # 获取指定资源
   @app.route('/posts/<int:pid>', methods=['GET'])
   def get_posts(pid):
       p = list(filter(lambda t: t['id'] == pid, posts))
       if len(p) == 0:
           abort(404)
       return jsonify({'posts': p[0]})

   # 修改指定资源
   @app.route('/posts/<int:pid>', methods=['PUT'])
   def update_posts(pid):
       #return 'PUT：%s号数据更新完成' % pid
       p = list(filter(lambda t: t['id'] == pid, posts))
       if len(p) == 0:
           abort(404)
       if 'title' in request.json:
           p[0]['title'] = request.json.get('title')
       if 'content' in request.json:
           p[0]['content'] = request.json.get('content')
       return jsonify({'posts': p[0]})
     
   # 删除指定资源
   @app.route('/posts/<int:pid>', methods=['DELETE'])
   def delete_posts(pid):
       #return 'DELETE：%d号数据已删除' % pid
       p = list(filter(lambda t: t['id'] == pid, posts))
       if len(p) == 0:
           abort(404)
       posts.remove(p[0])
       return jsonify({'result': '数据已删除'})
   ```

   练习：完成示例代码中的修改和删除资源

### 添加认证

说明：flask-httpauth扩展库可以提供简单的认证

安装：`pip install flask-httpauth`

使用：	

```python
# 导入认证的类库
from flask_httpauth import HTTPBasicAuth
# 创建认证的对象
auth = HTTPBasicAuth()

# 设置认证的回调函数，需要认证时自动回调，成功返回True，失败返回False
@auth.verify_password
def verify_password(username, password):
    # 这里是测试的假设数据，真实环境需要查询数据库
    if username == 'Jerry' and password == '123456':
        return True
    else:
        return False
    
# 认证的错误显示
@auth.error_handler
def unauthorized():
    return jsonify({'error': 'Unauthorized Access'}), 403
  
# 添加资源保护(需要认证才能访问)

# 获取资源列表
@app.route('/posts', methods=['GET'])
# 添加认证（路由保护）
@auth.login_required
def get_posts_list():
    # return 'GET：帖子列表展示'
    return jsonify({'posts': posts})
```

### flask-restful扩展库使用

安装：`pip install flask-restful`

使用：

```python
# 导入 restful类库
from flask_restful import Api

# 创建Api对象
api = Api(app)

# 创建资源，继承自Resource
class UserAPI(Resource):
    def get(self, id):
        return {'User': 'GET'}
    
    def put(self, id):
        return {'User': 'PUT'}
    
    def delete(self, id):
        return {'User': 'DELETE'}
  
# 添加资源
# 参数1：资源的类名
# 参数2：路由地址，可以是多个
# endpoint：端点
api.add_resource(UserAPI, '/user/<int:id>', '/u/<int:id>', endpoint='user')
```

一个资源的完整操作通常需要两个资源类体现，如下：

```python
# 创建资源，继承自Resource
class UserAPI(Resource):
    def get(self, id):
        return {'User': 'GET'}

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
api.add_resource(UserAPI, '/user/<int:id>', endpoint='user')
api.add_resource(UserListAPI, '/user', endpoint='users')
```

添加认证以完成对特定资源的保护

```python
class UserAPI(Resource):
    # 添加认证(资源保护)
    decorators = [auth.login_required]
	...
```

### token认证

token的生成和校验

```python
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

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
    return True
```

修改认证的方式

```python
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
```

