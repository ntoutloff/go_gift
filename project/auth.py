from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from sqlalchemy import select
from werkzeug.security import generate_password_hash, check_password_hash
from random import randint
import smtplib
from email.message import EmailMessage

from .models import User
from . import db

auth = Blueprint('auth', __name__)

def generate_code() -> str:
    return str(randint(100000, 999999))

def send_confirmation_email(user_email: str, code: str):
    email_sender = 'gogiftmailer@gmail.com'
    email_password = 'dzxu pxbj czgv osmb' 
    email_receiver = user_email

    subject = 'GoGift! email confirmation code.'
    body = f'Your code: {code}'

    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = email_sender
    msg['To'] = email_receiver

    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(email_sender, email_password)
            server.send_message(msg)
        print(f"confirmation email for {user_email} sent successfully!")
    except Exception as e:
        print(f"Error sending email for {user_email}: {e}")


@auth.get('/send_email/<int:id>')
def send_email(id: int):
    user = db.session.get(User, id)
    if user:
        user.confirmation_code = generate_code()
        send_confirmation_email(user.email, user.confirmation_code)
        db.session.commit()
        return redirect(url_for('auth.confirm_email', id=id))
    else:
        return redirect(url_for('confirmation_error'))

@auth.route('/confirm_email/<int:id>', methods=['GET', 'POST'])
def confirm_email(id: int):
    print('hello')
    user = db.session.get(User, id)
    if request.method == 'POST':
        code = request.form.get('code')
        
        print(code)
        print(user.confirmation_code)
        print(user and user.confirmation_code == code)
        if user and user.confirmation_code == code:
            user.confirmed = True
            db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            return render_template('confirm_email.html', user=user, error="Invalid confirmation code.")
    else:
        print('huh?')
        return render_template('confirm_email.html', user=user)


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()
    
    if not user:
        flash(f'user {email} not found.')
        return redirect(url_for('auth.login'))
    if not user.confirmed:
        flash('You must confirm email before logging in!')
        return redirect(url_for('auth.confirm_email', id=user.id))
    if not check_password_hash(user.password, password):
        flash('password hash failed.')
        return redirect(url_for('auth.login'))
    
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))


@auth.get('/signup')
def signup():
    return render_template('signup.html')


@auth.post('/signup')
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if user:
        if user.confirmed:
            flash('Email address already exists')
            return redirect(url_for('auth.signup'))
        else:
            db.session.delete(user)
            db.session.commit()

    new_user = User(
        email=email,
        name=name,
        password=generate_password_hash(password),
        confirmation_code=generate_code(),
        confirmed=False
    )
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('auth.send_email', id=new_user.id))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))