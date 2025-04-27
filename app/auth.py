from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, current_user, login_required
from urllib.parse import urlparse
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from flask_mail import Message
from . import db, mail  # Make sure mail is initialized in your __init__.py
from .models import User

auth = Blueprint('auth', __name__)

# Token generation and confirmation functions for email confirmation
def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt='email-confirm-salt')

def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt='email-confirm-salt', max_age=expiration)
    except (SignatureExpired, BadSignature):
        return False
    return email

# Token generation and confirmation functions for password reset
def generate_reset_token(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt='password-reset-salt')

def confirm_reset_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt='password-reset-salt', max_age=expiration)
    except (SignatureExpired, BadSignature):
        return False
    return email

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(password):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        # Enforce email verification
        if not user.email_verified:
            flash('Please verify your email before logging in.')
            return redirect(url_for('auth.login'))
        
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('main.home')
        return redirect(next_page)
    
    return render_template('login.html')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Check if user exists by username or email
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('auth.signup'))
        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('auth.signup'))
        
        # Create new user and set password using your model method
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        
        # Add the new user to the session and flush without committing immediately
        db.session.add(new_user)
        db.session.flush()
        
        # Generate confirmation token and build the confirmation URL
        token = generate_confirmation_token(new_user.email)
        confirm_url = url_for('auth.confirm_email', token=token, _external=True)
        html = render_template('activate.html', confirm_url=confirm_url)
        subject = "Please confirm your email"
        
        # Prepare the confirmation email message
        msg = Message(subject, recipients=[new_user.email], html=html)
        try:
            mail.send(msg)
            db.session.commit()  # Commit only if email sent successfully
        except Exception as e:
            current_app.logger.error("Failed to send confirmation email: %s", e)
            db.session.rollback()  # Roll back so the new user is not stored
            flash('There was an issue sending a confirmation email. Please check your email address and try again.', 'danger')
            return redirect(url_for('auth.signup'))
        
        flash('A confirmation email has been sent. Please check your inbox.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('signup.html')

@auth.route('/confirm/<token>')
def confirm_email(token):
    email = confirm_token(token)
    if not email:
        flash('The confirmation link is invalid or has expired.', 'danger')
        return redirect(url_for('auth.login'))
    
    user = User.query.filter_by(email=email).first_or_404()
    if user.email_verified:
        flash('Account already confirmed. Please login.', 'success')
    else:
        user.email_verified = True
        db.session.add(user)
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('auth.login'))

# Route to request a password reset
@auth.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user:
            token = generate_reset_token(user.email)
            reset_url = url_for('auth.reset_password', token=token, _external=True)
            html = render_template('reset_password_email.html', reset_url=reset_url)
            subject = "Reset Your Password"
            msg = Message(subject, recipients=[user.email], html=html)
            try:
                mail.send(msg)
            except Exception as e:
                current_app.logger.error("Failed to send password reset email: %s", e)
                flash('There was an issue sending a password reset email. Please try again later.', 'danger')
                return redirect(url_for('auth.reset_password_request'))
            flash('A password reset email has been sent. Please check your inbox.', 'success')
        else:
            flash('No account found with that email address.', 'warning')
        return redirect(url_for('auth.login'))
    
    return render_template('reset_password_request.html')

# Route to reset the password using the token
@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    email = confirm_reset_token(token)
    if not email:
        flash('The password reset link is invalid or has expired.', 'danger')
        return redirect(url_for('auth.reset_password_request'))
    
    user = User.query.filter_by(email=email).first_or_404()
    if request.method == 'POST':
        new_password = request.form['password']
        confirm_password = request.form['confirm_password']
        if new_password != confirm_password:
            flash('Passwords do not match. Try again.', 'warning')
            return redirect(url_for('auth.reset_password', token=token))
        
        user.set_password(new_password)
        db.session.commit()
        flash('Your password has been updated. You can now log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('reset_password.html', token=token)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))
