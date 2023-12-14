from flask import Blueprint, url_for
from werkzeug.utils import redirect

bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/hello') # 위의 prefix 설정, 말그대로 prefix, 앞과 같이 '/'으로 설정 할 시 /"prefix"/을 의미
def hello_pybo():
    return 'Hello, Pybo!'

@bp.route('/')
def index():
   return redirect(url_for('question._list'))