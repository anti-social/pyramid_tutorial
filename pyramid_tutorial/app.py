from pyramid.config import Configurator
from pyramid.response import Response

from sqlalchemy import engine_from_config

from waitress import serve

from .models import db_session
from .models import Product


def hello_world(request):
    print('Incoming request')
    num_products = db_session.query(Product).count()
    return Response(f'<body><h1>Hello World!</h1><p>{num_products}</body>')


def main(global_config, **settings):
    from pprint import pprint

    with Configurator(settings=settings) as config:
        engine = engine_from_config(settings, 'sqlalchemy.')
        pprint(engine.execute('select version()').fetchone())
        db_session.configure(bind=engine)
        config.add_route('hello', '/')
        config.add_view(hello_world, route_name='hello')
        pprint(config.get_settings())
        return config.make_wsgi_app()
