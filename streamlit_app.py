import streamlit as st
from scraper import get_heuristics

def my_app():
    url = st.text_input('Enter URL')
    if url:
        st.write(get_heuristics(url))
           

if __name__ == "__main__":
    my_app()