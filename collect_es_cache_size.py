import json
from logging import INFO, basicConfig, getLogger

import requests

# put in entry point file
CHAR_GREEN = "\033[32m"
CHAR_RESET = "\033[0m"
FORMAT = f"{CHAR_GREEN}%(asctime)s %(levelname)s %(name)s {CHAR_RESET}: %(message)s"
basicConfig(level=INFO, format=FORMAT)

# put in all files
logger = getLogger(__name__)

base_url = "http://10.43.253.171:9200"


def get_req_cache():
    # request cache
    res = requests.get(base_url + "/_nodes/stats/indices/request_cache")
    res_j = res.json()["nodes"]

    d_node_cache = {}
    for node_id, val in res_j.items():
        name = val["name"]
        req_cache = val["indices"]["request_cache"]
        # print(name, req_cache)
        d_node_cache[name] = req_cache
    return d_node_cache


def get_query_cache():
    # node cache
    res = requests.get(base_url + "/_nodes/stats/indices/query_cache")
    res_j = res.json()["nodes"]
    # print(json.dumps(res_j, indent=4))

    d_node_cache = {}
    for node_id, val in res_j.items():
        name = val["name"]
        query_cache = val["indices"]["query_cache"]
        # print(name, req_cache)
        d_node_cache[name] = query_cache
    return d_node_cache


def main():
    req_cache = get_req_cache()
    logger.info(req_cache)

    query_cache = get_query_cache()
    logger.info(query_cache)


if __name__ == "__main__":
    main()
