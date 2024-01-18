import datetime
from typing import List

import pdfplumber
from banks.halyk import HalykReport

from banks.halyk.excel import HalykExcelExporter


class HalykReportParser:
    @classmethod
    def get_date(self, date_str: str):
        date_str = date_str.strip()

        try:
            date = datetime.datetime.strptime(date_str, "%d.%m.%Y")
            return date
        except Exception:
            return None

    @classmethod
    def parse_sum(self, str_data: str):
        str_data = str_data.replace(" ", "")
        str_data = str_data.replace(",", ".")
        return float(str_data)

    @classmethod
    def parse_report(self, file_path, dest_path):
        transactions: List[HalykReport] = []

        with pdfplumber.open(file_path) as pdf:
            # image = pdf.pages[0].to_image(resolution=350)
            # image.draw_rects(pdf.pages[0].extract_words(keep_blank_chars=False)).show()
            # print(table)
            for page_data in pdf.pages:
                tables = page_data.extract_tables()

                for table in tables:
                    for row in table:
                        # # if column count is not 4, then skip this row
                        # if len(row) != 9:
                        #     continue

                        # parse date, if date is not valid, then skip this row
                        date_carry_out = self.get_date(row[0])
                        if not date_carry_out:
                            continue

                        # parse date, if date is not valid, then skip this row
                        date_processing = self.get_date(row[1])
                        if not date_processing:
                            continue

                        details = " ".join(row[2].split())
                        sum = self.parse_sum(row[3])
                        fiat = row[4].strip()
                        income = self.parse_sum(row[5])
                        expense = self.parse_sum(row[6])
                        comission = self.parse_sum(row[7])
                        card_number = " ".join(row[8].split()).strip()

                        trx_data = HalykReport(
                            date_carry_out.date(),
                            date_processing.date(),
                            details,
                            sum,
                            fiat,
                            income,
                            expense,
                            comission,
                            card_number,
                        )
                        transactions.append(trx_data)

        HalykExcelExporter.export_to_excel(transactions, dest_path)
