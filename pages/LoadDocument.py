import streamlit as st
from documents.ProcessorDocument import ProcessorDocument
import PyPDF2
import io
import os


class LoadDocument:

    def __init__(self):
        self.__processor_document = ProcessorDocument()

    def render(self) -> None:
        upload_file = st.file_uploader("Choose a file", type="pdf")
        if upload_file is not None:
            bytes_data = upload_file.getvalue()

            self.__clear_temp_path("documents/temp_files/")
            self.__split_pdf(bytes_data, "documents/temp_files/output", 2)

            pdfs_bytes = self.__pdf_to_bytes("documents/temp_files/")
            text = ""

            for index, pdf in enumerate(pdfs_bytes):
                result = self.__processor_document.analyze_document(pdf)
                text += self.__processor_document.format_text_extracted(result, index)

            st.text(text)

    def __split_pdf(self, pdf_file, output_path, number_pages):
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_file))
        total_pages = len(pdf_reader.pages)

        for i in range(0, total_pages, number_pages):
            pdf_writer = PyPDF2.PdfFileWriter()
            initial_part = i
            final_part = min(i + number_pages, total_pages)

            for page in range(initial_part, final_part):
                pdf_writer.addPage(pdf_reader.getPage(page))

            output_filename = f"{output_path}_parte_{i // number_pages + 1}.pdf"
            with open(output_filename, 'wb') as output_file:
                pdf_writer.write(output_file)

    def __clear_temp_path(self, path):
        files = os.listdir(path)

        for file in files:
            file_path = os.path.join(path, file)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    # print(f"Arquivo {file} excluído com sucesso.")
            except Exception as e:
                print(f"Erro ao excluir o arquivo {file}: {e}")

    def __pdf_to_bytes(self, path):
        files = os.listdir(path)
        list_bytes_data = list()

        for file in files:
            file_path = os.path.join(path, file)
            with open(file_path, "rb") as pdf_file:
                pdf_bytes = pdf_file.read()
                list_bytes_data.append(pdf_bytes)

        return list_bytes_data


if __name__ == "__main__":
    LoadDocument().render()
