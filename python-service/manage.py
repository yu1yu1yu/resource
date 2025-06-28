#!/usr/bin/env python3
"""
数据库管理脚本
"""
import os
from flask.cli import FlaskGroup
from app import create_app
from app.extensions import db
from app.models import User

app = create_app()
cli = FlaskGroup(app)


@cli.command("init-db")
def init_db():
    """初始化数据库"""
    db.create_all()
    print("Database initialized!")


@cli.command("create-admin")
def create_admin():
    """创建管理员用户"""
    username = input("Enter admin username: ")
    email = input("Enter admin email: ")
    password = input("Enter admin password: ")
    
    admin = User(
        username=username,
        email=email,
        password=password,
        is_admin=True
    )
    admin.save()
    print(f"Admin user '{username}' created successfully!")


@cli.command("create-user")
def create_user():
    """创建普通用户"""
    username = input("Enter username: ")
    email = input("Enter email: ")
    password = input("Enter password: ")
    
    user = User(
        username=username,
        email=email,
        password=password
    )
    user.save()
    print(f"User '{username}' created successfully!")


if __name__ == '__main__':
    cli() 