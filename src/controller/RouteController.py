from src.model.Route import RouteSchema as ModelRoute
from src.model.Schema import RouteSchema as SchemaRoute, AssignSchema
from src.model.Seller import SellerSchema as ModelSeller
from src.model.Customers import CustomersSchema as ModelCustomer
from src.resources.GeoJSON import check_geojson_integrity, check_point_in_polygon
from src.auth.Permissions import check_admin_permission
from fastapi import APIRouter, Depends, Form
from src.auth.AuthBearer import JWTBearer
from fastapi_sqlalchemy import db

router = APIRouter()


@router.post("/route/create", dependencies=[Depends(JWTBearer())], tags=["routes"])
async def create_route(name: str = Form(...), bounds: str = Form(...)):
    if not check_admin_permission():
        return {"Erro": "Usuário não tem permissão para cadastrar rotas"}
    db_route = db.session.query(ModelRoute).filter_by(name=name).first()
    if db_route:
        return {"Erro": "Rota já está cadastrada."}
    else:
        is_geojson = check_geojson_integrity(bounds)
        if not is_geojson:
            return {"Erro": "O JSON inserido não é um GeoJSON"}
        else:
            new_route = ModelRoute(name=name, bounds=bounds)
            db.session.add(new_route)
            db.session.commit()
            update_routes_in_customers(new_route)
            return {"Sucesso": "Rota criada com sucesso"}


@router.get("/route/get_all", dependencies=[Depends(JWTBearer())], tags=["routes"])
async def get_routes():
    if not check_admin_permission():
        return {"Erro": "Usuário não tem permissão para obter rotas"}
    routes = db.session.query(ModelRoute).all()
    return routes


@router.put("/route/edit", response_model=SchemaRoute, dependencies=[Depends(JWTBearer())], tags=["routes"])
async def edit_route(name: str = Form(...), bounds: str = Form(...)):
    if not check_admin_permission():
        return {"Erro": "Usuário não tem permissão para editar rotas"}
    db_route = db.session.query(ModelRoute).filter_by(name=name, bounds=bounds).first()
    if not db_route:
        return {"Erro": "Não foi possível editar pois a rota não existe"}
    else:
        db_route.name = name
        db_route.bounds = bounds
        db.session.add(db_route)
        try:
            db.session.commit()
        except:
            return {"Erro": "Erro de duplicidade para ID"}
        update_routes_in_customers(ModelRoute(name=name, bounds=bounds))
        return db_route


@router.delete("/route/delete", dependencies=[Depends(JWTBearer())], tags=["routes"])
async def delete_route(route_name):
    if not check_admin_permission():
        return {"Erro": "Usuário não tem permissão para deletar rotas"}
    db_route = db.session.query(ModelRoute).filter_by(name=route_name).delete()
    if not db_route:
        return {"Erro": "Rota não encontrada para exclusão"}
    else:
        try:
            db.session.commit()
        except:
            return {"Erro": "Não foi possível excluir a entrada"}
        return {"Sucesso": "Rota excluída com sucesso."}


@router.put("/route/assign_seller", dependencies=[Depends(JWTBearer())], tags=["routes"])
async def assign_seller(assign: AssignSchema):
    if not check_admin_permission():
        return {"Erro": "Usuário não tem permissão para atribuir vendedoras"}
    seller = db.session.query(ModelSeller).filter_by(email=assign.seller_email).first()
    if not seller:
        return {"Erro": "Vendedor não existe"}
    else:
        route = db.session.query(ModelRoute).filter_by(name=assign.route_name).first()
        if not route:
            return {"Erro": "Rota não existe"}
        else:
            raw_id = seller.id
            route.seller_id = str(raw_id)
            db.session.commit()
            return {"Sucesso": f"Rota {assign.route_name} atribuída ao vendedor {seller.name}"}


@router.put("/route/disassociate_seller", dependencies=[Depends(JWTBearer())], tags=["routes"])
async def disassociate_seller(route_name: str):
    if not check_admin_permission():
        return {"Erro": "Usuário não tem permissão para desvincular vendedores"}
    db_route = db.session.query(ModelRoute).filter_by(name=route_name).first()
    if not db_route:
        return {"Erro": "Não foi possível desassociar o vendedor da rota pois a mesma não existe"}
    else:
        db_route.seller_id = None
        try:
            db.session.commit()
        except:
            return {"Erro": "Erro de duplicidade para ID"}
        return {"Sucesso": f"Rota {db_route.name} teve seu vendedor desvinculado"}


def update_routes_in_customers(route: ModelRoute):
    locations = db.session.query(ModelCustomer.geolocation).filter(ModelCustomer.associated_route == "Outros").all()

    for location in locations:
        result = check_point_in_polygon(route.bounds, location)

        if result:
            customers_new_route = db.session.query(ModelCustomer).filter(ModelCustomer.geolocation == location).all()
            for customers in customers_new_route:
                customers.associated_route = route.name
                db.session.add(customers)
                db.session.commit()
