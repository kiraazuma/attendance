import streamlit as st

st.title("出欠確認アプリ")
name = st.text_input("名前を入力してください")

if st.button("出席"):
    st.success(f"{name} さんの出席を記録しました！")
  
