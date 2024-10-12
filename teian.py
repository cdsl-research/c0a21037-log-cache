import MeCab
import neologdn
import re

# MeCabの設定
mecab = MeCab.Tagger('-Owakati -d /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd')

# 日時パターンを正規表現で結合
def combine_datetime(text):
    # YYYY年MM月DD日 HH:MM の形式を一つのトークンにまとめる
    datetime_pattern = r'(\d{4}年\d{1,2}月\d{1,2}日)\s*(\d{1,2}):(\d{2})'
    # 一致した部分をまとめて処理（空白を取り除いて結合）
    combined_text = re.sub(datetime_pattern, r'\1\2:\3', text)
    return combined_text

# ファイルを読み込む
file_path = 'mail/test.txt'  # 読み込むファイルのパス

with open(file_path, 'r', encoding='utf-8') as file:
    content = file.read()

# テキストを正規化
normalized_content = neologdn.normalize(content)

# 日時を一つの単語として結合
combined_content = combine_datetime(normalized_content)

# 文節ごとにリストに分割する関数
def get_bunsetu_list(text):
    parsed_text = mecab.parse(text)
    # 文節ごとにリスト化
    bunsetsu_list = parsed_text.strip().split()
    return bunsetsu_list

# 結合後のテキストを文節ごとに分割してリスト化
bunsetu_list = get_bunsetu_list(combined_content)

# 結果を出力
print(bunsetu_list)
