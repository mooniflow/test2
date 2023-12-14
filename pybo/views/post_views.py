from flask import Blueprint, render_template, url_for, request, g, flash
from pybo.models import Posting, Comment, User
from pybo.forms import PostingForm, CommentForm
from datetime import datetime
from werkzeug.utils import redirect
from .. import db
from pybo.views.auth_views import login_required     

bp = Blueprint('posting', __name__, url_prefix='/posting')


# @bp.route('/')
# def hello_pybo():
#     return 'Hello, Pybo!'

@bp.route('/list/')
def _list():
    page = request.args.get('page', type=int, default=1)
    kw = request.args.get('kw', type=str, default='')
    posting_list = Posting.query.order_by(Posting.create_date.desc())
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
    return render_template('posting/posting_list.html', posting_list=posting_list, category_ = 3, page=page, kw=kw)


@bp.route('/detail/<int:posting_id>/')
def detail(posting_id):
    form = CommentForm()
    posting = Posting.query.get_or_404(posting_id)
    
    cnt = 0
    best = 0
    for comment in posting.comment_set:
        if len(comment.voter) >= cnt:
            cnt = len(comment.voter)
            best = comment.id
    

    return render_template('posting/posting_detail.html', posting=posting, form=form, best = best)


@bp.route('/create/', methods=('GET', 'POST'))
@login_required
def create():
    form = PostingForm()
    if request.method == 'POST' and form.validate_on_submit():
        posting = Posting(subject=form.subject.data,
                          content=form.content.data, create_date=datetime.now(), user=g.user, category=form.category.data)
        db.session.add(posting)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('posting/posting_form.html', form=form)

@bp.route('/modify/<int:posting_id>', methods=('GET', 'POST'))
@login_required
def modify(posting_id):
    posting = Posting.query.get_or_404(posting_id)
    if g.user != posting.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('posting.detail', posting_id=posting_id))
    if request.method == 'POST':  # POST 요청
        form = PostingForm()
        if form.validate_on_submit():
            form.populate_obj(posting)
            posting.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            return redirect(url_for('posting.detail', posting_id=posting_id))
    else:  # GET 요청
        form = PostingForm(obj=posting)
    return render_template('posting/posting_form.html', form=form)

@bp.route('/delete/<int:posting_id>')
@login_required
def delete(posting_id):
    posting = Posting.query.get_or_404(posting_id)
    if g.user != posting.user:
        flash('삭제권한이 없습니다')
        return redirect(url_for('posting.detail', posting_id=posting_id))
    db.session.delete(posting)
    db.session.commit()
    return redirect(url_for('posting._list'))


@bp.route('/vote/<int:pid>/')
@login_required
def vote(pid):
    _question = Posting.query.get_or_404(pid)
    if g.user == _question.user:
        flash('본인이 작성한 글은 추천할수 없습니다')
    else:
        _question.voter.append(g.user)
        db.session.commit()
    return redirect(url_for('posting.detail', posting_id=pid))