import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json

# API認証（環境変数またはローカルのcredentials.jsonを読み込み）
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_dict = json.loads(os.environ["GOOGLE_CREDS"])  # Streamlit Cloud用
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# スプレッドシートに接続
spreadsheet = client.open_by_key("1uNk3bJIIMtXOy2hrZoGOmMk6wc9lLK8yYuRCg9M69Lo")
sheet = spreadsheet.sheet1

# Streamlit UI
st.title("講演会受付")

name = st.text_input("名前を全角ひらがなスペースなしで入力してください")

if st.button("受付する"):
    records = sheet.get_all_records()
    found = False
    for i, row in enumerate(records):
        if row["名前"] == name:
            found = True
            if str(row["受付済み"]).upper() == "TRUE":
                st.warning("すでに登録されています")
            else:
                sheet.update_cell(i+2, 2, "TRUE")
                st.success("受付が完了しました！")
            break
    if not found:
        st.error("名前が見つかりませんでした")
