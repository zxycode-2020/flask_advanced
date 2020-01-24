from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class PostsForm(FlaskForm):
    # 如果想要设置字段的其它属性，可以通过render_kw完成
    content = TextAreaField('', render_kw={'placeholder': '这一刻的想法...'}, validators=[DataRequired(), Length(1, 128, message='说话要注意影响，不多不少最好')])
    submit = SubmitField('发表')
