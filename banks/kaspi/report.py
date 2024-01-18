import datetime
from typing import List

import pdfplumber
from banks.kaspi import KaspiReport

from banks.kaspi.excel import KaspiExcelExporter


class KaspiReportParser:
    @classmethod
    def get_date(self, date_str):
        try:
            date = datetime.datetime.strptime(date_str, "%d.%m.%y")
            return date
        except Exception:
            return None

    @classmethod
    def parse_sum(self, str_data):
        currency_index = str_data.find("₸")

        if currency_index != -1:
            str_data = str_data[:currency_index]
        else:
            return None

        str_data = str_data.replace(" ", "")
        str_data = str_data.replace(",", ".")
        return float(str_data)

    @classmethod
    def parse_report(self, file_path, dest_path):
        transactions: List[KaspiReport] = []

        with pdfplumber.open(file_path) as pdf:
            for page_data in pdf.pages:
                table = page_data.extract_table()

                for row in table:
                    trx_data: KaspiReport = KaspiReport()

                    # if column count is not 4, then skip this row
                    if len(row) != 4:
                        continue

                    # parse date, if date is not valid, then skip this row
                    date = self.get_date(row[0])
                    if not date:
                        continue

                    # parse sum, if sum is not valid, then skip this row
                    sum = self.parse_sum(row[1])
                    if not sum:
                        print("sum is None", row)
                        continue

                    trx_data.date = date.date()
                    trx_data.sum = sum
                    trx_data.operation = row[2]
                    trx_data.details = row[3]

                    transactions.append(trx_data)

        KaspiExcelExporter.export_to_excel(transactions, dest_path)
