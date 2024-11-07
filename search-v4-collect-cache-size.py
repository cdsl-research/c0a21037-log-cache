import os
import sys
import time
import statistics
import json
from logging import getLogger, basicConfig, INFO
from datetime import datetime

import collect_es_cache_size as es_cache

from elasticsearch import Elasticsearch

# Ignore warning message
import warnings
from elasticsearch.exceptions import ElasticsearchWarning

logger = getLogger(__name__)

FORMAT = f"%(asctime)s %(levelname)s %(name)s : %(message)s"

mode = os.getenv("MODE", "debug")
if mode is None:
    print("MODE should be provided", file=sys.stderr)
    sys.exit(1)
current_time = datetime.now()
timestamp = current_time.strftime("%Y%m%d_%H%M%S")
filename = f"exp-{mode}-{timestamp}"
basicConfig(format=FORMAT, level=INFO, filename=filename + ".log", filemode="a")
warnings.simplefilter("ignore", ElasticsearchWarning)

# Create connection to elasticsearch
es_host = os.getenv("ES_HOST", "10.43.253.171")
es = Elasticsearch(f"http://{es_host}:9200")
es_index = os.getenv("ES_INDEX_NAME", "l*")


def clear_cache():
    logger.info("Start clear_cache()")
    res = es.indices.clear_cache(
        request=True,  # Purge request-cache
        fielddata=True,  # Purge field-data-cache
        query=True,  # Purge query-cache
    )
    logger.info("Finish clear_cache_result " + str(res))

    return res


def q_trace_list_prop(service_name: str = "catalogue.sock-shop"):
    logger.info("Start q_trace_list_prop()")

    # Alert received date (+5m)
    date_str = "May 6, 2024 @ 11:37:00.000"
    dt = datetime.strptime(date_str, "%b %d, %Y @ %H:%M:%S.%f")
    unix_time = int(dt.timestamp() * 1000000)
    logger.info("unix_time=" + str(unix_time))

    _query = {
        "bool": {
            "must": [
                {"term": {"process.serviceName": {"value": service_name, "boost": 1}}},
                {"range": {"startTime": {"lte": unix_time}}},
                {"range": {"duration": {"gte": 3000000}}},  # 3 [sec]
            ]
        }
    }
    _aggs = {
        "distinct_operations": {
            "terms": {
                "field": "operationName",
                "size": 10000,
                "min_doc_count": 1,
                "shard_min_doc_count": 0,
                "show_term_doc_count_error": False,
                "order": [{"_count": "desc"}, {"_key": "asc"}],
            }
        }
    }

    resp = es.search(
        index=es_index,
        query=_query,
        size=10000,
        aggregations=_aggs,
        track_total_hits=2147483647,
    )
    logger.info(f"Found: {resp['hits']['total']}")

    return resp


def q_trace_list_fifo(service_name: str = "catalogue.sock-shop"):
    logger.info("Start q_trace_list_prop()")

    date_str = "May 6, 2024 @ 11:47:00.000"
    dt = datetime.strptime(date_str, "%b %d, %Y @ %H:%M:%S.%f")
    unix_time = int(dt.timestamp() * 1000000)
    logger.info("unix_time=" + str(unix_time))

    _query = {
        "bool": {
            "must": [
                {"term": {"process.serviceName": {"value": service_name, "boost": 1}}},
                {"range": {"startTime": {"lte": unix_time}}},
            ]
        }
    }
    _aggs = {
        "distinct_operations": {
            "terms": {
                "field": "operationName",
                "size": 10000,
                "min_doc_count": 1,
                "shard_min_doc_count": 0,
                "show_term_doc_count_error": False,
                "order": [{"_count": "desc"}, {"_key": "asc"}],
            }
        }
    }

    resp = es.search(
        index=es_index,
        query=_query,
        size=10000,
        aggregations=_aggs,
        track_total_hits=2147483647,
    )
    logger.info(f"Found: {resp['hits']['total']}")

    return resp


def q_single_trace(trace_id: str):
    logger.info("Start q_single_trace()")
    _query = {
        "bool": {
            "must": [
                {
                    "term": {
                        "traceID": {
                            "value": trace_id,
                            "boost": 1,
                        }
                    }
                }
            ],
            "adjust_pure_negative": True,
            "boost": 1,
        }
    }

    start_time = time.time()
    resp = es.search(index=es_index, query=_query)
    logger.info(f"Found: {resp['hits']['total']}")
    elapsed_time = time.time() - start_time

    return (elapsed_time, resp)


def proposed(trace_list: list):
    # sort by 'duration'
    trace_lst_s = sorted(
        trace_list, key=lambda x: x[1], reverse=True
    )  # 1000, 900, 800 ...
    logger.info(f"proposed length: {len(trace_lst_s)}")
    logger.info(f"proposed result: {json.dumps(trace_lst_s)}")
    return trace_lst_s


def fifo(trace_list: list):
    trace_lst_s = sorted(
        trace_list, key=lambda x: x[1], reverse=True
    )  # 1000, 900, 800 ...
    logger.info(f"proposed length: {len(trace_lst_s)}")
    logger.info(f"proposed result: {json.dumps(trace_lst_s)}")
    return trace_lst_s


def dump(dat, fname):
    d = json.dumps(dat)
    with open(fname, mode="w") as f:
        f.write(d)
    logger.info(f"Data has been stored on {fname}")


def cache_subtraction(d_from, d_to):
    result = {}
    for node in d_from.keys():
        result[node] = {}
        for k in d_from[node].keys():
            result[node][k] = d_from[node][k] - d_to[node][k]
    return result


def main():
    qcache = es_cache.get_query_cache()
    logger.info("Query_cache: " + json.dumps(qcache))

    clear_cache()

    qcache2 = es_cache.get_query_cache()
    logger.info("Query_cache: " + json.dumps(qcache))
    diff = cache_subtraction(qcache2, qcache)
    logger.info("Query_cache_sub: " + json.dumps(diff))

    resp = q_trace_list_prop(service_name="front-end.sock-shop")
    founds = resp["hits"]["hits"]
    # logger.info("response_body: " + json.dumps(founds))
    logger.info("Response_size: %s" % len(json.dumps(founds)))

    time.sleep(3)  # waiting 3 sec

    qcache3 = es_cache.get_query_cache()
    logger.info("Query_cache: " + json.dumps(qcache))
    diff = cache_subtraction(qcache3, qcache2)
    logger.info("Query_cache_sub: " + json.dumps(diff))

    return

    trace_lst = []
    for found in founds:
        trace_id = found["_source"]["traceID"]
        duration = found["_source"]["duration"]
        start_time = found["_source"]["startTime"]
        trace_lst.append((trace_id, duration, start_time))
    logger.info(f"trace_lst length: {len(trace_lst)}")

    l = proposed(trace_list=trace_lst)
    dump(l, filename + ".json")
    return


if __name__ == "__main__":
    main()
