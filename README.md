# log-cache

出来ること：Gmailをの送信時間からElasticsearchのtimestampを使った検索クエリを作成します．作成された検索クエリはnewquery.pyとして出力されます

## 事前にやること
test.txtというディレクトリを作り，gmailの全文（送信時間なども含める）をそのままコピーして貼ってください

## 実行するコマンド
```
python3 teian.py
```

## 各ファイルの説明
- query.txt:検索クエリのテンプレートを保存しています
- teian.py：test.txtから送信時間を抽出し，gteとltの値を求め，反映したファイルをnew.txtとして生成します
- kensaku.py：new.txtを使ってElasticsearchに検索をかけます
- search-v4-collect-cache-size.py：余計なキャッシュを削除します
- collect_es_cache_size.py：search-v4-collect-cache-size.pyを実行するときに使用します

## 実行結果
※長いので3枚に分けています

<img width="953" alt="image" src="https://github.com/user-attachments/assets/3f089a2a-5b5b-44a6-963e-6b581a704cb1">

<img width="950" alt="image" src="https://github.com/user-attachments/assets/dadc83b9-1adc-44e8-9b7d-082bc108b0a2">

<img width="947" alt="image" src="https://github.com/user-attachments/assets/7a7512e2-96a5-4104-8c64-81b6a8822678">
