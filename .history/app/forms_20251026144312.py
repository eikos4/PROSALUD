# app/forms.py
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    StringField, PasswordField, BooleanField, TextAreaField, SelectField,
    SubmitField, DecimalField, TimeField, IntegerField
)
from wtforms.fields import EmailField, TelField, URLField
from wtforms.validators import (
    DataRequired, Email, EqualTo, Length, Optional, NumberRange, URL, Regexp
)
from wtforms.widgets import TimeInput

# -------------------------------------------------------
# FORMULARIOS DE AUTENTICACIÓN
# -------------------------------------------------------

class LoginForm(FlaskForm):
    email = StringField('Correo', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember_me = BooleanField('Recuérdame')
    submit = SubmitField('Iniciar sesión')


class RegisterForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired(), Length(1, 64)])
    email = StringField('Correo', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField(
        'Contraseña',
        validators=[
            DataRequired(),
            Length(min=6),
            EqualTo('password2', message='Las contraseñas deben coincidir')
        ]
    )
    password2 = PasswordField('Repite la contraseña', validators=[DataRequired()])
    role = SelectField(
        'Tipo de cuenta',
        choices=[
            ('client', 'Cliente'),
            ('professional', 'Profesional')
        ],
        validators=[DataRequired()]
    )
    submit = SubmitField('Registrarse')

# -------------------------------------------------------
# FORMULARIOS DE PERFIL
# -------------------------------------------------------

class ClientProfileForm(FlaskForm):
    username = StringField('Nombre de Usuario', validators=[DataRequired(), Length(max=100)])
    email = StringField('Correo Electrónico', validators=[DataRequired(), Email(), Length(max=150)])
    phone = StringField('Teléfono', validators=[Optional(), Length(max=20)])
    location = StringField('Ciudad / Región', validators=[Optional(), Length(max=80)])
    submit = SubmitField('Guardar cambios')


class ProfileForm(FlaskForm):
    full_name = StringField(
        'Nombre completo',
        validators=[DataRequired(message="Este campo es obligatorio."), Length(max=100)],
        render_kw={"placeholder": "Ej: Antonia Escandón"}
    )
    email = EmailField(
        'Correo electrónico',
        validators=[DataRequired(message="Este campo es obligatorio."), Email(), Length(max=150)],
        render_kw={"placeholder": "correo@ejemplo.com"}
    )
    phone = TelField(
        'Teléfono',
        validators=[Optional(), Regexp(r'^\+?\d{8,15}$', message='Número de teléfono inválido.')],
        render_kw={"placeholder": "+56912345678"}
    )
    category = SelectField(
        'Profesión / Categoría',
        choices=[
            ('', 'Selecciona tu profesión'),
            ('medico', 'Médico(a)'),
            ('enfermeria', 'Enfermería'),
            ('kinesiologia', 'Kinesiología'),
            ('nutricionista', 'Nutricionista'),
            ('psicologia', 'Psicología'),
            ('fonoaudiologia', 'Fonoaudiología'),
            ('tecnologo_medico', 'Tecnólogo Médico'),
            ('odontologia', 'Odontología'),
            ('matroneria', 'Matronería'),
            ('terapia_ocupacional', 'Terapia Ocupacional'),
            ('quimico_farmaceutico', 'Químico Farmacéutico'),
            ('masoterapia', 'Masoterapia'),
            ('estetica', 'Estética y Bienestar'),
        ],
        validators=[DataRequired(message="Selecciona una profesión.")]
    )
    subcategory = StringField(
        'Especialidad o subcategoría',
        validators=[Optional(), Length(max=60)],
        render_kw={"placeholder": "Ej: Medicina interna, Pediatría, Oncología..."}
    )
    description = TextAreaField(
        'Presentación profesional',
        validators=[DataRequired(message="Este campo es obligatorio."), Length(max=500)],
        render_kw={"placeholder": "Describe tus servicios, experiencia y fortalezas."}
    )
    experience = TextAreaField(
        'Experiencia y formación',
        validators=[Optional(), Length(max=500)],
        render_kw={"placeholder": "Ej: 5 años en atención primaria, Diplomado en Diabetes, etc."}
    )
    location = StringField('Ciudad y región', validators=[Optional(), Length(max=80)])
    website = URLField(
        'Sitio web profesional o LinkedIn',
        validators=[Optional(), URL(message="URL inválida."), Length(max=200)],
        render_kw={"placeholder": "https://linkedin.com/in/tu-perfil"}
    )
    profile_image = FileField(
        'Foto de perfil (opcional)',
        validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Solo imágenes JPG o PNG, máximo 2 MB.')],
        render_kw={"accept": ".jpg,.jpeg,.png"}
    )
    certificate_file = FileField(
        'Subir título o certificado (PDF o imagen)',
        validators=[FileAllowed(['pdf', 'jpg', 'jpeg', 'png'], 'Solo PDF o imágenes.')],
        render_kw={"accept": ".pdf,.jpg,.jpeg,.png"}
    )
    submit = SubmitField('Guardar perfil')

# -------------------------------------------------------
# FORMULARIOS DE SERVICIOS Y DISPONIBILIDAD
# -------------------------------------------------------

class ServiceForm(FlaskForm):
    title = StringField('Nombre del servicio', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Descripción', validators=[DataRequired(), Length(max=500)])
    price = DecimalField('Precio (CLP)', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Guardar servicio')


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

# -------------------------------------------------------
# FORMULARIOS DE MENSAJES Y SOLICITUDES
# -------------------------------------------------------

class MessageForm(FlaskForm):
    subject = StringField('Asunto', validators=[Optional(), Length(max=100)])
    body = TextAreaField('Mensaje', validators=[DataRequired(), Length(max=1000)])
    submit = SubmitField('Enviar')


class RequestServiceForm(FlaskForm):
    message = TextAreaField('Mensaje para el profesional', validators=[DataRequired(), Length(max=500)])
    submit = SubmitField('Enviar solicitud')


class ResponseRequestForm(FlaskForm):
    status = SelectField('Estado', choices=[('accepted', 'Aceptar'), ('rejected', 'Rechazar')], validators=[DataRequired()])
    submit = SubmitField('Enviar')

# -------------------------------------------------------
# FORMULARIOS DE EVALUACIONES Y CONTACTO
# -------------------------------------------------------

class EvaluationForm(FlaskForm):
    rating = IntegerField('Puntaje', validators=[DataRequired(), NumberRange(min=1, max=5)])
    comment = TextAreaField('Comentario', validators=[DataRequired()])
    submit = SubmitField('Enviar reseña')


class ContactForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    email = StringField('Correo electrónico', validators=[DataRequired(), Email()])
    mensaje = TextAreaField('Mensaje', validators=[DataRequired()])
    submit = SubmitField('Enviar mensaje')

# -------------------------------------------------------
# OTROS FORMULARIOS (Upgrade / Delete)
# -------------------------------------------------------

class UpgradeAccountForm(FlaskForm):
    submit = SubmitField('Cambiar a profesional')


class DeleteForm(FlaskForm):
    pass  # Solo usado para token CSRF
