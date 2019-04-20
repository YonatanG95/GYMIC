from elasticsearch import Elasticsearch
from datetime import datetime

from conf import ELK_SERVER_IP, ELK_SERVER_PORT

class ElasticUtil():

    def __init__(self):
        try:
            self.es = Elasticsearch([{'host': ELK_SERVER_IP, 'port': ELK_SERVER_PORT}])
        except Exception as e:
            print e.message

    def send_to_elastic(self, index_name, doc_type, doc):
        try:
            res = self.es.index(index=index_name, doc_type=doc_type, body=doc)
        except Exception as e:
            print e.message

    def log(self, msg):
        try:
            doc = {"Message": msg, "timestamp": datetime.utcnow()}
            res = self.es.index(index="gymic-log", body=doc)
        except Exception as e:
            print e.message

    def log_error(self, error_msg):
        try:
            doc = {"Message": error_msg, "timestamp": datetime.utcnow()}
            res = self.es.index(index="gymic-log-error", body=doc)
        except Exception as e:
            print e.message