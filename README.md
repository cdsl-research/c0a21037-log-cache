# c0a21037-gmail

出来ること；Gmailをの送信時間からElasticsearchのtimestampを使った検索クエリを作成します

## 事前にやること
test.txtというディレクトリを作り，gmailの全文（送信時間なども含める）をそのままコピーして貼ってください

## 実行するコマンド
```
python3 teian.py
```

## 各ファイルの説明
・query.txt:検索クエリのテンプレートを保存しています
・teian.py：test.txtから送信時間を抽出し，gteとltの値を求め，反映したファイルをnew.txtとして生成します
・kensaku.py：new.txtを使ってElasticsearchに検索をかけます
・search-v4-collect-cache-size.py：余計なキャッシュを削除します
・collect_es_cache_size.py：search-v4-collect-cache-size.pyを実行するときに使用します

