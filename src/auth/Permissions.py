from src.model.User import UserLoginSchema as LoginUser
from fastapi_sqlalchemy import db
import datetime


def check_admin_permission():
    active_user = db.session.query(LoginUser).filter_by(user_role='admin').order_by(LoginUser.login_date.desc()).first()
    if not active_user:
        return False
    acc_login_time = active_user.login_date + datetime.timedelta(minutes=10)

    if acc_login_time >= datetime.datetime.utcnow():
        return True
    else:
        return False
