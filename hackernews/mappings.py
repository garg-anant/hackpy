from elasticsearch import Elasticsearch
# conntect es
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
# delete index if exists
if es.indices.exists(config.elastic_urls_index):
    es.indices.delete(index=config.elastic_urls_index)
# index settings
settings = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0
    },
    "mappings": {
        "urls": {
            "properties": {
                "url": {
                    "type": "string"
                }
            }
        }
     }
}