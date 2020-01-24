from flask import Flask, render_template, request
from flask_script import Manager
import os
# 导入上传相关类库及函数
from flask_uploads import UploadSet, IMAGES, configure_uploads, patch_request_class
# 图片处理库，默认只支持python2.x，python3.x中使用需要安装Pillow
from PIL import Image

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField


app = Flask(__name__)
manager = Manager(app)


# 配置上传文件的最大尺寸，默认不限制大小
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 16
# 配置上传文件的保存目录，还可以是FILES/DEFAULT
app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd()
# 设置秘钥
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'xxx'


# 文件类型过滤
photos = UploadSet('photos', IMAGES)
# 上传配置
configure_uploads(app, photos)
# 配置上传文件大小，默认64M，设置为None，会读取配置中的MAX_CONTENT_LENGTH选项
patch_request_class(app, size=None)


class UploadForm(FlaskForm):
    photo = FileField(validators=[FileAllowed(photos, '只能上传图片'), FileRequired('请选择文件后再上传')])
    submit = SubmitField('上传')


@app.route('/', methods=['GET', 'POST'])
def index():
    img_url = None
    form = UploadForm()
    if form.validate_on_submit():
        # 保存文件
        filename = photos.save(form.photo.data)
        # 生成缩略图
        img = Image.open(filename)
        img.thumbnail((64, 64))
        img.save(filename)
        # 获取文件的url
        img_url = photos.url(filename)
    return render_template('index.html', form=form, img_url=img_url)

if __name__ == '__main__':
    manager.run()
