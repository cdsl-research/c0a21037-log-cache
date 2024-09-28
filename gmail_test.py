from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from apiclient import errors
import base64
import csv

# OAuth2.0 Gmail API用スコープ
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


# アクセストークン取得
def get_token():
    creds = None
    if os.path.exists('creds/token.json'):
        creds = Credentials.from_authorized_user_file('creds/token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('creds/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('creds/token.json', 'w') as token:
            token.write(creds.to_json())
    return creds


# メールリスト取得（すべてのメール）
def get_all_messages(service, user_id, query):
    messages = []
    try:
        next_page_token = None
        while True:
            message_ids = (
                service.users()
                .messages()
                .list(userId=user_id, q=query, pageToken=next_page_token)
                .execute()
            )

            if "messages" not in message_ids:
                break

            for message_id in message_ids["messages"]:
                detail = (
                    service.users()
                    .messages()
                    .get(userId="me", id=message_id["id"])
                    .execute()
                )
                message = {}
                message["id"] = message_id["id"]
                # 本文
                if 'data' in detail['payload']['body']:
                    decoded_bytes = base64.urlsafe_b64decode(detail["payload"]["body"]["data"])
                    decoded_message = decoded_bytes.decode("UTF-8")
                    message["body"] = decoded_message
                else:
                    message["body"] = ""
                # 件名
                message["subject"] = [
                    header["value"]
                    for header in detail["payload"]["headers"]
                    if header["name"] == "Subject"
                ][0]
                # 送信元
                message["from"] = [
                    header["value"]
                    for header in detail["payload"]["headers"]
                    if header["name"] == "From"
                ][0]

                messages.append(message)

            next_page_token = message_ids.get("nextPageToken")
            if not next_page_token:
                break

        return messages

    except errors.HttpError as error:
        print("An error occurred: %s" % error)


# メール1件ごとに個別CSVファイルに出力
def export_messages_to_csv(messages):
    field_names = ['id', 'body', 'subject', 'from']
    for message in messages:
        file_name = f'mails/{message["id"]}.csv'
        with open(file_name, 'w', newline='', encoding='utf8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=field_names)
            writer.writeheader()
            writer.writerow(message)
        print(f'Saved: {file_name}')


# メイン部
def main(query=""):
    creds = get_token()
    service = build('gmail', 'v1', credentials=creds)
    messages = get_all_messages(service, "me", query)

    if messages:
        # メール1件ごとにCSVに出力
        export_messages_to_csv(messages)
    else:
        print("No messages found")


if __name__ == '__main__':
    main()
