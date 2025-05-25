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


from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField, FileField, URLField, TelField
from wtforms.validators import DataRequired, Length, Optional, Email, URL, Regexp

class ProfileForm(FlaskForm):
    full_name = StringField('Nombre Completo', validators=[DataRequired(), Length(max=100)])
    email = StringField('Correo Electrónico', validators=[DataRequired(), Email(), Length(max=150)])
    phone = TelField('Teléfono', validators=[Optional(), Regexp(r'^\+?\d{8,15}$', message='Número inválido.')])
    category = SelectField('Categoría', choices=[
        ('gasfiteria', 'Gasfitería'),
        ('electrico', 'Eléctrico'),
        ('gastronomia', 'Gastronomía'),
        ('paseo_mascotas', 'Paseo de Mascotas'),
        ('maestro', 'Maestro general'),
        ('profesor', 'Profesor particular'),
        ('salud', 'Salud y Bienestar'),
        ('tecnologia', 'Tecnología y Soporte'),
        # Añade más categorías personalizadas
    ], validators=[DataRequired()])
    subcategory = StringField('Especialidad / Subcategoría', validators=[Optional(), Length(max=60)])
    description = TextAreaField('Descripción profesional', validators=[DataRequired(), Length(max=500)])
    experience = TextAreaField('Experiencia / Educación', validators=[Optional(), Length(max=500)])
    location = StringField('Región / Ciudad', validators=[Optional(), Length(max=80)])
    website = URLField('Sitio web o LinkedIn', validators=[Optional(), URL(), Length(max=200)])
    profile_image = FileField('Foto de perfil (opcional)')
    submit = SubmitField('Guardar perfil')




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