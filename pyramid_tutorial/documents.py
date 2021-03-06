from elasticsearch import Elasticsearch

from elasticmagic import Cluster
from elasticmagic import Document
from elasticmagic import Field
from elasticmagic.types import Text
from elasticmagic.types import Integer


es_client = Elasticsearch()
es_cluster = Cluster(es_client)


def get_es_product_index(settings):
    return es_cluster[settings['elasticsearch.product_index']]


class ProductDoc(Document):
    __doc_type__ = 'product'

    name = Field(Text)
    status = Field(Integer)
