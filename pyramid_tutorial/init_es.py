import os
import sys
import logging

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
)

from .documents import es_client
from .documents import es_cluster
from .documents import ProductDoc
from .models import db_session
from .models import Product


log = logging.getLogger(__name__)


class ElasticsearchBulkError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]

    setup_logging(config_uri)

    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    db_session.configure(bind=engine)

    index_name = 'pyramid_tutorial_product'
    es_client.indices.create(
        index=index_name,
        body={
            'settings': {
                'index': {
                    'number_of_shards': 4,
                    'number_of_replicas': 0,
                }
            }
        }
    )
    es_product_index = es_cluster[index_name]
    es_product_index.put_mapping(ProductDoc)

    limit = 5
    last_product_id = None
    indexed_count = 0
    while True:
        query = (
            db_session.query(Product.id, Product.name, Product.status)
            .order_by(Product.id)
        )
        if last_product_id is not None:
            query = query.filter(Product.id > last_product_id)
        products = query.limit(limit).all()

        if not products:
            break

        docs = [
            ProductDoc(_id=p.id, name=p.name, status=p.status)
            for p in products
        ]
        bulk_res = es_product_index.add(docs)
        indexed_count += len(docs)
        if bulk_res.errors:
            raise ElasticsearchBulkError(
                '\n' +
                '\n'.join(
                    '\t{}'.format(it.error.reason) for it in bulk_res.items
                )
            )

        if len(products) < limit:
            break
        last_product_id = products[-1].id

    es_product_index.refresh()

    log.info('Indexed %s products', indexed_count)
    log.info(
        '%s products in the index',
        es_product_index.search_query().count()
    )
