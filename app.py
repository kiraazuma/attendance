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
spreadsheet = client.open("講演会受付")
sheet = spreadsheet.sheet1

# Streamlit UI
st.title("講演会受付")

name = st.text_input("名前を入力してください")

if st.button("受付する"):
    records = sheet.get_all_records()
    found = False
    for i, row in enumerate(records):
        if row["名前"] == name:
            if row["受付済み"] == True:
                st.warning("すでに受付済みです")
            else:
                sheet.update_cell(i+2, 2, "TRUE")  # 行、列
                st.success("受付が完了しました！")
            found = True
            break
    if not found:
        st.error("名前が見つかりませんでした")
