import os
import time #制度低め，時間を扱う
import statistics #平均,中央値等を計算してくれる
from logging import getLogger, basicConfig, INFO #ログを読み込む用
from datetime import datetime #精度高め，日時を扱う
from elasticsearch import Elasticsearch

# Ignore warning message
import warnings#警告を出せるようになる
from elasticsearch.exceptions import ElasticsearchWarning#↑のElastisearch版

logger = getLogger(__name__)#ログの取得

# CHAR_GREEN = '\033[32m'
# CHAR_RESET = '\033[0m'
# FORMAT = f"{CHAR_GREEN}%(asctime)s %(levelname)s %(name)s {CHAR_RESET}: %(message)s"　#メッセージに変換
FORMAT = f"%(asctime)s %(levelname)s %(name)s : %(message)s"#読み込んだログをどのように判断するか

current_time = datetime.now()#今の日時を取得
timestamp = current_time.strftime("%Y%m%d_%H%M%S")#日時を変換
filename = f"exp_{timestamp}.txt"#出力ファイル名
basicConfig(format=FORMAT, level=INFO, filename=filename, filemode='a')#読み込んだログをどのようにするか

warnings.simplefilter("ignore", ElasticsearchWarning)#ElasticsearchWarningを無視（ignore）

# Create connection to elasticsearch
es_host = os.getenv("ES_HOST", "10.43.253.171")
es = Elasticsearch(f"http://{es_host}:9200")
es_index = os.getenv("ES_INDEX_NAME", "l*")#どこのインデックス（Elastisearchのログ保存してるとこ）か

def clear_cache():
    logger.info("Start clear_cache()")
    res = es.indices.clear_cache(#キャッシュクリア
        request=True,#Purge request-cache# 同じリクエストが繰り返し行われたときに結果を再利用するためのキャッシュ
        fielddata=True,# Purge field-data-cache #フィールドエリア
        query=True, #Purge query-cache# クエリ結果
    )
    logger.info("Finish clear_cache_result " + str(res))#キャッシュクリアしたら表示するよ

def q_single_trace(trace_id: str):
    logger.info("Start q_single_trace()")

    # クエリを定義
    _query = {
        "match": {
            "message": f"Configured paths: [/var/log/containers/{trace_id}.log]"

        }
    }

    #Elasticsearchの検索を実行
    start_time = time.time()
    resp = es.search(index=es_index, query=_query)
    logger.info(f"Found: {resp['hits']['total']}")

    elapsed_time = time.time() - start_time

    return (elapsed_time, resp)

"""
Collection of sample data
0a6aedee1ab8e07bf2194750aea6cd17 14
1bab7367306bccb4df20d4b7104dd5f4 14
2ae99ad9d3f98a96b6860a71f53c4fcb 14
5b6f806669b0fc4b36919663569f8854 14
47e426b544f8d48b3c3904674e5e9590 13
5682508746d8551c09956a8cc93735c8 13
"""

def main():
    default_trace_id = "0a6aedee1ab8e07bf2194750aea6cd17"
    trace_id = os.getenv("TRACE_ID", default_trace_id)
    if trace_id == default_trace_id:
        logger.info("Detault trace_id")
    else:
        logger.info("trace_id: " + trace_id)

    #clear_cache()
    logger.info("Start issuer")
    t, res = q_single_trace(trace_id=trace_id)
    logger.info("_measure_ No cached time: " + str(t))


    t_buffer = set()
    iteration = int(os.getenv("ISSUER_COUNT", 5))
    #for i in range(iteration):
    t, res = q_single_trace(trace_id=trace_id)
    logger.info("_measure_ Cached time: " + str(t))
    t_buffer.add(t)
"""
    logger.info("_measure_ breakdown: " + ",".join(map(str, t_buffer)))　#　各実行時間
    logger.info("_measure_ mean: " + str(statistics.mean(t_buffer))) # 平均
    logger.info("_measure_ median: " + str(statistics.median(t_buffer))) #　中央時間
"""

if __name__ == "__main__":
    main()
