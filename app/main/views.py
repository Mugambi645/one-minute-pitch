from . import main
import flask
from flask_login import login_required,current_user
from flask import render_template,abort,redirect,url_for,request
from ..models import Role,User
from .forms import UpdateProfile,PitchForm,CommentForm
from .. import db,photos
from ..models import User,Pitch,Comment
from ..forms import UpdateProfile

#main route
@main.route("/")
def index():
    """
    view root page that returns the index page and its data
    """
    return render_template("index.html")

#profile
@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)


#photos logic
@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update_profile.html',form =form)


@main.route('/pitch/new', methods = ['GET','POST'])
@login_required
def new_pitch():
    pitch_form = PitchForm()
    if pitch_form.validate_on_submit():
        title = pitch_form.title.data
        pitch = pitch_form.text.data
        category = pitch_form.category.data
        # Updated pitch instance
        new_pitch = Pitch(pitch_title=title,pitch_content=pitch,category=category, user=current_user,likes=0,dislikes=0)

        # Save pitch method
        new_pitch.save_pitch()
        return redirect(url_for('.index'))

    title = 'New pitch'
    return render_template('new_pitch.html',title = title,pitch_form=pitch_form )




@main.route('/pitches/science_pitches')
def science_pitches():

    pitches = Pitch.get_pitches('science')

    return render_template("science_pitches.html", pitches = pitches)


@main.route('/pitches/anaconda_pitches')
def anaconda_pitches():

    pitches = Pitch.get_pitches('anaconda')

    return render_template("anaconda_pitches.html", pitches = pitches)


@main.route('/pitches/alien_pitches')
def alien_pitches():

    pitches = Pitch.get_pitches('alien')

    return render_template("alien_pitches.html", pitches = pitches)



@main.route('/pitches/birds_pitches')
def birds_pitches():

    pitches = Pitch.get_pitches('birds')

    return render_template("birds_pitches.html", pitches = pitches)


@main.route('/pitches/culture_pitches')
def culture_pitches():

    pitches = Pitch.get_pitches('culture')

    return render_template("culture_pitches.html", pitches = pitches)


@main.route('/pitches/poetry_pitches')
def poetry_pitches():

    pitches = Pitch.get_pitches('poetry')

    return render_template("poetry_pitches.html", pitches = pitches)


@main.route('/pitch/<int:id>', methods = ['GET','POST'])
def pitch(id):
    pitch = Pitch.get_pitch(id)
    posted_date = pitch.posted.strftime('%b %d, %Y')

    if request.args.get("like"):
        pitch.likes = pitch.likes + 1

        db.session.add(pitch)
        db.session.commit()

        return redirect("/pitch/{pitch_id}".format(pitch_id=pitch.id))
                                

    elif request.args.get("dislike"):
        pitch.dislikes = pitch.dislikes + 1

        db.session.add(pitch)
        db.session.commit()

        return redirect("/pitch/{pitch_id}".format(pitch_id=pitch.id))

    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        comment = comment_form.text.data

        new_comment = Comment(comment = comment,user = current_user,pitch_id = pitch)

        new_comment.save_comment()


    comments = Comment.get_comments(pitch)

    return render_template("pitch.html", pitch = pitch, comment_form = comment_form, comments = comments, date = posted_date)

@main.route('/user/<uname>/pitches')
def user_pitches(uname):
    user = User.query.filter_by(username=uname).first()
    pitches = Pitch.query.filter_by(user_id = user.id).all()
    pitches_count = Pitch.count_pitches(uname)
    

    return render_template("profile/user_pitches.html", user=user,pitches=pitches,pitches_count=pitches_count)
