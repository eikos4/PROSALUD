# app/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms.widgets import TimeInput


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



from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, TextAreaField, SelectField, TimeField, SubmitField
from wtforms.validators import DataRequired

# Crear o editar servicio
class ServiceForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired()])
    description = TextAreaField('Descripción')
    price = FloatField('Precio', validators=[DataRequired()])
    submit = SubmitField('Guardar')

# Configurar disponibilidad
class AvailabilityForm(FlaskForm):
    weekday = SelectField('Día', choices=[
        ('Monday', 'Lunes'),
        ('Tuesday', 'Martes'),
        ('Wednesday', 'Miércoles'),
        ('Thursday', 'Jueves'),
        ('Friday', 'Viernes'),
        ('Saturday', 'Sábado'),
        ('Sunday', 'Domingo'),
    ])
    start_time = TimeField('Hora de inicio', widget=TimeInput(), format='%H:%M')
    end_time = TimeField('Hora de término', widget=TimeInput(), format='%H:%M')
    submit = SubmitField('Agregar')

# Responder solicitud
class ResponseRequestForm(FlaskForm):
    status = SelectField('Estado', choices=[('accepted','Aceptar'),('rejected','Rechazar')], validators=[DataRequired()])
    submit = SubmitField('Enviar')


from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Optional, Length

class ClientProfileForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Nueva contraseña', validators=[Optional(), Length(min=6)])
    submit = SubmitField('Guardar cambios')




class RequestServiceForm(FlaskForm):
    message = TextAreaField('Mensaje para el profesional', validators=[DataRequired(), Length(max=500)])
    submit = SubmitField('Enviar solicitud')