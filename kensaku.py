from datetime import datetime
from elasticsearch import Elasticsearch

# Elasticsearchに接続
es = Elasticsearch(['http://10.43.253.171:9200'])  # Elasticsearchのホストとポートを指定

# 検索したいタイムスタンプを設定（ISO 8601形式）
timestamp = '2019-12-06T09:20:00'  # ここに任意のタイムスタンプを指定

# 1つ目の検索クエリを定義
query1 = {
    "query": {
        "bool": {
            "must": {
                "range": {
                    "TimeStamp": {
                        "lt": timestamp
                    }
                }
            },
            "must_not": {
                "range": {
                    "ResponseCode": {
                        "gte": 200,
                        "lt": 400
                    }
                }
            }
        }
    },
    "sort": [
        {
            "@timestamp": {
                "order": "desc"
            }
        }
    ],
    "size": 1
}

# 1つ目のクエリを実行
index_name = 'logstash-2024.09.16'  # 検索するインデックス名を指定
response1 = es.search(index=index_name, body=query1)

# 1つ目の検索結果を出力
if response1['hits']['total']['value'] > 0:
    print(f"1つ目の検索結果: {response1['hits']['total']['value']} 件")
    for hit in response1['hits']['hits']:
        print(hit['_source'])  # 各ヒットのソースデータを表示
else:
    print("1つ目の検索結果はありません。")

# URIを取得
uri = response1['hits']['hits'][0]['_source']['Uri'] if response1['hits']['total']['value'] > 0 else ""
lt = response1['hits']['hits'][0]['_source']['TimeStamp'] if response1['hits']['total']['value'] > 0 else ""
print(uri)
print(lt)
# 2つ目の検索クエリを定義
query2 = {
    "query": {
        "bool": {
            "must": [
                {
                    "range": {
                        "TimeStamp": {
                            "lt": timestamp
                        }
                    }
                },
                {
                    "term": {
                        "ResponseCode": 200
                    }
                },
                {
                    "term": {
                        "Uri": uri
                    }
                }
            ]
        }
    },
    "sort": [
        {
            "@timestamp": {
                "order": "desc"
            }
        }
    ],
    "size": 1
}

# 2つ目のクエリを実行
response2 = es.search(index=index_name, body=query2)

# 2つ目の検索結果を出力
if response2['hits']['total']['value'] > 0:
    print(f"2つ目の検索結果: {response2['hits']['total']['value']} 件")
    for hit in response2['hits']['hits']:
        print(hit['_source'])  # 各ヒットのソースデータを表示
else:
    print("2つ目の検索結果はありません。")
