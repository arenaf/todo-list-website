from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TimeField, DateField, PasswordField
from wtforms.validators import DataRequired

# Formularios creados con WTForms

# Formulario que añade una nueva tarea
class RegisterForm(FlaskForm):
    name_task = StringField("Tarea", validators=[DataRequired()])
    description_task = StringField("Descripción")
    duration_task = StringField("Duración")
    date_task = DateField("Fecha")
    time_task = TimeField("Hora", format='%H:%M')
    submit = SubmitField("Aceptar")


# Creación de nuevos usuarios
class NewUserForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Contraseña", validators=[DataRequired()])
    name = StringField("Nombre", validators=[DataRequired()])
    submit = SubmitField("Registrar")

# Formulario login para usuarios que ya existen
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")
