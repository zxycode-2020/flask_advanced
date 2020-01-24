from flask import Flask, jsonify, abort, request
from flask_script import Manager
# 导入认证的类库
from flask_httpauth import HTTPBasicAuth


app = Flask(__name__)
manager = Manager(app)


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


@app.route('/')
def index():
    return 'RESTful API 开发'


@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'error': 'page not found'}), 404


@app.errorhandler(400)
def bad_request(e):
    return jsonify({'error': 'bad request'}), 400


# 添加RESTful的API接口
# 获取资源列表
@app.route('/posts', methods=['GET'])
# 添加认证（路由保护）
@auth.login_required
def get_posts_list():
    # return 'GET：帖子列表展示'
    return jsonify({'posts': posts})


# 获取指定资源
@app.route('/posts/<int:pid>', methods=['GET'])
def get_posts(pid):
    # return 'GET：%d号帖子详情' % pid
    p = list(filter(lambda t: t['id'] == pid, posts))
    if len(p) == 0:
        abort(404)
    return jsonify({'posts': p[0]})


# 创建新资源
@app.route('/posts', methods=['POST'])
def create_posts():
    # return 'POST：资源创建已完成'
    if not request.json or 'title' not in request.json or 'content' not in request.json:
        abort(400)
    # 新建资源
    post = {
        "id": posts[-1]['id'] + 1,
        "title": request.json['title'],
        "content": request.json['content']
    }
    # 保存资源
    posts.append(post)
    return jsonify({'posts': post}), 201


# 修改指定资源
@app.route('/posts/<int:pid>', methods=['PUT'])
def update_posts(pid):
    #return 'PUT：%d号数据更新完成' % pid
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


if __name__ == '__main__':
    manager.run()

