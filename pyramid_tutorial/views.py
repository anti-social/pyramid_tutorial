from pyramid.response import Response
from pyramid.view import view_config

from .models import db_session
from .models import Product


def hello_world(request):
    print('Incoming request')
    products = db_session.query(Product).all()
    return Response(f'<body><h1>Hello World!</h1></body>')


@view_config(route_name='products', renderer='products.jinja2')
def products(request):
    products = (
        db_session.query(Product)
        .filter(Product.status == 0)
        .limit(10)
        .all()
    )
    return {
        'products': products,
    }
