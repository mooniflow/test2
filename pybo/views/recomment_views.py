from datetime import datetime

from flask import Blueprint, url_for, request, render_template, g, flash
from werkzeug.utils import redirect

from pybo import db
from ..forms import CommentForm, RecommentForm
from pybo.models import Posting, Comment, Recomment
from .auth_views import login_required


bp = Blueprint('recomment', __name__, url_prefix='/recomment')

@bp.route('/create/<int:comment_id>', methods=('GET', 'POST'))
@login_required
def recomment(comment_id):
    form = RecommentForm()
    comment = Comment.query.get_or_404(comment_id)
    if form.validate_on_submit():
        content = request.form['content']
        recomment = Recomment(pid=comment, content=content, create_date=datetime.now(), user=g.user)
        # recomment = Comment()
        comment.recomment_set.append(recomment)
        db.session.commit()
        return redirect(url_for('posting.detail', posting_id=comment.posting.id))
    return render_template('comment/recomment_form.html', form=form)

@bp.route('/modify/<int:recomment_id>', methods=('GET', 'POST'))
@login_required
def modify(recomment_id):
    recomment = Recomment.query.get_or_404(recomment_id)
    if g.user != recomment.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('posting.detail', posting_id=recomment.pid))
    if request.method == "POST":
        form = RecommentForm()
        if form.validate_on_submit():
            form.populate_obj(recomment)
            recomment.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            return redirect(url_for('posting.detail', posting_id=recomment.pid))
    else:
        form = RecommentForm(obj=recomment)
    return render_template('comment/recomment_form.html', form=form)

@bp.route('/delete/<int:recomment_id>')
@login_required
def delete(recomment_id):
    recomment = Recomment.query.get_or_404(recomment_id)
    recomment_id = recomment.posting.id
    if g.user != recomment.user:
        flash('삭제권한이 없습니다')
    else:
        db.session.delete(recomment)
        db.session.commit()
    return redirect(url_for('posting.detail', posting_id=recomment.pid))