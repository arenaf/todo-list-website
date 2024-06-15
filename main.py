from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, ForeignKey


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
    # Relates the users table to the comments
    #"comment_author" refers to the comment_author property in the Comment class.
    ##comments = relationship("Comment", back_populates="comment_author")

class TodoList(db.Model):
    __tablename__ = "todo_list"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name_task: Mapped[str] = mapped_column(String(250), nullable=False)
    description_task: Mapped[str] = mapped_column(String(250), nullable=True)
    duration_task: Mapped[str] = mapped_column(String(250), nullable=True)
    date_task: Mapped[str] = mapped_column(String(250), nullable=True)
    time_task: Mapped[str] = mapped_column(String(250), nullable=True)
    # Relationship between the task and users tables
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="task")
    # Relationship with color
    color_id: Mapped[int] = mapped_column(Integer, ForeignKey("color.id"))
    color = relationship("Color", back_populates="task_color")

class Color(db.Model):
    __tablename__ = "color"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name_color: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    task_color = relationship("TodoList", back_populates="color")

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return db.session.execute(db.select(User).where(User.id == user_id)).scalar()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/head")
def head():
    return render_template("header.html")


if __name__ == '__main__':
    app.run(debug=True)
