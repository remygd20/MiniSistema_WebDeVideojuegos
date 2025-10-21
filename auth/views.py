from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from models import db, User
from . import auth_bp
from .forms import LoginForm, RegistrationForm

# Usamos @auth_bp.route en lugar de @app.route
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('juegos')) # juegos no está en el blueprint
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.verify_password(form.password.data):
            flash('Usuario o contraseña inválidos', 'error')
            return redirect(url_for('auth.login')) # auth.login SÍ está
        
        login_user(user, remember=form.remember_me.data)
        flash('Has iniciado sesión exitosamente.', 'message')
        next_page = request.args.get('next')
        return redirect(next_page or url_for('juegos'))

    # Apuntamos a la nueva ruta de la plantilla
    return render_template('auth/login.html', form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión.', 'message')
    return redirect(url_for('auth.login'))


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('juegos'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('¡Felicidades, te has registrado exitosamente! Ahora puedes iniciar sesión.', 'message')
        return redirect(url_for('auth.login'))

    # Apuntamos a la nueva ruta de la plantilla
    return render_template('auth/register.html', form=form)