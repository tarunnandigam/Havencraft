from flask import render_template, request, session, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from app import app, db
from models import User
from werkzeug.security import check_password_hash

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = bool(request.form.get('remember'))
        
        if not email or not password:
            flash('Please fill in all fields', 'error')
            return render_template('auth/login.html')
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user, remember=remember)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            flash(f'Welcome back, {user.get_full_name()}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password', 'error')
    
    return render_template('auth/login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        phone = request.form.get('phone')
        
        # Validation
        if not all([username, email, password, confirm_password]):
            flash('Please fill in all required fields', 'error')
            return render_template('auth/register.html')
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('auth/register.html')
        
        if password and len(password) < 6:
            flash('Password must be at least 6 characters long', 'error')
            return render_template('auth/register.html')
        
        # Check if user already exists
        if User.query.filter_by(email=email).first():
            flash('Email address already registered', 'error')
            return render_template('auth/register.html')
        
        if User.query.filter_by(username=username).first():
            flash('Username already taken', 'error')
            return render_template('auth/register.html')
        
        # Create new user
        user = User()
        user.username = username
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.phone = phone
        user.set_password(password)
        
        try:
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            app.logger.error(f'Error during registration: {e}')
            flash('An error occurred during registration. Please try again.', 'error')
    
    return render_template('auth/register.html')

@app.route('/logout')
@login_required
def logout():
    username = current_user.get_full_name()
    logout_user()
    flash(f'Goodbye, {username}!', 'info')
    return redirect(url_for('index'))

@app.route('/profile')
@login_required
def profile():
    return render_template('auth/profile.html', user=current_user)

@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        current_user.first_name = request.form.get('first_name')
        current_user.last_name = request.form.get('last_name')
        current_user.phone = request.form.get('phone')
        
        # Handle password change
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        if new_password:
            if not current_password or not current_user.check_password(current_password):
                flash('Current password is incorrect', 'error')
                return render_template('auth/edit_profile.html', user=current_user)
            
            if new_password != confirm_password:
                flash('New passwords do not match', 'error')
                return render_template('auth/edit_profile.html', user=current_user)
            
            if len(new_password) < 6:
                flash('Password must be at least 6 characters long', 'error')
                return render_template('auth/edit_profile.html', user=current_user)
            
            current_user.set_password(new_password)
        
        try:
            db.session.commit()
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('user_profile'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating your profile.', 'error')
    
    # Handle GET request
    return render_template('auth/edit_profile.html', user=current_user)