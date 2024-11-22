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
1/3枚目
<img width="949" alt="image" src="https://github.com/user-attachments/assets/fd6a33da-a959-4d40-bd72-a3063e73e0ae">
2/3枚目
<img width="950" alt="image" src="https://github.com/user-attachments/assets/dadc83b9-1adc-44e8-9b7d-082bc108b0a2">
3/3枚目
<img width="946" alt="image" src="https://github.com/user-attachments/assets/ad7aca80-56d0-4d7e-9bb1-765a4291a346">

