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
```
2024/10/31 18:05
2024-10-31T18:05:00
{
    "query": {
        "range": {
            "@timestamp": {
                "gte": "gte2",
                "lt": "lt2"
            }
        }
    }
}


1つ目の検索結果: 19 件
{'input': {'type': 'container'}, 'host': {'name': 'fb-filebeat-kjt6q'}, 'message': '10.42.0.1 - - [31/Oct/2024:09:16:08 +0000] "GET /aaa HTTP/1.1" 404 284140 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"', 'ecs': {'version': '8.0.0'}, '@version': '1', 'stream': 'stdout', 'tags': ['beats_input_codec_plain_applied'], '@timestamp': '2024-10-31T09:16:08.118Z', 'kubernetes': {'replicaset': {'name': 'wordpress-6f9795b567'}, 'namespace_uid': 'd3632d21-196d-4b00-8f77-5404e387c02a', 'node': {'name': 'test-wordpress', 'labels': {'beta_kubernetes_io/arch': 'amd64', 'node-role_kubernetes_io/master': 'true', 'beta_kubernetes_io/instance-type': 'k3s', 'kubernetes_io/hostname': 'test-wordpress', 'kubernetes_io/arch': 'amd64', 'node-role_kubernetes_io/control-plane': 'true', 'node_kubernetes_io/instance-type': 'k3s', 'kubernetes_io/os': 'linux', 'beta_kubernetes_io/os': 'linux'}, 'uid': '146900e9-3430-4ccb-b72b-9462a6f47ba3', 'hostname': 'test-wordpress'}, 'namespace': 'wp', 'pod': {'ip': '10.42.0.78', 'uid': '341c86d0-a6dd-4779-8bd9-db249fd0b48a', 'name': 'wordpress-6f9795b567-bhwj4'}, 'container': {'name': 'wordpress'}, 'namespace_labels': {'kubernetes_io/metadata_name': 'wp'}, 'deployment': {'name': 'wordpress'}, 'labels': {'pod-template-hash': '6f9795b567', 'tier': 'frontend', 'app': 'wordpress'}}, 'container': {'image': {'name': 'wordpress:6.2.1-apache'}, 'runtime': 'containerd', 'id': '0ef85d84a1b96fc41de0ba85d6af143e367d4a8f2939785e12f0557d2c5dfdef'}, 'agent': {'name': 'fb-filebeat-kjt6q', 'ephemeral_id': '3d84c70c-9518-4ed1-b48f-ea15e6d9a8e0', 'id': 'fd876e74-a4ee-4603-8640-613c3a71ac6e', 'version': '8.5.1', 'type': 'filebeat'}, 'event': {'original': '10.42.0.1 - - [31/Oct/2024:09:16:08 +0000] "GET /aaa HTTP/1.1" 404 284140 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"'}, 'log': {'file': {'path': '/var/log/containers/wordpress-6f9795b567-bhwj4_wp_wordpress-0ef85d84a1b96fc41de0ba85d6af143e367d4a8f2939785e12f0557d2c5dfdef.log'}, 'offset': 91234}, 'fields': {'index': 'logstash'}}
wp
2024-10-31T09:16:08.118Z
2つ目の検索結果: 10000 件
{'input': {'type': 'container'}, 'host': {'name': 'fb-filebeat-kjt6q'}, 'message': '10.42.0.1 - - [31/Oct/2024:09:15:58 +0000] "POST /wp-admin/admin-ajax.php HTTP/1.1" 200 582 "http://192.168.100.58:30590/wp-admin/post.php?post=8&action=edit" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"', 'ecs': {'version': '8.0.0'}, '@version': '1', 'stream': 'stdout', 'tags': ['beats_input_codec_plain_applied'], '@timestamp': '2024-10-31T09:15:58.175Z', 'kubernetes': {'replicaset': {'name': 'wordpress-6f9795b567'}, 'namespace_uid': 'd3632d21-196d-4b00-8f77-5404e387c02a', 'node': {'labels': {'beta_kubernetes_io/arch': 'amd64', 'beta_kubernetes_io/instance-type': 'k3s', 'node-role_kubernetes_io/master': 'true', 'node_kubernetes_io/instance-type': 'k3s', 'node-role_kubernetes_io/control-plane': 'true', 'kubernetes_io/arch': 'amd64', 'kubernetes_io/hostname': 'test-wordpress', 'beta_kubernetes_io/os': 'linux', 'kubernetes_io/os': 'linux'}, 'hostname': 'test-wordpress', 'uid': '146900e9-3430-4ccb-b72b-9462a6f47ba3', 'name': 'test-wordpress'}, 'namespace': 'wp', 'pod': {'ip': '10.42.0.80', 'uid': '479546b2-3f71-4aaf-b592-089559fa3575', 'name': 'wordpress-6f9795b567-g8h4b'}, 'container': {'name': 'wordpress'}, 'namespace_labels': {'kubernetes_io/metadata_name': 'wp'}, 'deployment': {'name': 'wordpress'}, 'labels': {'pod-template-hash': '6f9795b567', 'tier': 'frontend', 'app': 'wordpress'}}, 'container': {'image': {'name': 'wordpress:6.2.1-apache'}, 'runtime': 'containerd', 'id': '548a570ca5960b162f27547823679d6ae62cd773c02a02f25033347abee52ae2'}, 'fields': {'index': 'logstash'}, 'event': {'original': '10.42.0.1 - - [31/Oct/2024:09:15:58 +0000] "POST /wp-admin/admin-ajax.php HTTP/1.1" 200 582 "http://192.168.100.58:30590/wp-admin/post.php?post=8&action=edit" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"'}, 'log': {'file': {'path': '/var/log/containers/wordpress-6f9795b567-g8h4b_wp_wordpress-548a570ca5960b162f27547823679d6ae62cd773c02a02f25033347abee52ae2.log'}, 'offset': 125747}, 'agent': {'type': 'filebeat', 'ephemeral_id': '3d84c70c-9518-4ed1-b48f-ea15e6d9a8e0', 'id': 'fd876e74-a4ee-4603-8640-613c3a71ac6e', 'version': '8.5.1', 'name': 'fb-filebeat-kjt6q'}}
2024-10-31T09:15:58.175Z
2024-10-31T18:15:58.175Z
2024-10-31T18:16:08.118Z
2024-11-19 09:54:57,412 INFO __main__ : Query_cache: {"elasticsearch-master-0": {"memory_size_in_bytes": 1768923, "total_count": 1112800, "hit_count": 29939, "miss_count": 1082861, "cache_size": 57, "cache_count": 1157, "evictions": 1100}, "elasticsearch-master-2": {"memory_size_in_bytes": 1725584, "total_count": 3346463, "hit_count": 106147, "miss_count": 3240316, "cache_size": 57, "cache_count": 317, "evictions": 260}, "elasticsearch-master-1": {"memory_size_in_bytes": 0, "total_count": 129, "hit_count": 0, "miss_count": 129, "cache_size": 0, "cache_count": 0, "evictions": 0}}
2024-11-19 09:54:57,412 INFO __main__ : Start clear_cache()
2024-11-19 09:54:57,422 INFO elastic_transport.transport : POST http://ls-master:31410/_cache/clear?fielddata=true&query=true&request=true [status:200 duration:0.010s]
2024-11-19 09:54:57,422 INFO __main__ : Finish clear_cache_result {'_shards': {'total': 6, 'successful': 6, 'failed': 0}}
2024-11-19 09:54:57,427 INFO __main__ : Query_cache: {"elasticsearch-master-0": {"memory_size_in_bytes": 1768923, "total_count": 1112800, "hit_count": 29939, "miss_count": 1082861, "cache_size": 57, "cache_count": 1157, "evictions": 1100}, "elasticsearch-master-2": {"memory_size_in_bytes": 1725584, "total_count": 3346463, "hit_count": 106147, "miss_count": 3240316, "cache_size": 57, "cache_count": 317, "evictions": 260}, "elasticsearch-master-1": {"memory_size_in_bytes": 0, "total_count": 129, "hit_count": 0, "miss_count": 129, "cache_size": 0, "cache_count": 0, "evictions": 0}}
2024-11-19 09:54:57,427 INFO __main__ : Query_cache_sub: {"elasticsearch-master-0": {"memory_size_in_bytes": -1701400, "total_count": 0, "hit_count": 0, "miss_count": 0, "cache_size": -55, "cache_count": 0, "evictions": 55}, "elasticsearch-master-2": {"memory_size_in_bytes": -1701400, "total_count": 0, "hit_count": 0, "miss_count": 0, "cache_size": -55, "cache_count": 0, "evictions": 55}, "elasticsearch-master-1": {"memory_size_in_bytes": 0, "total_count": 0, "hit_count": 0, "miss_count": 0, "cache_size": 0, "cache_count": 0, "evictions": 0}}
2024-11-19 09:54:57,427 INFO __main__ : Start q_trace_list_prop()
2024-11-19 09:54:57,428 INFO __main__ : unix_time=1714995420000000
2024-11-19 09:54:57,430 INFO elastic_transport.transport : POST http://ls-master:31410/l*/_search [status:200 duration:0.002s]
2024-11-19 09:54:57,430 INFO __main__ : Found: {'value': 0, 'relation': 'eq'}
2024-11-19 09:54:57,430 INFO __main__ : Response_size: 2
2024-11-19 09:55:00,445 INFO __main__ : Query_cache: {"elasticsearch-master-0": {"memory_size_in_bytes": 1768923, "total_count": 1112800, "hit_count": 29939, "miss_count": 1082861, "cache_size": 57, "cache_count": 1157, "evictions": 1100}, "elasticsearch-master-2": {"memory_size_in_bytes": 1725584, "total_count": 3346463, "hit_count": 106147, "miss_count": 3240316, "cache_size": 57, "cache_count": 317, "evictions": 260}, "elasticsearch-master-1": {"memory_size_in_bytes": 0, "total_count": 129, "hit_count": 0, "miss_count": 129, "cache_size": 0, "cache_count": 0, "evictions": 0}}
2024-11-19 09:55:00,446 INFO __main__ : Query_cache_sub: {"elasticsearch-master-2": {"memory_size_in_bytes": 0, "total_count": 136, "hit_count": 0, "miss_count": 136, "cache_size": 0, "cache_count": 0, "evictions": 0}, "elasticsearch-master-1": {"memory_size_in_bytes": 0, "total_count": 0, "hit_count": 0, "miss_count": 0, "cache_size": 0, "cache_count": 0, "evictions": 0}, "elasticsearch-master-0": {"memory_size_in_bytes": 0, "total_count": 274, "hit_count": 8, "miss_count": 266, "cache_size": 0, "cache_count": 0, "evictions": 0}}
```

