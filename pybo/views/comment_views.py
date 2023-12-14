from datetime import datetime

from flask import Blueprint, url_for, request, render_template, g, flash
from werkzeug.utils import redirect

from pybo import db
from ..forms import CommentForm, RecommentForm
from pybo.models import Posting, Comment, Recomment
from .auth_views import login_required


bp = Blueprint('comment', __name__, url_prefix='/comment')

@bp.route('/create/<int:posting_id>', methods=('POST',))
@login_required
def create(posting_id):
    form = CommentForm()
    posting = Posting.query.get_or_404(posting_id)
    if form.validate_on_submit():
        content = request.form['content']
        # user = Comment.query.get_or_404(user_id)
        comment = Comment(pid=posting.id, content=content, create_date=datetime.now(), user=g.user)
        # comment = Comment()
        posting.comment_set.append(comment)
        db.session.commit()
        return redirect(url_for('posting.detail', posting_id=posting_id))
    return render_template('posting/posting_detail.html', posting=posting, form=form)

@bp.route('/modify/<int:comment_id>', methods=('GET', 'POST'))
@login_required
def modify(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if g.user != comment.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('posting.detail', posting_id=comment.posting.id))
    if request.method == "POST":
        form = CommentForm()
        if form.validate_on_submit():
            form.populate_obj(comment)
            comment.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            return redirect(url_for('posting.detail', posting_id=comment.posting.id))
    else:
        form = CommentForm(obj=comment)
    return render_template('comment/comment_form.html', form=form)

@bp.route('/delete/<int:comment_id>')
@login_required
def delete(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    posting_id = comment.posting.id
    if g.user != comment.user:
        flash('삭제권한이 없습니다')
    else:
        db.session.delete(comment)
        db.session.commit()
    return redirect(url_for('posting.detail', posting_id=posting_id))

@bp.route('/vote/<int:comment_id>/')
@login_required
def vote(comment_id):
    _question = Comment.query.get_or_404(comment_id)
    pid = _question.pid
    if g.user == _question.user:
        flash('본인이 작성한 글은 추천할수 없습니다')
    else:
        _question.voter.append(g.user)
        db.session.commit()
    return redirect(url_for('posting.detail', posting_id=pid))