import streamlit as st
from st_pages import Page, add_page_title, show_pages


class App:

    def __init__(self):
        show_pages(
            [
                Page("./pages/LoadDocument.py", "Load Documents", "📚"),
                Page("./pages/Voicebot.py", "Voicebot", "🎙️"),
            ]
        )

    def render(self) -> None:
        try:
            st.set_page_config(layout="wide")
        except:
            pass
        add_page_title()
        st.info("Select the section you want to start!")


if __name__ == "__main__":
    App().render()
