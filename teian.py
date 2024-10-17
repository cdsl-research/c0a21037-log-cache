from datetime import datetime #日付の変換
from elasticsearch import Elasticsearch
import subprocess
file_path = 'mail/test.txt'  # 読み込むファイルのパス

with open(file_path, 'r', encoding='utf-8') as file:
    content = file.read()  # ファイルの各行をリストとして読み込む
    content = content.split()

# 読み込んだ内容を確認
print(content[4],content[5])

day = content[4] +" "+content[5]

day = "2019年12月6日 9:20" #テスト用

# 日本語形式の日付をパースして datetime オブジェクトに変換
day_date = datetime.strptime(day, '%Y年%m月%d日 %H:%M')

# ISO 8601 形式に変換
iso_date = day_date.strftime('%Y-%m-%dT%H:%M:%S')

# 出力
print(iso_date)

with open("query.txt",'r', encoding='utf-8') as file:
    content = file.read()

print(content)

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
                        "Uri.keyword": uri
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
gte = response2['hits']['hits'][0]['_source']['TimeStamp'] if response2['hits']['total']['value'] > 0 else ""

print(gte)

recontent = content.replace('gte2',gte)
recontent = recontent.replace('lt2', lt)

with open("new.txt", 'w', encoding='utf-8') as file:
            file.write(recontent)

subprocess.run(["python3", "search-v4-collect-cache-size.py"])
subprocess.run(["python3", "c.py"])
