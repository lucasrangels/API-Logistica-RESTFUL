from src.model.User import UserSchema as ModelUser
from src.model.Schema import UserSchema as SchemaUser
from src.model.User import UserLoginSchema as LoginUser
from src.model.Schema import UserLoginSchema as SchemaLogin
from fastapi import APIRouter, Depends
from src.auth.AuthHandler import sign_jwt
from src.auth.AuthBearer import JWTBearer
from fastapi_sqlalchemy import db
from src.auth.PasswordEncrypt import encrypt, decrypt

router = APIRouter()


@router.post("/user/signup", tags=["users"])
async def create_user(user: SchemaUser):
    encrypted_password = encrypt(user.password)
    db_user = ModelUser(fullname=user.fullname,
                        email=user.email,
                        password=encrypted_password)
    db.session.add(db_user)
    db.session.commit()
    return {"Resultado": "Usuário criado com sucesso."}


@router.post("/user/login", tags=["users"])
async def login(user: SchemaLogin):
    user_login = db.session.query(ModelUser).filter_by(email=user.email).first()
    if not user_login:
        return {"Erro": "Usuário inexistente"}
    is_pswrd_valid = decrypt(user.password, user_login.password)
    if not is_pswrd_valid:
        return {"Erro": f"Senha incorreta."}
    login_user = LoginUser(email=user.email, password=user_login.password, user_role=user_login.role)
    db.session.add(login_user)
    db.session.commit()
    return sign_jwt(user.email)



@router.get("/user/get_all", dependencies=[Depends(JWTBearer())], tags=["users"])
async def get_users():
    users = db.session.query(ModelUser).all()
    return users


def load_default_admin_user(app, database):
    with db():
        db_admin = database.session.query(ModelUser).filter_by(fullname="admin", email="admin@email.com")
        if not db_admin:
            admin_password = "admin"
            encrypted_password = encrypt(admin_password)
            admin_user = ModelUser(fullname="admin", email="admin@email.com", password=encrypted_password)
            database.session.add(admin_user)
            database.session.commit()
