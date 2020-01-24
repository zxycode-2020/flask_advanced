from flask import Flask, render_template, request
from flask_script import Manager
import os
# 导入上传相关类库及函数
from flask_uploads import UploadSet, IMAGES, configure_uploads, patch_request_class


app = Flask(__name__)
manager = Manager(app)


# 配置上传文件的最大尺寸，默认不限制大小
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 16
# 配置上传文件的保存目录，还可以是FILES/DEFAULT
app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd()


# 文件类型过滤
photos = UploadSet('photos', IMAGES)
# 上传配置
configure_uploads(app, photos)
# 配置上传文件大小，默认64M，设置为None，会读取配置中的MAX_CONTENT_LENGTH选项
patch_request_class(app, size=None)


# 生成随机的字符串
def rand_str(length=32):
    import random
    base_str = 'abcdefghijklmnopqrstuvwxyz1234567890'
    return ''.join(random.choice(base_str) for i in range(length))


@app.route('/', methods=['GET', 'POST'])
def index():
    img_url = None
    if request.method == 'POST' and 'photo' in request.files:
        # 获取文件后缀
        suffix = os.path.splitext(request.files['photo'].filename)[1]
        # 生成随机的文件名，然后拼接后缀
        name = rand_str() + suffix
        # 保存文件
        filename = photos.save(request.files['photo'], name=name)
        # 获取文件的url
        img_url = photos.url(filename)
    return render_template('index.html', img_url=img_url)

if __name__ == '__main__':
    manager.run()
