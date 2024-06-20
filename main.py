import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, ForeignKey, Date, Time, Boolean
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from forms import RegisterForm, NewUserForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')
Bootstrap5(app)

login_manager = LoginManager()
login_manager.init_app(app)


class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URI", 'sqlite:///task.db')
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Creación de tablas
class User(db.Model, UserMixin):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    email: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    # Relaciona la tabla usuario con la tabla de tareas
    task = relationship("TodoList", back_populates="user")


class TodoList(db.Model):
    __tablename__ = "todo_list"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name_task: Mapped[str] = mapped_column(String(250), nullable=False)
    description_task: Mapped[str] = mapped_column(String(250), nullable=True)
    duration_task: Mapped[str] = mapped_column(String(250), nullable=True)
    date_task: Mapped[Date] = mapped_column(Date, nullable=True)
    time_task: Mapped[Time] = mapped_column(Time, nullable=True)
    check_task: Mapped[bool] = mapped_column(Boolean, default=False)
    # Relaciona la tarea con el usuario que la creó
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="task")


with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return db.session.execute(db.select(User).where(User.id == user_id)).scalar()


# --------- Registro de nuevo usuario --------
@app.route('/new-user', methods=["GET", "POST"])
def new_user_register():
    form = NewUserForm()
    if request.method == "POST":
        user = User.query.filter_by(email=request.form["email"]).first()
        if user != None:
            flash("¡Este email ya existe!")
            return redirect(url_for("login"))
        final_pass = generate_password_hash(password=request.form["password"], method="pbkdf2:sha256", salt_length=8)
        new_user = User(
            name=request.form["name"],
            password=final_pass,
            email=request.form["email"]
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("home"))
    return render_template("new_user.html", form=form, current_user=current_user)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


# -------- Login de usuario --------
@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=request.form["email"]).first()
        if user == None:
            flash("¡No hay ningún usuario registrado con ese email!")
            return redirect(url_for("login"))
        if check_password_hash(user.password, request.form["password"]):
            login_user(user)
            return redirect(url_for("home"))
        else:
            flash("Password incorrecta. Inténtalo de nuevo")
            return redirect(url_for("login"))
    return render_template("login.html", form=form, current_user=current_user)


# -------- Función decorador --------
# Solo los usuarios logueados pueden ver sus tareas
def user_logged(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("Debes loguearte para ver y crear tareas.")
            return redirect(url_for("login"))
        return function(*args, **kwargs)
    return decorated_function


# -------- Vista en formato tabla --------
@app.route("/")
def home():
    if current_user.is_authenticated:
        result = db.session.execute(db.select(TodoList).where(TodoList.check_task == False).where(TodoList.user_id == current_user.id).order_by(TodoList.date_task))
        todo_list = result.scalars().all()
        return render_template("index.html", todo_list=todo_list, current_user=current_user)
    return render_template("index.html", current_user=current_user)


@app.route("/all_task")
@user_logged
def all_task():
    result = db.session.execute(db.select(TodoList).where(TodoList.user_id == current_user.id).order_by(TodoList.date_task))
    todo_list = result.scalars().all()
    return render_template("index.html", todo_list=todo_list)


@app.route("/only_complete")
@user_logged
def only_complete():
    result = db.session.execute(db.select(TodoList).where(TodoList.check_task == True).where(TodoList.user_id == current_user.id).order_by(TodoList.date_task))
    todo_list = result.scalars().all()
    return render_template("index.html", todo_list=todo_list)


# -------- Vista en formato tarjeta --------
@app.route("/pending-task")
@user_logged
def pending_task():
    result = db.session.execute(db.select(TodoList).where(TodoList.check_task == False).where(TodoList.user_id == current_user.id).order_by(TodoList.date_task))
    todo_list = result.scalars().all()
    return render_template("status_task.html", todo_list=todo_list)


@app.route("/complete-task")
@user_logged
def complete_task():
    result = db.session.execute(db.select(TodoList).where(TodoList.check_task == True).where(TodoList.user_id == current_user.id).order_by(TodoList.date_task))
    todo_list = result.scalars().all()
    return render_template("status_task.html", todo_list=todo_list)


@app.route("/show-all-task")
@user_logged
def show_all_task():
    result = db.session.execute(db.select(TodoList).where(TodoList.user_id == current_user.id).order_by(TodoList.date_task))
    todo_list = result.scalars().all()
    return render_template("status_task.html", todo_list=todo_list)


# -------- Añade una nueva tarea --------
@app.route("/register", methods=["GET", "POST"])
@user_logged
def register():
    form = RegisterForm()
    if request.method == "POST":
        new_task = TodoList(
            name_task=form.name_task.data,
            description_task=form.description_task.data,
            duration_task=form.duration_task.data,
            date_task=form.date_task.data,
            time_task=form.time_task.data,
            check_task=False,
            user_id=current_user.id
        )
        db.session.add(new_task)
        db.session.commit()

        return redirect(url_for("home"))
    return render_template("register.html", form=form)


# -------- Modifica una nueva tarea ya existente --------
@app.route("/edit-task/<int:task>", methods=["GET", "POST"])
@user_logged
def edit_task(task):
    task_to_edit = db.get_or_404(TodoList, task)
    edit_task = RegisterForm(
        name_task=task_to_edit.name_task,
        description_task=task_to_edit.description_task,
        duration_task=task_to_edit.duration_task,
        date_task=task_to_edit.date_task,
        time_task=task_to_edit.time_task,
    )
    if edit_task.validate_on_submit():
        task_to_edit.name_task = edit_task.name_task.data
        task_to_edit.description_task = edit_task.description_task.data
        task_to_edit.duration_task = edit_task.duration_task.data
        task_to_edit.date_task = edit_task.date_task.data
        task_to_edit.time_task = edit_task.time_task.data
        db.session.commit()
        return redirect(url_for("home", task=task_to_edit.id))
    return render_template("register.html", form=edit_task, edit=True)


# -------- Actualiza una tarea --------
@app.route("/update/<int:task>", methods=["GET", "POST"])
@user_logged
def update(task):
    update_state = db.get_or_404(TodoList, task)
    update_state.check_task = True
    db.session.commit()
    return redirect(url_for("home"))


# -------- Elimina una tarea --------
@app.route("/delete/<int:task>")
@user_logged
def delete_task(task):
    task_to_delete = db.get_or_404(TodoList, task)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
