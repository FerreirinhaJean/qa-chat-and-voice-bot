import streamlit as st
from documents.ProcessorDocument import ProcessorDocument


class LoadDocument:

    def __init__(self):
        self.__processor_document = ProcessorDocument()

    def render(self) -> None:
        upload_file = st.file_uploader("Choose a file", type="pdf")
        if upload_file is not None:
            bytes_data = upload_file.getvalue()
            result = self.__processor_document.analyze_document(bytes_data)
            text = self.__processor_document.format_text_extracted(result)

            st.text(text)


if __name__ == "__main__":
    LoadDocument().render()
