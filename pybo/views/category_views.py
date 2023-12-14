from flask import Blueprint, render_template, url_for, request, g, flash
from pybo.models import Posting, Comment, User
from pybo.forms import PostingForm, CommentForm
from datetime import datetime
from werkzeug.utils import redirect
from .. import db
from pybo.views.auth_views import login_required   

bp = Blueprint('category', __name__, url_prefix='/category')


# 취업 게시판 페이지에 해당하는 라우트
@bp.route('/category1')
def category1():
    page = request.args.get('page', type=int, default=1)
    kw = request.args.get('kw', type=str, default='')
    posting_list = Posting.query.order_by(Posting.create_date.desc()).filter_by(category=0)
    if kw:
        search = '%%{}%%'.format(kw)
        sub_query = db.session.query(Comment.pid, Comment.content, User.username).join(User, Comment.uid == User.id).subquery()
        posting_list = posting_list.join(User).outerjoin(sub_query, sub_query.c.pid == Posting.id).filter(Posting.subject.ilike(search) |  # 질문제목
                    Posting.content.ilike(search) |  # 질문내용
                    User.username.ilike(search) |  # 질문작성자
                    sub_query.c.content.ilike(search) |  # 답변내용
                    sub_query.c.username.ilike(search)  # 답변작성자
                    ).distinct()
    posting_list = posting_list.paginate(page=page, per_page=10)
    return render_template('posting/posting_list.html', posting_list=posting_list, page=page, category_=0, kw=kw)



# 자유 게시판 페이지에 해당하는 라우트
@bp.route('/category2')
def category2():
    page = request.args.get('page', type=int, default=1)
    kw = request.args.get('kw', type=str, default='')
    posting_list = Posting.query.order_by(Posting.create_date.desc()).filter_by(category=1)
    if kw:
        search = '%%{}%%'.format(kw)
        sub_query = db.session.query(Comment.pid, Comment.content, User.username).join(User, Comment.uid == User.id).subquery()
        posting_list = posting_list.join(User).outerjoin(sub_query, sub_query.c.pid == Posting.id).filter(Posting.subject.ilike(search) |  # 질문제목
                    Posting.content.ilike(search) |  # 질문내용
                    User.username.ilike(search) |  # 질문작성자
                    sub_query.c.content.ilike(search) |  # 답변내용
                    sub_query.c.username.ilike(search)  # 답변작성자
                    ).distinct()
    posting_list = posting_list.paginate(page=page, per_page=10)
    return render_template('posting/posting_list.html', posting_list=posting_list, category_ = 1, page=page, kw=kw)

