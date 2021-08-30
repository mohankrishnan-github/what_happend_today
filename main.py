from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from sqlalchemy.orm import relationship
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import SubmitField, TextField
from wtforms.validators import DataRequired
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from random import choice
app = Flask(__name__)
app.config['SECRET_KEY'] = "ilikebigbuttandicannotlie"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///personel.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
quotes = ['The life of every person is like a diary in which he means to write one story, and writes another.', 'When all is said and done, leading a good life is more important than keeping a good diary.', 'A diary is the last place to go if you wish to seek the truth about a person. Nobody dares to make the final confession to themselves on paper: or at least, not about love.', 'History is the diary of humankind; to forget it is to try to navigate the future with no memory of the past.', 'Making records should be fun.', "Keep a diary, and someday it'll keep you.", 'Write a diary, imagining that you are trying to make an old person jealous.', "To write a diary every day is like returning to one's own vomit.", 'Writing is a socially acceptable form of schizophrenia.', 'A journal should be neither an echo nor a pander.', 'Keeping a journal implies hope.', 'You may be keeping a diary of your thoughts but know that, in every religion, the God you believe is keeping a diary of your actions.', 'Memory is the diary that we all carry about with us.', 'Each new day is a blank page in the diary of your life.', 'One advantage in keeping a diary is that you become aware with reassuring clarity of the changes which you constantly suffer.', 'Some of what you write may be humdrum dates and places, but there will also be rich passages that will be quoted by your posterity.', "A diary is an assassin's cloak which we wear when we stab a comrade in the back with a pen.", "Everyone should have a form of a diary, it's a great release.", 'A diary is more or less the work of a man of clay whose hands are clumsy and in whose eyes there is no light.', 'All records are made to be broken.', 'Keeping a diary is like closing your bedroom door and refusing to come out until dinnertime: it is a declaration of self.', 'A great library contains the diary of the human race.', "A proper family diary with everyone's events and parties in it really helps organise the household.", 'Oh, this is a dear diary moment.', 'Painting is just another way of keeping a diary.', 'Writing is not necessarily something to be ashamed of, but do it in private and wash your hands afterward.', 'Nothing matters but the writing. There has been nothing else worthwhile a stain upon the silence.', 'The diary will really try and tell people who you are and what you were. The alternative is writing nothing, or creating a totally lifeless, as it is leafless, garden.', "A diary need not be a dreary chronicle of one's movements; it should aim rather at giving salient account of some particular episode, a walk, a book, a conversation.", 'As we live longer and healthier for longer, we need to keep ourselves busy the diary is pretty full.', "It's the good girls who keep diaries; the bad girls never have the time.", 'I never travel without my diary; one should always have something sensational to read in the train.', 'She is so sure of getting her own way, she could even write her diary in advance.', 'The evolution of a new diary: double entry, single entry, blank.', 'Wars take longer nowadays because generals spend most of their time keeping diaries for future books.', 'Some people are such liars, they cannot even tell the truth in a diary.', "One always forgets the most important things, it's the things one can't remember that stay with you.", 'Life is all memory, except for the one present moment that goes by you so quickly you hardly catch it going.\n', "I'm not good at future planning. I don't plan at all. I don't know what I'm doing tomorrow. I don't have a day planner and I don't have a diary. I completely live in the now, not in the past, not in the future.", "Writing in a diary is a really strange experience for someone like me. Not only because I've never written anything before, but also because it seems to me that later on neither I nor anyone else will be interested in the musings of a thirteen-year-old schoolgirl.", 'Paper has more patience than people.', "Although diaries have often been dismissed as simplistic or artless of more 'highbrow' literary dgenres, in fact, dairies posses their own complexities.", 'Great. All I need is for some jerk to catch me carrying this book around and get the wrong idea.', 'A journal is a record of experiences and growth, not a preserve of things well done or said.', 'The charm of the journal must consist in a certain greeness, though fresh, and not in maturity.', 'Diaries are so multifaceted that every broad claim made about the genre within these pages should be understood to be provisional and will not apply to all diaries.', 'The diary is considered to be one of the the most significant literary expressions of this new, modern individual.', 'Diary is of a basically private nature and that it should not be published.', 'For such a diary to have meaning and impact, literary skill may be less effective than vanity, and a kind of brutal frankness is essential.', 'A diary is the ordinary sense can be a simple chronological record of day-to-day events.', 'A diary is a book. You write down how you felt or what you thought about the things that happened.', 'People keep diaries to help them remember what happened.', 'The diary exists at the margin of literature, and most diarists would label themselves as authors.', 'Although the diary is often taken to be a spontaneous expression of individuality, it is in fact a cultural practice that has a history.', 'Diary writing is necessarily discontinuous, a matter of stringing together disconnected entries. nd yet they are related to each other by rhythms of repetition and variation that may not be obvious.', 'The diary is a wager on the future. It bases the individual.. on ipseity, a sort of abstract commitment to remain faithful to oneself.', 'Dairies are records of a life process rather than finished narratives about a life, and as such they are only part of the practice of narrating and understanding what a life means.', 'Diaries remain a means of expressing oneself in writing, and its creation is based on the culture or the community at that historical moment.', 'The diary has become a dialogue with history and that history has been reconstructed within the pages of the journal written.', "Whatever your life, it is urging you to record it--to embrace the crumbs with the cake. It's why so many of us want to write memoir.", 'We have turned so fulllheartedly to the memoir form. We have an intuition that it can save us. Writing is the act of reaching across the abyss of isolation to share and reflect.']


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class PostForm(FlaskForm):
    message = TextField(validators=[DataRequired()])
    submit = SubmitField()


