import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_script import Manager
from flask_bootstrap import Bootstrap
# 表单基本类库
from flask_wtf import FlaskForm
# 所需字段类型
from wtforms import StringField, SubmitField
# 验证器
from wtforms.validators import DataRequired


app = Flask(__name__)
# 秘钥，表单会用到，若不想公开写出来，可以配置环境变量
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or '很难猜到的字符串'
manager = Manager(app)
bootstrap = Bootstrap(app)


# 表单使用，定义一个表单类
class NameForm(FlaskForm):
    name = StringField('用户名', validators=[DataRequired()])
    submit = SubmitField('提交')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return 'Hello ' + request.form['username']
    return render_template('index.html')


@app.route('/form/', methods=['GET', 'POST'])
def test_form():
    form = NameForm()
    # 表单校验
    if form.validate_on_submit():
        session['name'] = form.name.data
        return redirect(url_for('test_form'))
    name = session.get('name')
    return render_template('test_form.html', form=form, name=name)

if __name__ == '__main__':
    manager.run()
