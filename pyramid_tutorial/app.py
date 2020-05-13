import logging

from pyramid.config import Configurator
from pyramid.response import Response

from sqlalchemy import engine_from_config

from waitress import serve

from .models import db_session
from .models import Product


log = logging.getLogger(__name__)


def hello_world(request):
    print('Incoming request')
    products = db_session.query(Product).all()
    return Response(f'<body><h1>Hello World!</h1></body>')


def products(request):
    products = (
        db_session.query(Product)
        .filter(Product.status == 0)
        .limit(10)
        .all()
    )
    product_list_html = '\n'.join(f'<p>{p.id}<p>{p.name}' for p in products)
    return Response(f'<body><h1>Our store products!</h1>{product_list_html}</body>')


def main(global_config, **settings):
    config = Configurator(settings=settings)
    engine = engine_from_config(settings, prefix='sqlalchemy.')
    db_session.configure(bind=engine)
    config.add_route('hello', '/')
    config.add_view(hello_world, route_name='hello')
    config.add_route('products', '/products')
    config.add_view(products, route_name='products')
    return config.make_wsgi_app()
