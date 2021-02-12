# coding:utf8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pymysql

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:root@localhost:3306/movie_project?charset=utf8'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)


# 会员表
class User(db.Model):

    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)                    # id
    name = db.Column(db.String(100), unique=True)                   # 昵称
    pwd = db.Column(db.String(100))                                 # 密码
    email = db.Column(db.String(100), unique=True)                  # 邮箱
    info = db.Column(db.String(100))                   # 简介
    phone = db.Column(db.String(11), unique=True)                   # 手机号
    avatar = db.Column(db.String(255), unique=True)                 # 头像
    addtime = db.Column(db.DATETIME, index=True, default=datetime.now() )       # 添加时间
    uuid = db.Column(db.Integer, unique=True)                       # 唯一标识符

    comments = db.relationship("Comment", backref="user")           # 评论外键关联
    userlogs = db.relationship("Userlog", backref="user")           # 用户日志外键关联
    moviecols = db.relationship("Moviecol", backref="user")         # 收藏外键关联

    def __repr__(self):
        return "<User %r>" % self.name

# 会员登录日志
class Userlog(db.Model):

    _tablename__ = "userlog"
    id = db.Column(db.Integer, primary_key=True)                    # id
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))       # 所属会员
    ip = db.Column(db.String(100))                                  # 登录ip
    addtime = db.Column(db.DATETIME, default=datetime.now())        # 登录时间

    def __repr__(self):
        return "<Userlog %r>" % self.id

# 标签
class Tag(db.Model):

    _tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True)                    # id
    name = db.Column(db.String(100), unique=True)                   # 标签名称
    addtime = db.Column(db.DATETIME, default=datetime.now())        # 登录时间
    movies = db.relationship("Movie", backref="tag")

    def __repr__(self):
        return "<Tag %r>" % self.name

# 电影
class Movie(db.Model):

    __tablename__ = "movie"
    id = db.Column(db.Integer, primary_key=True)                    # id
    title = db.Column(db.String(100), unique=True)                  # 昵称
    url = db.Column(db.String(255), unique=True)                    # 地址
    info = db.Column(db.Text)                                       # 简介
    logo = db.Column(db.String(255), unique=True)                                # 封面
    star = db.Column(db.SmallInteger)                               # 星级
    playnum = db.Column(db.BigInteger)                                  # 播放量
    commentnum = db.Column(db.BigInteger)                               # 评论量
    tag_id = db.Column(db.Integer, db.ForeignKey("tag.id"))          # 所属标签
    area = db.Column(db.String(255))                                # 上映地区
    release_time = db.Column(db.DATE)                               # 上映时间
    length = db.Column(db.String(100))                              # 播放时间
    addtime = db.Column(db.DateTime, index=True, default=datetime.now())
    comments = db.relationship("Comment", backref="movie")          # 评论外键关联
    moviecols = db.relationship("Moviecol", backref="movie")        # 收藏外键关联

    def __repr__(self):
        return "<Movie %r>" % self.title

# 上映预告
class Preview(db.Model):

    __tablename__ = "preview"
    id = db.Column(db.Integer, primary_key=True)                    # id
    title = db.Column(db.String(255), unique=True)                  # 昵称
    logo = db.Column(db.String(255),unique=True)                    # 封面
    addtime = db.Column(db.DateTime, index=True, default=datetime.now())

    def __repr__(self):
        return "<Preview %r>" % self.title

#  评论
class Comment(db.Model):

    ___tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)                    # id
    content = db.Column(db.Text)                                    # 评论内容
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.id"))     # 所属电影
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))       # 所属用户
    addtime = db.Column(db.DateTime, index=True, default=datetime.now())

    def __repr__(self):
        return "<Comment %r>" % self.id


#  电影收藏
class Moviecol(db.Model):

    ___tablename__ = "moviecol"
    id = db.Column(db.Integer, primary_key=True)                    # id
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.id"))     # 电影id
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))       # 所属用户
    addtime = db.Column(db.DateTime, index=True, default=datetime.now())

    def __repr__(self):
        return "<Moviecol %r>" % self.id


#  权限表
class Auth(db.Model):

    _tablename__ = "auth"
    id = db.Column(db.Integer, primary_key=True)                    # id
    name = db.Column(db.String(100), unique=True)                   # 昵称
    url = db.Column(db.String(255), unique=True)                    # url
    addtime = db.Column(db.DATETIME, index=True, default=datetime.now())

    def __repr__(self):
        return "<Auth %r>" % self.id

#  角色数据模型
class Role(db.Model):

    _tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)                    # id
    name = db.Column(db.String(100), unique=True)                   # 名称
    auths = db.Column(db.String(255))                               # 角色权限列表
    addtime = db.Column(db.DATETIME, index=True, default=datetime.now())
    admins = db.relationship("Admin", backref="role")               # 管理员外键关联

    def __repr__(self):
        return "<Role %r>" % self.id

#  管理员
class Admin(db.Model):

    _tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)                    # id
    name = db.Column(db.String(100), unique=True)                   # 昵称
    pwd = db.Column(db.String(100))                                 # 密码
    is_super = db.Column(db.SMALLINT)                               # 是否是超级管理员
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"))       # 角色id
    addtime = db.Column(db.DATETIME, index=True, default=datetime.now())
    adminlogs = db.relationship("Adminlog", backref="admin")        # 日志外键关联
    oplogs = db.relationship("Oplog", backref="admin")            # 操作外键关联

    def __repr__(self):
        return "<Admin %r>" % self.id

#  管理员日志
class Adminlog(db.Model):

    _tablename__ = "adminlog"
    id = db.Column(db.Integer, primary_key=True)                    # id
    admin_id = db.Column(db.Integer, db.ForeignKey("admin.id"))     # 所属管理员
    ip = db.Column(db.String(100))                                  # 登录ip
    addtime = db.Column(db.DATETIME, default=datetime.now())        # 登录时间

    def __repr__(self):
        return "<Adminlog %r>" % self.id

#  管理员操作日志
class Oplog(db.Model):

    _tablename__ = "oplog"
    id = db.Column(db.Integer, primary_key=True)                    # id
    admin_id = db.Column(db.Integer, db.ForeignKey("admin.id"))     # 所属管理员
    ip = db.Column(db.String(100))                                  # 登录ip
    reason = db.Column(db.Text)                        # 操作原因
    addtime = db.Column(db.DATETIME, default=datetime.now())

    def __repr__(self):
        return "<Oplog %r>" % self.id

# if __name__ == "__main__":
#     from werkzeug.security import generate_password_hash
#     # role = Role(
#     #     name="super-admin",
#     #     auths=""
#     # )
#     # db.session.add(role)
#     admin = Admin(
#         name= "nido",
#         pwd = generate_password_hash("nido"),
#         is_super=0,
#         role_id=1
#     )
#     db.session.add(admin)
#     db.session.commit()
