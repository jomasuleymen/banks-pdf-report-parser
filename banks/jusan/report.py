import datetime
from typing import List

import pdfplumber
from banks.jusan import JusanReport

from banks.jusan.excel import JusanExcelExporter


class JusanReportParser:
    @classmethod
    def get_date(self, date_str: str):
        if not date_str:
            return None

        # replace all new lines with spaces
        date_str = date_str.replace("\n", " ")

        try:
            if len(date_str.split(" ")) == 1:
                return datetime.datetime.strptime(date_str, "%d.%m.%Y")

            return datetime.datetime.strptime(date_str, "%d.%m.%Y %H:%M:%S")
        except Exception:
            return None

    @classmethod
    def parse_sum(self, str_data: str):
        str_data = str_data.replace(" ", "")
        str_data = str_data.replace(",", ".")
        return float(str_data)

    @classmethod
    def parse_report(self, file_path, dest_path):
        transactions: List[JusanReport] = []

        with pdfplumber.open(file_path) as pdf:
            # image = pdf.pages[0].to_image(resolution=350)
            # image.draw_rects(pdf.pages[0].extract_words(keep_blank_chars=False)).show()
            # print(table)
            for page_data in pdf.pages:
                tables = page_data.extract_tables()

                for table in tables:
                    for row in table:
                        # # if column count is not 4, then skip this row
                        if len(row) != 9 or row[0].strip().find("Дата") != -1:
                            continue

                        # parse date, if date is not valid, then skip this row
                        date_carry_out = self.get_date(row[0])
                        if not date_carry_out:
                            continue

                        # parse date, if date is not valid, then skip this row
                        date_processing = self.get_date(row[1])
                        if not date_processing:
                            continue

                        operation = " ".join(row[2].split())
                        details = " ".join(row[3].split())
                        sum = self.parse_sum(row[5])
                        fiat = row[6].strip()
                        sum_in_fiat = self.parse_sum(row[7])

                        if sum_in_fiat == 0:
                            sum_in_fiat = self.parse_sum(row[8]) * -1

                        trx_data = JusanReport(
                            date_carry_out.date(),
                            date_processing.date(),
                            operation,
                            details,
                            sum,
                            fiat,
                            sum_in_fiat,
                        )
                        transactions.append(trx_data)

        JusanExcelExporter.export_to_excel(transactions, dest_path)
