from flask import render_template,url_for,flash,redirect,request,Blueprint
from flask_login import login_user,current_user,logout_user,login_required
from CompanyBlog import db
from CompanyBlog.models import User, BlogPost
from CompanyBlog.Users.forms import RegistrationForm, LoginForm, UpdateUserForm
from CompanyBlog.Users.pictureHandler import addProfilePic


users = Blueprint('users',__name__)



#Register
@users.route('/register',methods=['POST','GET'])
def register():

    form = RegistrationForm()

    if form.validate_on_submit():

        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Thanks For Registeration!')

        return redirect(url_for('users.login'))

    return render_template('register.html',form=form)

#Login
@users.route('/login',methods=['POST','GET'])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        if user.checkPassword(form.password.data) and user is not None:
            print('User Found')
            login_user(user)
            flash('Login Successfully!')

            next = request.args.get('next')

            if next == None or not next[0] == '/':
                next = url_for('core.index')

            return redirect(next)

    return render_template('login.html',form=form)


#Logout
@users.route('/logout')
def logout():
    logout_user()

    return redirect(url_for('core.index'))


#Account (Update User Form)
@users.route('/account',methods=['GET','POST'])
@login_required
def account():

    form = UpdateUserForm()

    if form.validate_on_submit():

        if form.picture.data:

            username = current_user.username
            pic = addProfilePic(form.picture.data,username)
            current_user.profileImage = pic

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('User Account Updated!')

        return redirect(url_for('users.account'))

    elif request.method == 'GET':

        form.username.data = current_user.username
        form.email.data = current_user.email

    profileImage = url_for('static', filename='profile_pics/' + current_user.profileImage)

    return render_template('account.html',profileImage=profileImage, form=form)


#User's List of Blog Posts
@users.route('/<username>')
def userPosts(username):

    page = request.args.get('page',1,type=int)
    user = User.query.filter_by(username=username).first_or_404()
    blog_posts = BlogPost.query.filter_by(author=user).order_by(BlogPost.date.desc()).paginate(page=page, per_page=5)

    return render_template('user_blog_posts.html', blog_posts=blog_posts, user=user)
