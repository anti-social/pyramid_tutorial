from pyramid.config import Configurator
from pyramid.response import Response

from sqlalchemy import engine_from_config

from waitress import serve

from .models import db_session
from .models import Product


def hello_world(request):
    print('Incoming request')
    products = db_session.query(Product).all()
    return Response(f'<body><h1>Hello World!</h1></body>')


def main(global_config, **settings):
    with Configurator(settings=settings) as config:
        engine = engine_from_config(settings, prefix='sqlalchemy.')
        db_session.configure(bind=engine)
        config.add_route('hello', '/')
        config.add_view(hello_world, route_name='hello')
        return config.make_wsgi_app()
