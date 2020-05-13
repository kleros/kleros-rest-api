from src.routes.t2cr import register_t2cr_routes

def register_all(app):
    register_t2cr_routes(app)
