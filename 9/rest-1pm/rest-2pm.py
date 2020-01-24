from flask import Flask, jsonify, abort, request
from flask_script import Manager
# 导入认证的类库
from flask_httpauth import HTTPBasicAuth

from flask_restful import Api,Resource

app = Flask(__name__)
manager = Manager(app)
api=Api(__name__)
auth = HTTPBasicAuth()
#设置认证的回调函数
#设置认证的回调函数，需要认证时自动回调，成功返回True
@auth.verify_password
def verify_password(username,password):
    if username == 'ZXY' and password == 'asdqwe':
        return True
    else:
        return False
@auth.error_handler
def unauthorized():
    return jsonify({'error':'Unauthorized Access'}),403



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

#定义404错误界面
@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'error': 'page not found'}), 404
#定义400错误
@app.errorhandler(400)
def bad_request(e):
    return jsonify({'error': 'bad request'}), 400

#添加RESTful的API接口
#获取资源列表
@app.route('/posts',methods=['GET'])
# #添加认证
# @auth.login_required
# def get_posts_list():
#     return jsonify({'posts':posts})
#
#
# #获取指定资源
# @app.route('/posts/<int:pid>',methods=['GET'])
# def get_posts(pid):
#     p=list(filter(lambda t: t['id'] == pid,posts))
#     if len(p) == 0:
#         abort(404)
#     return jsonify({'posts':p[0]})
#
# #创建新资源
# @app.route('/posts',methods=['POST'])
# def create_posts():
#     if not request.json or 'title' not in request.json or 'content' not in request.json:
#         abort(400)
#     #新建资源
#     post = {
#         "id":posts[-1]['id']+1,
#         'title':request.json['title'],
#         'content':request.json['content']
#     }
#     #保存资源
#     posts.append(post)
#     return jsonify({'posts':post}),201
#
# #修改资源
# @app.route('/posts/<int:ppid>',methods=['PUT'])
# def put_posts(ppid):
#     p = list(filter(lambda t: t['id'] == ppid, posts))
#     if len(p) == 0:
#         abort(400)
#     #新建资源
#     if 'title' in request.json:
#         p[0]['title']=request.json.get('title')
#     if 'content' in request.json:
#         p[0]['content']=request.json.get('content')
#
#     return jsonify({'posts':p[0]})
#
#
# #删除指定资源
# @app.route('/posts/<int:pid>',methods=['DELETE'])
# def delete_posts(pid):
#     p=list(filter(lambda t: t['id'] == pid,posts))
#     if len(p) == 0:
#         abort(404)
#     posts.remove(p[0])
#     return jsonify({'posts':posts})






#添加RESTful的API接口
#获取资源列表
# @app.route('/posts/',methods=['GET'])
# def get_posts_list():
#     return 'GET:Z帖子列表展示'
#
# #获取指定资源
# @app.route('/posts/<id>',methods=['GET'])
# def get_posts(id):
#     return 'GET:%s号帖子详情'% id
#
# #创建新资源
# @app.route('/posts/',methods=['POST'])
# def create_posts():
#     return 'POST:资源创建已完成'
#
# #修改指定资源
# @app.route('/posts/<id>',methods=['PUT'])
# def update_posts(id):
#     return 'PUT:%s号数据更新完成' % id
#
# #删除制定资源
# @app.route('/posts/<id>',methods=['DELETE'])
# def delete_posts(id):
#     return 'DELETE:%s号数据已删除'% id


class UserAPI(Resource):
    def get(self,id):
        return {'User':'GET'}
    def put(self,id):
        return {'User':'PUT'}
    def delete(self,id):
        return {'User':'DELETE'}

#添加资源
#参数1：资源的类名
#参数2：路由地址，可以是多个
#endpoint:端点

api.add_resource(UserAPI,'/user/<int:id>',endpoint = 'user')



















@app.route('/')
def hello_world():
    return 'RESTful API'


if __name__ == '__main__':
    manager.run()
