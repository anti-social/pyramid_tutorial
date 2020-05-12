from pyramid.config import Configurator
from pyramid.response import Response

from sqlalchemy import engine_from_config
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from waitress import serve

from zope.sqlalchemy import register as register_session


db_session = scoped_session(sessionmaker())
register_session(db_session)


def hello_world(request):
    print('Incoming request')
    return Response('<body><h1>Hello World!</h1></body>')


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
