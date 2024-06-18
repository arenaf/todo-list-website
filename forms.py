from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TimeField, DateField
from wtforms.validators import DataRequired

COLOR = ["#F72798", "#FF204E", "#FFF455", "#6420AA", "#007F73", "#00DFA2", "#0079FF", "#247881", "#FF5403", "#F7FD04"]
CHECK = ["...", "✓", "✘",]


# WTForm: se crea el formulario para añadir nueva tarea
class RegisterForm(FlaskForm):
    name_task = StringField("Tarea", validators=[DataRequired()])
    description_task = StringField("Descripción")
    duration_task = StringField("Duración")
    date_task = DateField("Fecha")
    time_task = TimeField("Hora", format='%H:%M')
    color = SelectField("Etiqueta", choices=COLOR)
    check_task = SelectField("Etiqueta", choices=CHECK)
    submit = SubmitField("Aceptar")


# # Create a RegisterForm to register new users
# class RegisterForm(FlaskForm):
#     email = StringField("Email", validators=[DataRequired()])
#     password = PasswordField("Password", validators=[DataRequired()])
#     name = StringField("Name", validators=[DataRequired()])
#     submit = SubmitField("New user")
#
# # Create a LoginForm to login existing users
# class LoginForm(FlaskForm):
#     email = StringField("Email", validators=[DataRequired()])
#     password = PasswordField("Password", validators=[DataRequired()])
#     submit = SubmitField("Login")