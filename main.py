import sqlite3

from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, ForeignKey, insert

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




# with db.session.connect() as conn:
#     query = ('INSERT INTO Color VALUES (("#F72798"), ("#FF204E"), ("#FFF455"), ("#6420AA"), ("#007F73"), ("#00DFA2"),'
#              '("#0079FF"), ("#247881"), ("#FF5403"), ("#F7FD04"))')
#     conn.execute(query)
#     conn.commit()


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
    date_task: Mapped[str] = mapped_column(String(250), nullable=True)
    time_task: Mapped[str] = mapped_column(String(250), nullable=True)
    color: Mapped[str] = mapped_column(String(250), nullable=True)
    # Relationship between the task and users tables
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="task")


class Color(db.Model):
    __tablename__ = "color"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name_color: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)


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


@app.route("/prueba")
def head():
    return render_template("prueba.html")


@app.route('/colors')
def get_all_colors():
    result = db.session.execute(db.select(Color))
    colors = result.scalars().all()
    return render_template("colors.html", all_colors=colors)


if __name__ == '__main__':
    app.run(debug=True)
