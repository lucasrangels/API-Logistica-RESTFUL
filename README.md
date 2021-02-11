<h1 align="center">
	Sistema de Logística - REST API<br/>
	<a href="https://www.stone.com.br" target="_blank">
		<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c9/Stone_pagamentos.png/800px-Stone_pagamentos.png" width="250" />
	</a>
	
  
  
</h1>

## Proposta
  Desafio proposto pela fintech Stone Pagamentos, com o intuito de desenvolver uma API REST cuja finalidade é o gerenciamento de clientes, vendedores e rotas comerciais baseados em suas coordenadas.
  
  Este projeto foi desenvolvido na linguagem de programação PYTHON utilizando o FrameWork FastAPI. O banco de dados escolhido para armazenamento em geral foi o PostgreSQL, além do ORM SQLAlchemy para facilitar transações e garantir segurança ao processo.


## Tecnologias

### FrameWork
* <a href="https://fastapi.tiangolo.com/" target="_blank">FastAPI</a>

### Bancos de dados
* <a href="https://www.postgresql.org" target="_blank">Postgres</a>

### Autenticação/Segurança

* <a href="https://pyjwt.readthedocs.io/en/stable/" target="_blank">PyJWT</a>

* <a href="https://pypi.org/project/python-oauth2/" target="_blank">OAuth2</a>

* <a href="https://pypi.org/project/bcrypt/" target="_blank">BCrypt</a>


## GeoLocalização

* <a href="https://pypi.org/project/geopy/" target="_blank">GeoPy</a>

* <a href="https://pypi.org/project/geojson//" target="_blank">GeoJSON</a>


## Como Rodar
> É necessário o Docker para executar os passos abaixo

1- Faça a construção inicial do projeto via Docker.
```
$ docker-compose build
```

2- Inicie o projeto.

```
$ docker-compose up
```


## Modelo de Dados
A API possui operação de CRUD para as entidades listadas abaixo:

- Rota:

- Vendedores:

- Clientes:

- Usuários


## Endpoints

### Usuários/Users

- Create User
```
{
  "fullname": "Lucas Serra",
  "email": "Lucas@email.com",
  "password": "123"
}
```

- Login
```
{
  "email": "Lucas@email.com",
  "password": "123"
}
```

### Rotas/Routes
Em alguns requests será necessário um GeoJSON, ou seja, um polígono 2D representando uma área de atuação de um possível vendedor.
Para obter o JSON de forma gráfica acesse o endereço <a href="https://geojson.io/" target="_blank">GeoJSON.io</a>

- Create Route
```
{
  "name": "Rota 1",
  "bounds": "<GEOJSON>"
}
```
- Edit Route
```
{
  "name": "Rota 1",
  "bounds": "<GEOJSON>"
}
```
- Delete Route
```
{
  "route_name": "Rota 1"
}
```
- Get Routes
```
{}
```
- Assign Seller
```
{
  "route_name": "Rota 1",
  "seller_email": "Vendedor 1"
}
```
- Disassociate Seller
```
{
  "route_name": "Rota 1",
  "seller_email": "Vendedor 1"
}
```

### Vendedores/Sellers

- Create Seller
```
{
  "name": "string",
  "email": "string"
}
```
- Get Seller
```
{}
```
- Delete Seller
```
{
  "name": "string",
  "email": "string"
}
```

### Clientes/Customers
Para definir se o cliente está em uma rota de entrega ou não é utilizado o cruzamento de informações geográficas baseadas no ponto(coordenadas) onde o cliente está
 com o polígono 2D cadastrado em cada rota. As coordenadas são obtidas automaticamente a partir do endereço do cliente.
 
- Create Customer
```
{
  "name": "Cliente 1",
  "street_address": "Rua Exemplo",
  "address_number": "123",
  "city": "Cidade Exemplo",
  "state": "Estado Exemplo",
  "zip_code": 00000000
}
```
- Edit Customer
```
{
  "name": "Cliente 1",
  "street_address": "Rua Exemplo",
  "address_number": "123",
  "city": "Cidade Exemplo",
  "state": "Estado Exemplo",
  "zip_code": 00000000
}
```
- Delete Customer
```
{
  "name": "string"
}
```
- Get Customer
```
{}
```
- Get Customer by Route
```
{
  "route_name": "Rota 1" 
}
```
