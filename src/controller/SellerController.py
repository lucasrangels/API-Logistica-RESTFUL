from src.model.Route import RouteSchema as ModelRoute
from src.model.Schema import RouteSchema as SchemaRoute
from src.model.Seller import SellerSchema as ModelSeller
from src.model.Schema import SellerSchema as SchemaSeller
from src.auth.Permissions import check_admin_permission
from fastapi import APIRouter, Depends
from src.auth.AuthBearer import JWTBearer
from fastapi_sqlalchemy import db

router = APIRouter()


@router.post("/seller/create", response_model=SchemaSeller, dependencies=[Depends(JWTBearer())], tags=["sellers"])
async def create_seller(seller: SchemaSeller):
    if not check_admin_permission():
        return {"Erro": "Usuário não tem permissão para cadastrar vendedores"}
    db_seller = ModelSeller(name=seller.name, email=seller.email)
    db.session.add(db_seller)
    db.session.commit()
    return db_seller


@router.get("/seller/get_all", dependencies=[Depends(JWTBearer())], tags=["sellers"])
async def get_sellers():
    if not check_admin_permission():
        return {"Erro": "Usuário não tem permissão para visualizar o cadastro de vendedores"}
    sellers = db.session.query(ModelSeller).all()
    return sellers


@router.delete("/seller/delete", response_model=SchemaSeller, dependencies=[Depends(JWTBearer())], tags=["sellers"])
async def delete_seller(seller: SchemaSeller):
    if not check_admin_permission():
        return {"Erro": "Usuário não tem permissão para deletar vendedores"}
    db_seller = db.session.query(ModelSeller).filter_by(name=seller.name, email=seller.email).delete()
    if not db_seller:
        return {"Erro": "Vendedor não encontrado para exclusão"}
    else:
        try:
            db.session.commit()
        except:
            return {"Erro": "Não foi possível excluir a entrada"}
        return {"Sucesso": "Vendedor excluído com sucesso."}
