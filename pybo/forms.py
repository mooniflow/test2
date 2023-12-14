from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo

class PostingForm(FlaskForm):
    subject = StringField('제목', validators=[DataRequired('제목은 필수입력 항목입니다.')])
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수입력 사항입니다.')])
    category = StringField('카테고리', validators=[DataRequired('카테고리는 필수입력 사항입니다.')])

class CommentForm(FlaskForm):
    content = TextAreaField('댓글', validators=[DataRequired('내용은 필수입력 항목입니다.')])

class RecommentForm(FlaskForm):
    content = TextAreaField('대댓글', validators=[DataRequired('내용은 필수입력 항목입니다.')])

class UserCreateForm(FlaskForm):
    username = StringField('사용자이름', validators=[DataRequired(), Length(min=3, max=25)])
    password1 = PasswordField('비밀번호', validators=[
        DataRequired(), EqualTo('password2', '비밀번호가 일치하지 않습니다')])
    password2 = PasswordField('비밀번호확인', validators=[DataRequired()])

class UserLoginForm(FlaskForm):
    username = StringField('사용자이름', validators=[DataRequired(), Length(min=3, max=25)])
    password = PasswordField('비밀번호', validators=[DataRequired()])

