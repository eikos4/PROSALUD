# app/forms.py

from flask_wtf import FlaskForm
from wtforms import DecimalField, StringField, PasswordField, BooleanField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms.widgets import TimeInput


from wtforms import StringField, TextAreaField, DecimalField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange
from wtforms.validators import NumberRange

from flask_wtf.file import FileField, FileAllowed





from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Optional

class ClientProfileForm(FlaskForm):
    full_name = StringField('Nombre Completo', validators=[DataRequired(), Length(max=100)])
    email     = StringField('Correo Electrónico', validators=[DataRequired(), Email(), Length(max=150)])
    phone     = StringField('Teléfono', validators=[Optional(), Length(max=20)])
    location  = StringField('Ciudad / Región', validators=[Optional(), Length(max=80)])
    submit    = SubmitField('Guardar cambios')

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
    profile_image = FileField(
        'Foto de perfil (opcional)',
        validators=[
            FileAllowed(['jpg', 'jpeg', 'png'], 'Solo se permiten imágenes JPG o PNG')
        ]
    )
    submit = SubmitField('Guardar perfil')

class MessageForm(FlaskForm):
    subject = StringField('Asunto', validators=[Optional(), Length(max=100)])
    body = TextAreaField('Mensaje', validators=[DataRequired(), Length(max=1000)])
    submit = SubmitField('Enviar')



from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, TextAreaField, SelectField, TimeField, SubmitField
from wtforms.validators import DataRequired

# Crear o editar servicio
class ServiceForm(FlaskForm):
    title = StringField('Nombre del servicio', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Descripción', validators=[DataRequired(), Length(max=500)])
    price = DecimalField('Precio (CLP)', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Guardar servicio')

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

from flask_wtf import FlaskForm
from wtforms import TextAreaField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class EvaluationForm(FlaskForm):
    rating = IntegerField('Puntaje', validators=[DataRequired(), NumberRange(min=1, max=5)])
    comment = TextAreaField('Comentario', validators=[DataRequired()])
    submit = SubmitField('Enviar reseña')


class ContactForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    email = StringField('Correo electrónico', validators=[DataRequired(), Email()])
    mensaje = TextAreaField('Mensaje', validators=[DataRequired()])

from flask_wtf import FlaskForm
from wtforms import SubmitField

class UpgradeAccountForm(FlaskForm):
    submit = SubmitField('Cambiar a profesional')

