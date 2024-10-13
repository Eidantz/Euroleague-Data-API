import strawberry
from strawberry.asgi import GraphQL
from schema import schema

graphql_app = GraphQL(schema)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(graphql_app, host="0.0.0.0", port=8000)
