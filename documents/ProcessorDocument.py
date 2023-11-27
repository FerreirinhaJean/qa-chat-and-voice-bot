from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
import os
from dotenv import load_dotenv
from shapely.geometry import Polygon
import re


class ProcessorDocument:

    def __init__(self):
        load_dotenv()
        self.__endpoint = os.getenv("FORM_RECOGNIZER_ENDPOINT")
        self.__api_key = os.getenv("FORM_RECOGNIZER_KEY")

    def analyze_document(self, bytes_data):
        document_analysis_client = DocumentAnalysisClient(
            endpoint=self.__endpoint, credential=AzureKeyCredential(self.__api_key)
        )
        poller = document_analysis_client.begin_analyze_document("prebuilt-document", bytes_data, pages="1-2")
        result = poller.result()

        return result

    def format_text_extracted(self, document_analyze, number_part):
        body_value = ""

        for page in document_analyze.pages:
            if number_part == 0:
                for table in document_analyze.tables:
                    table_value = self.__get_table_values(table)

                    bounding_regions = table.bounding_regions[0]
                    polygon_table = bounding_regions.polygon

                    for line in page.lines:
                        if self.__has_overlap(polygon_table, line.polygon):
                            continue

                        body_value += f"{line.content}\n"

                        if re.search(r"^Cronograma\s+abaixo:$", line.content, flags=re.I | re.M):
                            body_value += f"\n{table_value}\n\n"

                continue

            for line in page.lines:
                body_value += f"{line.content}\n"

        return f"{body_value}"

    def __get_table_values(self, table):
        registration_date_test = ""
        location_test = ""
        selections_methods = ""

        for cell in table.cells:
            column_index = cell.column_index
            row_index = cell.row_index

            if column_index is None or cell.content is None:
                continue

            if column_index == 0 and row_index > 0:
                registration_date_test += f"Período de inscrição: {cell.content}, "

            if column_index == 1 and row_index > 0:
                registration_date_test += f"Dia e horário da Prova de Proficiência em Língua Portuguesa (Redação): {cell.content}\n"

            if column_index == 2:
                if row_index == 0:
                    location_test += f"{cell.content}:\n"
                else:
                    location_test += cell.content

            if column_index == 3:
                if row_index == 0:
                    selections_methods += f"{cell.content}:\n"
                else:
                    selections_methods += f"{cell.content} "

        table_text = f"{registration_date_test}\n{location_test}\n\n{selections_methods}"

        return table_text

    def __has_overlap(self, polygon_table, polygon_line):
        table = Polygon(polygon_table)
        line = Polygon(polygon_line)

        return table.intersects(line)
