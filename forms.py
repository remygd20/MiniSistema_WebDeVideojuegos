from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from models import User

class LoginForm(FlaskForm):
    """Formulario de inicio de sesión."""
    username = StringField('Usuario', validators=[DataRequired(message="El usuario es requerido.")])
    password = PasswordField('Contraseña', validators=[DataRequired(message="La contraseña es requerida.")])
    remember_me = BooleanField('Recuérdame')
    submit = SubmitField('Ingresar')


class RegistrationForm(FlaskForm):
    """Formulario de registro."""
    username = StringField('Usuario', validators=[DataRequired(message="El usuario es requerido.")])
    password = PasswordField('Contraseña', validators=[DataRequired(message="La contraseña es requerida.")])
    password2 = PasswordField(
        'Repetir Contraseña', 
        validators=[DataRequired(), EqualTo('password', message='Las contraseñas deben coincidir.')]
    )
    submit = SubmitField('Registrarse')

    # Validador que asegura que el username no exista
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Este nombre de usuario ya está en uso. Por favor, elige otro.')