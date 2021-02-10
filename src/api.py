from fastapi.routing import APIRoute
from fastapi import FastAPI, Body, APIRouter, Request, Response
from ast import literal_eval
from src.controller import UserController
from src.controller import RouteController
from src.controller import SellerController
from src.controller import CustomerController
from typing import Callable
import json


class CustomRoute(APIRoute):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            request_body = await request.body()

            request_body = literal_eval(request_body.decode("utf-8"))

            request_body = json.dumps(request_body).encode("utf-8")

            request._body = request_body  # Note that we are overriding the incoming request's body

            response = await original_route_handler(request)
            return response

        return custom_route_handler


api_router = APIRouter(route_class=CustomRoute)
api_router.include_router(UserController.router)
api_router.include_router(RouteController.router)
api_router.include_router(SellerController.router)
api_router.include_router(CustomerController.router)
