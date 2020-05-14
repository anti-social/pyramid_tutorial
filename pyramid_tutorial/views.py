from pyramid.httpexceptions import HTTPBadRequest
from pyramid.httpexceptions import HTTPFound
from pyramid.httpexceptions import HTTPNotFound
from pyramid.response import Response
from pyramid.view import view_config

from .forms import ProductForm
from .models import db_session
from .models import Product


def hello_world(request):
    print('Incoming request')
    products = db_session.query(Product).all()
    return Response(f'<body><h1>Hello World!</h1></body>')


@view_config(route_name='product_create', renderer='product_edit.jinja2')
def product_create(request):
    form = ProductForm(request.POST)
    if request.method == 'POST' and form.validate():
        product = Product()
        form.populate_obj(product)
        db_session.add(product)
        db_session.flush()
        return HTTPFound(request.route_url('products'))
    return {
        'form': form,
    }


@view_config(route_name='product_edit', renderer='product_edit.jinja2')
def product_edit(request):
    try:
        product_id = int(request.matchdict['id'])
    except ValueError:
        return HTTPBadRequest()

    product = db_session.query(Product).get(product_id)
    if not product:
        return HTTPNotFound()

    form = ProductForm(request.POST, product)
    if request.method == 'POST' and form.validate():
        form.populate_obj(product)
        db_session.add(product)
        db_session.flush()
        return HTTPFound(request.route_url('products'))
    return {
        'form': form,
    }


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
