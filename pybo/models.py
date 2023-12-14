from pybo import db 

post_voter = db.Table(
    'post_voter',
    db.Column('uid', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('pid', db.Integer, db.ForeignKey('posting.id', ondelete='CASCADE'), primary_key=True)
)

comment_voter = db.Table(
    'comment_voter',
    db.Column('user_id',  db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('comment_id', db.Integer, db.ForeignKey('comment.id', ondelete='CASCADE'), primary_key=True)
)

class Posting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    uid = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('posting_set'))
    mod_date = db.Column(db.DateTime(), nullable=True)
    modify_date = db.Column(db.DateTime(), nullable=True)
    category = db.Column(db.Integer, nullable=True, server_default='1')
    voter = db.relationship('User', secondary=post_voter, backref=db.backref('post_voter_set'))

    def __init__(self, **kwargs):
        super(Posting, self).__init__(**kwargs)
    
    
    
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pid = db.Column(db.Integer, db.ForeignKey('posting.id', ondelete='CASCADE')) # ondelete='CASCADE' : 해당하는 question이 삭제될시, answer들도 삭제된다.
    posting = db.relationship('Posting', backref=db.backref('comment_set'))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    uid = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('comment_set'))
    mod_date = db.Column(db.DateTime(), nullable=True)
    modify_date = db.Column(db.DateTime(), nullable=True)
    voter = db.relationship('User', secondary=comment_voter, backref=db.backref('comment_voter_set'))

    def __init__(self, **kwargs):
        super(Comment, self).__init__(**kwargs)
    
    
class Recomment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pid = db.Column(db.Integer, db.ForeignKey('comment.id', ondelete='CASCADE')) # ondelete='CASCADE' : 해당하는 question이 삭제될시, answer들도 삭제된다.
    comment = db.relationship('Comment', backref=db.backref('recomment_set'))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    uid = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('recomment_set'))
    mod_date = db.Column(db.DateTime(), nullable=True)

    def __init__(self, **kwargs):
        super(Recomment, self).__init__(**kwargs)
    
    
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    pw = db.Column(db.String(200), nullable=False)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)







