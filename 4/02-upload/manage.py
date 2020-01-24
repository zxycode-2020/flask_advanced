from flask import Flask, render_template, request, url_for, send_from_directory
from flask_script import Manager
import os

app = Flask(__name__)
manager = Manager(app)

# 设置允许上传的文件后缀
ALLOWED_EXTENSIONS = set(['jpg', 'png', 'jpeg', 'gif'])
# 配置上传文件的最大尺寸，默认不限制大小
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 16
# 配置上传文件的保存目录
app.config['UPLOAD_FOLDER'] = os.getcwd()


# 判断是否是允许的文件后缀
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# 生成随机的字符串
def rand_str(length=32):
    import random
    base_str = 'abcdefghijklmnopqrstuvwxyz1234567890'
    return ''.join(random.choice(base_str) for i in range(length))


# 显示上传文件
@app.route('/show/<imagename>')
def show(imagename):
    # 发送指定的文件
    return send_from_directory(app.config['UPLOAD_FOLDER'], imagename)


@app.route('/', methods=['GET', 'POST'])
def index():
    img_url = None
    if request.method == 'POST':
        file = request.files.get('photo')
        # 上传信息得有，并且是允许的文件后缀
        if file and allowed_file(file.filename):
            # 获取文件后缀
            suffix = os.path.splitext(file.filename)[1]
            # 生成随机的文件名，然后拼接后缀
            filename = rand_str() + suffix
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            img_url = url_for('show', imagename=filename)
    return render_template('index.html', img_url=img_url)

if __name__ == '__main__':
    manager.run()
