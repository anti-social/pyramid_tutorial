from typing import Any
from typing import Dict
from typing import Union

from pyramid.httpexceptions import HTTPBadRequest
from pyramid.httpexceptions import HTTPFound
from pyramid.httpexceptions import HTTPNotFound
from pyramid.request import Request
from pyramid.response import Response
from pyramid.view import view_config

from .documents import get_es_product_index
from .documents import ProductDoc
from .forms import ProductForm
from .models import db_session
from .models import Product


ViewResponse = Union[Response, Dict[str, Any]]


def hello_world(request: Request) -> Response:
    print('Incoming request')
    return Response('<body><h1>Hello World!</h1></body>')


@view_config(route_name='product_create', renderer='product_edit.jinja2')
def product_create(request: Request) -> Response:
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
def product_edit(request: Request) -> ViewResponse:
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
def products(request: Request) -> ViewResponse:
    products = (
        db_session.query(Product)
        .filter(Product.status == 0)
        .limit(10)
        .all()
    )
    return {
        'products': products,
    }


@view_config(route_name='product_search', renderer='products.jinja2')
def product_search(request: Request) -> ViewResponse:
    q = request.GET['q'].strip()
    if not q:
        return HTTPBadRequest()
    es_product_index = get_es_product_index(request.registry.settings)
    sq = es_product_index.search_query(ProductDoc.name.match(q))
    res = sq.get_result()
    return {
        'products': res.hits
    }
