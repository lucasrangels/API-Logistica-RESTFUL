from src.resources.LocationModule import get_location_by_coordinates, get_coordinates_by_location
from src.model.Customers import CustomersSchema as ModelCustomer
from src.model.Schema import CostumerSchema as SchemaCustomer, NameCostumerSchema
from src.model.Route import RouteSchema as ModelRoute
from fastapi import APIRouter, Depends
from src.auth.AuthBearer import JWTBearer
from fastapi_sqlalchemy import db
from src.auth.Permissions import check_admin_permission
from src.resources.GeoJSON import check_geojson_integrity, check_point_in_polygon

router = APIRouter()


@router.post("/customer/create", dependencies=[Depends(JWTBearer())], tags=["customers"])
async def create_customer(customer: SchemaCustomer):
    full_address = f"{customer.street_address} {customer.address_number} {customer.city} {customer.state} {customer.zip_code} Brasil "
    address_result = get_coordinates_by_location(full_address)
    if not address_result:
        return {"Erro": "Endereço não encontrado. Detalhe para obter resultado mais preciso"}
    else:
        db_customer = ModelCustomer(name=customer.name,
                                    street_address=customer.street_address,
                                    address_number=customer.address_number,
                                    city=customer.city,
                                    state=customer.state,
                                    zip_code=customer.zip_code,
                                    geolocation=address_result)
        db.session.add(db_customer)
        db.session.commit()
        update_customers_routes(db_customer)
        return {"Sucesso": f"Cliente {customer.name} criado com sucesso para a localização {address_result}"}


@router.get("/customer/get_all", dependencies=[Depends(JWTBearer())], tags=["customers"])
async def get_customers():
    customers = db.session.query(ModelCustomer).all()
    return customers


@router.get("/customer/get_by_route", dependencies=[Depends(JWTBearer())], tags=["customers"])
async def get_customers_by_route(route_name: str):
    if not check_admin_permission():
        return {"Erro": "Usuário não tem permissão para visualizar clientes por rota"}
    db_customers = db.session.query(ModelCustomer).filter(ModelCustomer.associated_route == route_name).all()

    return db_customers


@router.put("/customer/edit", dependencies=[Depends(JWTBearer())], tags=["customers"])
async def edit_customer(customer: SchemaCustomer):
    db_customer = db.session.query(ModelCustomer).filter_by(name=customer.name).first()
    if not db_customer:
        return {"Erro": "Não foi possível editar pois o cliente não existe"}
    else:
        full_address = f"{customer.street_address} {customer.address_number} {customer.city} {customer.state} {customer.zip_code} Brasil "
        address_result = get_coordinates_by_location(full_address)
        if not address_result:
            return {"Erro": "Endereço não encontrado. Detalhe para obter resultado mais preciso"}
        else:
            db_customer.name = customer.name
            db_customer.street_address = customer.street_address
            db_customer.address_number = customer.address_number
            db_customer.city = customer.city
            db_customer.state = customer.state
            db_customer.zip_code = customer.zip_code
            db_customer.geolocation = address_result
            db.session.add(db_customer)
            try:
                db.session.commit()
            except:
                return {"Erro": "Erro de duplicidade para ID"}
            return {"Sucesso": "Cliente editado com sucesso"}


@router.delete("/customer/delete", dependencies=[Depends(JWTBearer())], tags=["customers"])
async def delete_customer(customer: NameCostumerSchema):
    db_costumer = db.session.query(ModelCustomer).filter_by(name=customer.name).delete()
    if not db_costumer:
        return {"Erro": "Cliente não encontrado para exclusão"}
    else:
        try:
            db.session.commit()
        except:
            return {"Erro": "Não foi possível excluir a entrada"}
        return {"Sucesso": "Cliente excluído com sucesso."}


def update_customers_routes(customer: ModelCustomer):
    routes = db.session.query(ModelRoute).all()

    for route in routes:
        result = check_point_in_polygon(route.bounds, customer.geolocation)

        if result:
            customer_new_route = db.session.query(ModelCustomer).filter(ModelCustomer.name == customer.name).first()
            customer_new_route.associated_route = route.name
            db.session.add(customer_new_route)
            db.session.commit()
