from click import prompt
import click
from flask import Blueprint
from sqlalchemy.exc import IntegrityError

from app.models import db, User, UserData


cli_bp = Blueprint("user", __name__)


@cli_bp.cli.command("add", help="Add a user.")
@click.argument("username")
@click.argument("password")
@click.option("--admin", is_flag=True)
def add_user(username, password, admin):
    try:
        user = User.add_user(username=username, password=password, isAdmin=admin)
        print(f'{"<admin> " if admin else ""}User {user.username} created.')
    except IntegrityError:
        print("用户名已存在：", username)


@cli_bp.cli.command("drop", help="Delete a User.")
@click.argument("username")
def drop_user(username):
    if user := User.query.filter_by(username=username).first():
        if user.validate_password(input(f"请输入用户{username}的密码：")):
            db.session.delete(user)
            db.session.commit()
            print(f"User {username} deleted.")
        else:
            print("密码错误！")
    else:
        print("用户名不存在：", username)
