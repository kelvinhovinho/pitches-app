
from flask import render_template,request,redirect,url_for,abort
from . import main
from ..models import User,Pitch,Comment
from .forms import updateProfile,PitchForm,CommentForm
from .. import db,photos
from flask_login import login_required,current_user

@main.route('/')
def index():

    return render_template('index.html')

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    pitches = Pitch.query.filter_by(user_id = user.id).all()
    if user is None:
        abort(404)

    return render_template('profile/profile.html',user = user,pitches=pitches)   

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = updateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()
           
        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)  

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

@main.route('/pitch/newpitch',methods= ['POST','GET'])
@login_required
def newPitch():
    pitch = PitchForm()
    if pitch.validate_on_submit():
        title = pitch.pitch_title.data
        category = pitch.pitch_category.data;
        yourPitch = pitch.pitch_comment.data

        #update pitch instance

        newPitch = Pitch(pitch_title = title,pitch_category = category,pitch_comment = yourPitch,user= current_user)

        #save pitch
        newPitch.save_pitch()
        return redirect(url_for('.index'))

    title = 'NEW PITCH'
    return render_template('newPitch.html',title = title,pitchform = pitch)  

@main.route('/category/interview',methods= ['GET'])
def displayInterviewCategory():
    interviewPitches = Pitch.get_pitches('interview')
    return render_template('category/interview.html',interviewPitches = interviewPitches)
    
@main.route('/category/product',methods= ['POST','GET'])
def displayProductCategory():
    productPitches = Pitch.get_pitches('product')
    return render_template('category/product.html',productPitches = productPitches)

@main.route('/category/promotion',methods= ['POST','GET'])
def displayPromotionCategory():
    promotionPitches = Pitch.get_pitches('promotion')
    return render_template('category/promotion.html',promotionPitches = promotionPitches)

@main.route('/category/pickup',methods= ['POST','GET'])
def displayPickupCategory():
    pickupPitches = Pitch.get_pitches('pickup')
    return render_template('category/pickup.html',pickupPitches = pickupPitches)

@main.route('/comment/<int:id>',methods= ['POST','GET'])
@login_required
def viewPitch(id):
    onepitch = Pitch.getPitchId(id)
    comments = Comment.getComments(id)

    if request.args.get("like"):
        onepitch.likes = onepitch.likes + 1

        db.session.add(onepitch)
        db.session.commit()

        return redirect("/comment/{pitch_id}".format(pitch_id=pitch.id))

    elif request.args.get("dislike"):
        onepitch.dislikes = onepitch.dislikes + 1

        db.session.add(onepitch)
        db.session.commit()

        return redirect("/comment/{pitch_id}".format(pitch_id=pitch.id))

    commentForm = CommentForm()
    if commentForm.validate_on_submit():
        comment = commentForm.text.data

        newComment = Comment(comment = comment,user = current_user,pitch_id= id)

        newComment.saveComment()

    return render_template('comment.html',commentForm = commentForm,comments = comments,pitch = onepitch)

    






