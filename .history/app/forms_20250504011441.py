# app/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class LoginForm(FlaskForm):
    email = StringField('Correo', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember_me = BooleanField('Recuérdame')
    submit = SubmitField('Iniciar sesión')

# app/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegisterForm(FlaskForm):
    username = StringField(
        'Nombre de usuario',
        validators=[DataRequired(), Length(1, 64)]
    )
    email = StringField(
        'Correo',
        validators=[DataRequired(), Email(), Length(max=120)]
    )
    password = PasswordField(
        'Contraseña',
        validators=[
            DataRequired(),
            Length(min=6),
            EqualTo('password2', message='Las contraseñas deben coincidir')
        ]
    )
    password2 = PasswordField(
        'Repite la contraseña',
        validators=[DataRequired()]
    )
    role = SelectField(
        'Tipo de cuenta',
        choices=[
            ('client', 'Cliente'),
            ('professional', 'Profesional')
        ],
        validators=[DataRequired()]
    )
    submit = SubmitField('Registrarse')


class ProfileForm(FlaskForm):
    # Campos de perfil profesional
    full_name = StringField('Nombre Completo', validators=[DataRequired()])
    category = SelectField('Categoría', choices=[
        ('gasfiteria', 'Gasfitería'),
        ('electrico', 'Eléctrico'),
        ('gastronomia', 'Gastronomía'),
        ('paseo_mascotas', 'Paseo de Mascotas'),
        # añade más categorías según necesites
    ], validators=[DataRequired()])
    description = TextAreaField('Descripción', validators=[DataRequired(), Length(max=500)])
    experience = TextAreaField('Experiencia / Educación', validators=[Length(max=500)])
    submit = SubmitField('Guardar perfil')

class MessageForm(FlaskForm):
    body = TextAreaField('Mensaje', validators=[DataRequired(), Length(max=1000)])
    submit = SubmitField('Enviar')
