import logging

from pyramid.config import Configurator

from sqlalchemy import engine_from_config

from .models import db_session


log = logging.getLogger(__name__)


def main(global_config, **settings):
    config = Configurator(settings=settings)

    # Database
    engine = engine_from_config(settings, prefix='sqlalchemy.')
    db_session.configure(bind=engine)
    config.include('pyramid_tm')

    # Templating
    config.include('pyramid_jinja2')

    # Routing
    config.add_route('hello', '/')
    config.add_route('products', '/products')
    config.add_route('product_create', '/products/create')
    config.add_route('product_edit', '/products/edit/{id}')
    config.scan('.views')

    return config.make_wsgi_app()
