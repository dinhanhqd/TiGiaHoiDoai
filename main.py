import os
import streamlit as st


def main():
    st.set_page_config(layout="wide")  # Thiết lập trang Streamlit để có giao diện rộng
    st.page_link("pages/page_1.py", label="Page 1", icon="1️⃣")

if __name__ == "__main__":
    main()