from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    StringField, PasswordField, BooleanField, TextAreaField,
    SelectField, DecimalField, TelField, URLField, SubmitField, TimeField
)
from wtforms.validators import (
    DataRequired, Email, EqualTo, Length, Optional,
    NumberRange, Regexp, URL
)
from wtforms.widgets import TimeInput

# Lista de categorías de servicio para IndepWork
SERVICE_CATEGORIES = [
    ('gasfiteria', 'Gasfitería'),
    ('electrico', 'Eléctrico'),
    ('gastronomia', 'Gastronomía'),
    ('paseo_mascotas', 'Paseo de Mascotas'),
    ('maestro', 'Maestro general'),
    ('profesor', 'Profesor particular'),
    ('salud', 'Salud y Bienestar'),
    ('tecnologia', 'Tecnología y Soporte'),
    ('carpinteria', 'Carpintería'),
    ('jardineria', 'Jardinería'),
    ('limpieza', 'Limpieza domiciliaria'),
    ('mudanza', 'Mudanza y Transporte'),
    ('diseno_grafico', 'Diseño Gráfico'),
    ('marketing_digital', 'Marketing Digital'),
    ('contabilidad', 'Contabilidad'),
    ('asesoria_legal', 'Asesoría Legal'),
    ('fotografia', 'Fotografía'),
    ('masajes', 'Masajes Terapéuticos'),
    ('estetica', 'Estética y Belleza'),
    ('eventos', 'Organización de Eventos'),
    ('idiomas', 'Clases de Idiomas'),
    ('programacion', 'Desarrollo de Software'),
    ('diseno_web', 'Diseño Web'),
    ('copywriting', 'Redacción y Copywriting'),
    ('video', 'Producción de Video'),
    ('audio', 'Producción de Audio'),
    ('ilustracion', 'Ilustración'),
    ('voz_acting', 'Locución y Voice-Over'),
    ('decoracion', 'Decoración de Interiores'),
    ('seguridad', 'Seguridad y Vigilancia'),
    ('construccion', 'Construcción'),
    ('pintura', 'Pintura y Acabados'),
    ('plomeria', 'Plomería'),
    ('reparaciones', 'Reparaciones y Mantenimiento'),
]

class LoginForm(FlaskForm):
    email = StringField('Correo', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember_me = BooleanField('Recuérdame')
    submit = SubmitField('Iniciar sesión')

class RegisterForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired(), Length(1, 64)])
    email = StringField('Correo', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Contraseña', validators=[
        DataRequired(),
        Length(min=6),
        EqualTo('password2', message='Las contraseñas deben coincidir')
    ])
    password2 = PasswordField('Repite la contraseña', validators=[DataRequired()])
    role = SelectField('Tipo de cuenta', choices=[('client','Cliente'),('professional','Profesional')], validators=[DataRequired()])
    submit = SubmitField('Registrarse')

class UpgradeAccountForm(FlaskForm):
    submit = SubmitField('Cambiar a profesional')

class MessageForm(FlaskForm):
    subject = StringField('Asunto', validators=[Optional(), Length(max=100)])
    body = TextAreaField('Mensaje', validators=[DataRequired(), Length(max=1000)])
    submit = SubmitField('Enviar')

class ProfileForm(FlaskForm):
    full_name      = StringField('Nombre Completo', validators=[DataRequired(), Length(max=100)])
    email          = StringField('Correo Electrónico', validators=[DataRequired(), Email(), Length(max=150)])
    phone          = TelField('Teléfono', validators=[Optional(), Regexp(r'^\+?\d{8,15}$', message='Número inválido.')])
    category       = SelectField('Categoría', choices=SERVICE_CATEGORIES, validators=[DataRequired()])
    subcategory    = StringField('Especialidad / Subcategoría', validators=[Optional(), Length(max=60)])
    description    = TextAreaField('Descripción profesional', validators=[DataRequired(), Length(max=500)])
    experience     = TextAreaField('Experiencia / Educación', validators=[Optional(), Length(max=500)])
    location       = StringField('Región / Ciudad', validators=[Optional(), Length(max=80)])
    website        = URLField('Sitio web o LinkedIn', validators=[Optional(), URL(), Length(max=200)])
    profile_image  = FileField('Foto de perfil (opcional)', validators=[FileAllowed(['jpg','jpeg','png'], 'Solo se permiten imágenes JPG o PNG')])
    submit         = SubmitField('Guardar perfil')

class ServiceForm(FlaskForm):
    title       = StringField('Nombre del servicio', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Descripción', validators=[DataRequired(), Length(max=500)])
    price       = DecimalField('Precio (CLP)', validators=[DataRequired(), NumberRange(min=0)])
    submit      = SubmitField('Guardar servicio')

class AvailabilityForm(FlaskForm):
    weekday    = SelectField('Día', choices=[
        ('Monday','Lunes'),('Tuesday','Martes'),('Wednesday','Miércoles'),
        ('Thursday','Jueves'),('Friday','Viernes'),('Saturday','Sábado'),('Sunday','Domingo')
    ])
    start_time = TimeField('Hora de inicio', widget=TimeInput(), format='%H:%M')
    end_time   = TimeField('Hora de término', widget=TimeInput(), format='%H:%M')
    submit     = SubmitField('Agregar')

class RequestServiceForm(FlaskForm):
    message = TextAreaField('Mensaje para el profesional', validators=[DataRequired(), Length(max=500)])
    submit  = SubmitField('Enviar solicitud')

class EvaluationForm(FlaskForm):
    rating  = DecimalField('Puntaje', validators=[DataRequired(), NumberRange(min=1, max=5)])
    comment = TextAreaField('Comentario', validators=[DataRequired(), Length(max=1000)])
    submit  = SubmitField('Enviar reseña')

class ContactForm(FlaskForm):
    nombre  = StringField('Nombre', validators=[DataRequired(), Length(max=100)])
    email   = StringField('Correo electrónico', validators=[DataRequired(), Email(), Length(max=150)])
    mensaje = TextAreaField('Mensaje', validators=[DataRequired(), Length(max=1000)])
    submit  = SubmitField('Enviar')
