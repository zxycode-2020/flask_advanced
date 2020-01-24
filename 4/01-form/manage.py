import os
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'xxx'
# 使用本地扩展库中的文件，不是项目根目录下的static
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
manager = Manager(app)
bootstrap = Bootstrap(app)


class NameForm(FlaskForm):
    #name = StringField('用户名', validators=[DataRequired(), Length(2, 8, message='大哥，此处需要2~8个字符')])
    name = StringField('用户名', validators=[DataRequired()])
    submit = SubmitField('提交')

    # 自定义验证器函数，格式'validate_字段'
    def validate_name(self, field):
        if len(field.data) < 6:
            raise ValidationError('不能少于6个字符')



@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        # 获取原来的名字
        last_name = session.get('name')
        if last_name is not None and last_name != form.name.data:
            flash('大哥，您的名字又换了')
        session['name'] = form.name.data
        return redirect(url_for('index'))
    name = session.get('name')
    return render_template('index.html', form=form, name=name)


if __name__ == '__main__':
    manager.run()

