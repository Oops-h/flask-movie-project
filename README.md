# flask-movie-project
flask电影网站实战
完成注册页面

manager.py 无法正常运行
正在完成会员页面，修改密码、登录日志查看、电影收藏列表、个人信息等


标签管理
1、分页使用sqlalchemy.Pagination
url:http://www.pythondoc.com/flask-sqlalchemy/api.html?highlight=next#flask.ext.sqlalchemy.Pagination.next
模型：Tag
表单：TagFrom
请求方法：get、post
访问控制：@admin_login_req

电影管理
1、使用werkzeug.utils.secure_filename存储路径
模型：Movie
表单：MovieForm
请求方法：get post
访问控制：@ admin_login_req
