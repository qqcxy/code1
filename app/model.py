#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from __init__ import *
from flask import current_app
# from flask.ext.login import AnonymousUserMixin, login_manager
from flask.ext.login import AnonymousUserMixin, login_manager
from flask_security import RoleMixin, UserMixin

# Define models
from app import db


class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    # 只有一个角色需要设置为true，用户注册时，其角色会被设置成默认
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    user = db.relationship('User', backref='role', lazy='dynamic')

    # roles_users = db.Table('roles_users',
    #                        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    #                        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))
    #
    #
    # class Role(db.Model, RoleMixin):
    #     id = db.Column(db.Integer(), primary_key=True)
    #     name = db.Column(db.String(80), unique=True)
    #     description = db.Column(db.String(255))
    #
    #
    # class User(db.Model, UserMixin):
    #     id = db.Column(db.Integer, primary_key=True)
    #     email = db.Column(db.String(255), unique=True)
    #     password = db.Column(db.String(255))
    #     active = db.Column(db.Boolean())
    #     confirmed_at = db.Column(db.DateTime())
    #     roles = db.relationship('Role', secondary=roles_users,
    #                             backref=db.backref('users', lazy='dynamic'))
    #     envs = db.relationship('Env', backref=db.backref('user'))
    #
    #
    # class Env(db.Model):
    #     def __init__(self, name, user_id):
    #         self.name = name
    #         self.user_id = user_id
    #
    #     id = db.Column(db.Integer, primary_key=True)
    #     name = db.Column(db.String(255), unique=True)
    #     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.FOLLOW | Permission.COMMENT | Permission.WRITE_ARTICLES, True),
            'Moderator': (
                Permission.FOLLOW | Permission.COMMENT | Permission.WRITE_ARTICLES | Permission.MODERATE_COMMENTS,
                False),
            'Administrator': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            print roles[r][0]
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()


# Use
# python manage shell

# Role.insert_roles()


class User(UserMixin, db.Model):
    # 与运算验证权限

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASKY_ADMIN]']:
                self.role = Role.filter_by(Permission=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    # 检查用户是否有指定的权限
    def can(self, permissions):
        return self.role is not None and (self.role.permissions & permissions == permissions)

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)


# 出于一致性考虑，这里还定义了AnonymousUser类，继承Flask-Login的AnonymousUserMixin类
class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administator(self):
        return False


# 将其设为用户未登录时的current_user值， 这样程序不用先检查用户是否已经登入
login_manager.anonymous_user = AnonymousUser
