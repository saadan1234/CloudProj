# USERACCMGMTSERV/routes.py
from flask import Blueprint, render_template, request, redirect, url_for
from models import db, User
user_bp = Blueprint('user', __name__)

@user_bp.route('/')
def main():
    return render_template('main.html')

@user_bp.route('/user', methods=['POST'])
def create_user():
    data = request.form
    existing_user = User.query.filter_by(username=data['username']).first()
    if existing_user:
        return render_template('signup.html', message='Username already exists. Please choose another.')
    new_user = User(username=data['username'], email=data['email'])
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('user.main'))

@user_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.form
        existing_user = User.query.filter_by(username=data['username']).first()
        if existing_user:
            return render_template('signup.html', message='Username already exists. Please choose another.')
        new_user = User(username=data['username'], email=data['email'])
        new_user.set_password(data['password'])
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('user.main'))
    return render_template('signup.html')

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        user = User.query.filter_by(username=data['username']).first()
        if user and user.check_password(data['password']):
            # You can implement session management or token-based authentication here
            return redirect(url_for('user.main'))
        return render_template('login.html', message='Invalid username or password')
    return render_template('login.html')
