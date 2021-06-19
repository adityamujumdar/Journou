from flask import render_template, flash, redirect, url_for, request
from journou import app, db, bcrypt, socketio
from journou.forms import RegistrationForm, LoginForm, UpdateAccountForm
from journou.models import Users, Forums
from flask_login import login_user, current_user, logout_user, login_required
import secrets, os
from flask_socketio import send

from PIL import Image

@app.route("/home") # decorater for the website route
@app.route("/") # decorater for the website
def home_page():
    return render_template('home.html')
    
@app.route("/wikis/education")
def education_page():
    return render_template('education.html')

@app.route("/jobs/oncampusjobs")
def oncampusjobs_page():
    return render_template('oncampusjobs.html')

@app.route("/jobs/offcampusjobs")
def offcampusjobs_page():
    return render_template('offcampusjobs.html')

@app.route("/chatroom")
# @socketio.on('message')
# def chatroom_page(message):
def chatroom_page():
	# print(f"Message: {msg}")
	# send(msg, broadcast=True)
    return render_template('chatroom.html')

@app.route("/wikis/housing")
def housing_page():
    return render_template('housing.html')

@app.route("/wikis/flights")
def flights_page():
    return render_template('flights.html')

@app.route("/wikis/vocabularychanges")
def vocabularychanges_page():
    return render_template('vocabulary.html')

@app.route("/wikis/moneymanagement/")
def moneymanagement_page():
    return render_template('money.html')

@app.route("/wikis/helpfulwebsites/")
def helpfulwebsites_page():
    return render_template('websites.html')

@app.route("/login", methods=['GET', 'POST'])
def login_page():
	if current_user.is_authenticated:
		return redirect(url_for('home_page'))
	form = LoginForm()
	if form.validate_on_submit():
		user = Users.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('home_page'))
		else:
			flash(f'Login Unsuccessful. Please check email and password', 'danger wt-50 mt-3')
	return render_template('login.html', form=form)
	# return render_template('login.html')

@app.route("/register", methods=['GET', 'POST'])
def register_page():
	if current_user.is_authenticated:
		return redirect(url_for('home_page'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = Users(username=form.username.data, email=form.email.data, university=form.university.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash(f'Your account has been created!', 'success wt-50 mt-3')
		return redirect(url_for('login_page'))
	return render_template('register.html', form=form)
    # return render_template('register.html')


#  Forum pages
@app.route("/forums/education")
def education_forum_page():
	e_forums=[
		{
			# 'id': uuid.uuid4().hex,
			'forum_name': 'GRE scores needed to get scholarship at Arizona State University',
			'date_posted': '2021-05-05 10:10:10',
			'posted_by': 'Ugly_gravy122',
			'likes': 122,
			'dislikes': 22
		},
		{
			# 'id': uuid.uuid4().hex,
			'forum_name': 'How is the Computer Science program at Iowa State University',
			'date_posted': '2021-05-05 10:10:10',
			'posted_by': 'pronz44',
			'likes': 211,
			'dislikes': 2
		}
	]
	return render_template('education_forum.html', forums=e_forums)

@app.route("/forums/jobs")
def jobs_forum_page():
	j_forums=[
		{
			# 'id': uuid.uuid4().hex,
			'forum_name': 'UOA: Best companies to apply in AZ',
			'date_posted': '2021-05-05 10:10:10',
			'posted_by': 'Ugly_gravy122',
			'likes': 53,
			'dislikes': 0
		},
		{
			# 'id': uuid.uuid4().hex,
			'forum_name': 'Resume tips for applying to oncampus jobs',
			'date_posted': '2021-05-05 10:10:10',
			'posted_by': 'pronz44',
			'likes': 9,
			'dislikes': 2
		}
	]
	return render_template('jobs_forum.html', forums=j_forums)

@app.route("/forums/housing")
def housing_forum_page():
	h_forums=[
		{
			# 'id': uuid.uuid4().hex,
			'forum_name': 'Best apartments near stanford',
			'date_posted': '2021-05-05 10:10:10',
			'posted_by': 'stagger24',
			'likes': 1,
			'dislikes': 2
		},
		{
			# 'id': uuid.uuid4().hex,
			'forum_name': 'ASU: comparing on campus housing.',
			'date_posted': '2021-05-05 10:10:10',
			'posted_by': 'iyv',
			'likes': 5,
			'dislikes': 2
		}
	]
	return render_template('housing_forum.html', forums=h_forums)

@app.route("/forums/flights")
def flights_forum_page():
	f_forums=[
		{
			# 'id': uuid.uuid4().hex,
			'forum_name': 'Reliable airlines we can use in COVID times thread',
			'date_posted': '2021-05-05 10:10:10',
			'posted_by': 'flier34',
			'likes': 77,
			'dislikes': 4
		}
	]
	return render_template('flights_forum.html', forums=f_forums)

@app.route("/forums/vocabularychanges")
def vocabularychanges_forum_page():
	v_forums=[
		{
			# 'id': uuid.uuid4().hex,
			'forum_name': 'Hello',
			'date_posted': '2021-05-05 10:10:10',
			'posted_by': 'ssniper',
			'likes': 666,
			'dislikes': 2
		},
		{
			# 'id': uuid.uuid4().hex,
			'forum_name': 'What is being tall?',
			'date_posted': '2021-05-05 10:10:10',
			'posted_by': 'weee2',
			'likes': 2,
			'dislikes': 2
		}
	]
	return render_template('vocabulary_forum.html', forums=v_forums)

@app.route("/forums/moneymanagement")
def moneymanagement_forum_page():
	m_forums=[
		{
			# 'id': uuid.uuid4().hex,
			'forum_name': 'Minimum amount of cash I can travel with to USA',
			'date_posted': '2021-05-05 10:10:10',
			'posted_by': 'janhu',
			'likes': 64,
			'dislikes': 3
		}
	]
	return render_template('money_forum.html', forums=m_forums)

@app.route("/forums/helpfulwebsites")
def helpfulwebsites_forum_page():
	he_forums=[
		{
			# 'id': uuid.uuid4().hex,
			'forum_name': 'libgen is an awesome site for textbooks. Here are some more',
			'date_posted': '2021-05-05 10:10:10',
			'posted_by': 'wequto',
			'likes': 244,
			'dislikes': 2
		}
	]
	return render_template('websites_forum.html', forums=he_forums)

@app.route("/logout")
def logout_page():
	logout_user()
	return redirect(url_for('home_page'))

# saves image uploaded by user on the account page
def save_image(form_image):
	fname = secrets.token_hex(8)
	_, ext = os.path.splitext(form_image.filename)
	final_name = fname + ext
	image_path = os.path.join(app.root_path, 'static/profile_pics', final_name)
	# reduce the size of big image files uploaded by users
	output_size = (125,125)
	reduced_image = Image.open(form_image)
	reduced_image.thumbnail(output_size)
	reduced_image.save(image_path)
	return final_name

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account_page():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		if form.image.data:
			saved_image = save_image(form.image.data)
			current_user.image_file=saved_image
		current_user.username=form.username.data
		current_user.email = form.email.data
		current_user.university = form.university.data
		db.session.commit()
		flash(f'Journou account info has been updated', 'success mt-3')
		return redirect(url_for('account_page'))
	elif request.method == 'GET':
		form.username.data=current_user.username
		form.email.data=current_user.email
		form.university.data=current_user.university
	image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
	return render_template('account.html', image_file=image_file, form=form)