class User(UserMixin,db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(40), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)
    posts = relationship("Posts", back_populates="user")


class Posts(db.Model):
    __tablename__="posts"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = relationship("User", back_populates="posts")
    date = db.Column(db.String(20), nullable=False, unique=True)
    content = db.Column(db.String(500), nullable=False)


db.create_all()


def get_posts():
    all_posts = []
    for row in db.session.query(Posts).filter_by(user_id=current_user.id).order_by(desc(Posts.date)).all():
        all_posts.append({"id": row.id, "title": row.date, "content": row.content})
    return all_posts

@app.route("/")
def home():
    return redirect(url_for('login'))

@app.route("/posts")
@login_required
def posts():
    today = datetime.now()

    form = PostForm()
    all_posts = get_posts()
    return render_template("index.html" ,today=today.strftime("%B-%d, %Y"), form=form, posts=all_posts, quote=choice(quotes), user_name=current_user.name)


@app.route("/add_post", methods = ["GET", "POST"])
@login_required
def add_post():
    today = datetime.now()

    am_or_pm = "AM"
    if int(today.hour) > 11:
        am_or_pm = "PM"
    date = today.strftime(f"%A, %B-%d, %Y : %H:%M:%S {am_or_pm}")
    form = PostForm()
    message = form.message.data
    print(f"{date}\n{message}")
    new_post = Posts()
    new_post.user_id = current_user.id
    new_post.date = date
    new_post.content = message
    db.session.add(new_post)
    db.session.commit()
    return redirect(url_for('posts'))


@app.route("/post/<int:id>")
@login_required
def post(id):
    post = db.session.query(Posts).get(id)

    return render_template("post.html", post=post)


@app.route("/sign-up", methods = ["GET", "POST"])
def signup():
    if request.method == "POST":
        try:
            new_user = User()
            new_user.name = request.form.get("name")
            new_user.email = request.form.get("email")
            new_user.password = generate_password_hash(request.form.get("password"), method="pbkdf2:sha256", salt_length=8)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('home'))
        except :
            flash("Email ID exists try login or enter new one")
            return redirect(url_for('signup'))
    return render_template("signup.html",)


@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        user = db.session.query(User).filter_by(email = request.form.get("email")).first()
        if user:
            if check_password_hash(user.password, request.form.get("password")):
                login_user(user)
                return redirect(url_for('posts'))
            else:
                flash("Incorrect password")
                return redirect(url_for('login'))
        else:
            flash("Email ID doesn't exists")
            return redirect(url_for('login'))
    return render_template("login.html")


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))



app.run(debug=True)




