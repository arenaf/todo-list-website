from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, ForeignKey, Date, Time, Boolean

from forms import RegisterForm
# COLOR = ["#F72798", "#FF204E", "#FFF455", "#6420AA", "#007F73", "#00DFA2", "#0079FF", "#247881", "#FF5403", "#F7FD04"]

app = Flask(__name__)
app.config['SECRET_KEY'] = '1N-43lNWmnqwi893'
Bootstrap5(app)

login_manager = LoginManager()
login_manager.init_app(app)

class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Creación de tablas
class User(db.Model, UserMixin):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    email: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    # Relates the users table to the blogs
    task = relationship("TodoList", back_populates="user")


class TodoList(db.Model):
    __tablename__ = "todo_list"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name_task: Mapped[str] = mapped_column(String(250), nullable=False)
    description_task: Mapped[str] = mapped_column(String(250), nullable=True)
    duration_task: Mapped[str] = mapped_column(String(250), nullable=True)
    # date_task: Mapped[str] = mapped_column(String(250), nullable=True)
    date_task: Mapped[Date] = mapped_column(Date, nullable=True)
    # time_task: Mapped[str] = mapped_column(String(250), nullable=True)
    time_task: Mapped[Time] = mapped_column(Time, nullable=True)
    color: Mapped[str] = mapped_column(String(250), nullable=True)
    check_task: Mapped[str] = mapped_column(String(4), default="...")

    # Relationship between the task and users tables
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="task")


# class Color(db.Model):
#     __tablename__ = "color"
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     name_color: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)


with app.app_context():
    db.create_all()


# with app.app_context():
#     objects = [Color(name_color="#F72798"), Color(name_color="#FF204E"), Color(name_color="#FFF455"),
#                Color(name_color="#6420AA"), Color(name_color="#007F73"), Color(name_color="#00DFA2"),
#                Color(name_color="#0079FF"), Color(name_color="#247881"), Color(name_color="#FF5403"),
#                Color(name_color="#F7FD04")]
#     db.session.add_all(objects)
#     db.session.commit()

# with app.app_context():
#     new_user = User(name="Pepe", email="pepe@mail.com", password="1234")
#     db.session.add(new_user)
#     db.session.commit()
#
# with app.app_context():
#     new_task = TodoList(name_task="Cena", date_task="15/06/2024", time_task="21:30", color="#FF5403", user_id=1)
#     db.session.add(new_task)
#     db.session.commit()
#
# with app.app_context():
#     new_task = TodoList(name_task="Yoga", duration_task="30", color="#0079FF", user_id=1)
#     db.session.add(new_task)
#     db.session.commit()

# with app.app_context():
#     new_task = TodoList(name_task='Cumpleaños', description_task='Comida con amigos', duration_task='4 horas',
#                           date_task='21/06/2024', time_task='14:00', color='#6420AA', user_id=1)
#     db.session.add(new_task)
#     db.session.commit()


@login_manager.user_loader
def load_user(user_id):
    return db.session.execute(db.select(User).where(User.id == user_id)).scalar()


@app.route("/")
def home():
    result = db.session.execute(db.select(TodoList))
    todo_list = result.scalars().all()
    return render_template("index.html", todo_list=todo_list)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if request.method == "POST":
        new_task = TodoList(
            name_task=form.name_task.data,
            description_task=form.description_task.data,
            duration_task=form.duration_task.data,
            date_task=form.date_task.data,
            time_task=form.time_task.data,
            color=form.color.data,
            check_task=form.check_task.data,
            user_id=1
        )
        db.session.add(new_task)
        db.session.commit()

        return redirect(url_for("home"))
    return render_template("register.html", form=form)


@app.route("/edit-task/<int:task>", methods=["GET", "POST"])
def edit_task(task):
    task_to_edit = db.get_or_404(TodoList, task)
    edit_task = RegisterForm(
        name_task=task_to_edit.name_task,
        description_task=task_to_edit.description_task,
        duration_task=task_to_edit.duration_task,
        date_task=task_to_edit.date_task,
        time_task=task_to_edit.time_task,
        color=task_to_edit.color,
        check_task=task_to_edit.check_task,
    )
    if edit_task.validate_on_submit():
        task_to_edit.name_task = edit_task.name_task.data
        task_to_edit.description_task = edit_task.description_task.data
        task_to_edit.duration_task = edit_task.duration_task.data
        task_to_edit.date_task = edit_task.date_task.data
        task_to_edit.time_task = edit_task.time_task.data
        task_to_edit.color = edit_task.color.data
        task_to_edit.check_task = edit_task.check_task.data
        db.session.commit()
        return redirect(url_for("home", task=task_to_edit.id))
    return render_template("register.html", form=edit_task, edit=True)


@app.route("/delete/<int:task>")
def delete_task(task):
    task_to_delete = db.get_or_404(TodoList, task)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/prueba")
def head():
    return render_template("prueba.html")


# @app.route('/colors')
# def get_all_colors():
#     result = db.session.execute(db.select(Color))
#     colors = result.scalars().all()
#     return render_template("colors.html", all_colors=colors)


if __name__ == '__main__':
    app.run(debug=True)



# TODO 1: formatear fecha y hora
# TODO 2: seleccionar un color
# TODO 3: error update si no se introduce fecha y hora
