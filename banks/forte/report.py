import datetime
from typing import List

import pdfplumber
from banks.forte import ForteReport

from banks.forte.excel import ForteExcelExporter


class ForteReportParser:
    @classmethod
    def get_date(self, date_str):
        try:
            date = datetime.datetime.strptime(date_str, "%d.%m.%Y")
            return date
        except Exception:
            return None

    @classmethod
    def parse_sum(self, str_data: str):
        sumStr = str_data.split(" ", 1)[0].strip()
        fiat = str_data.split(" ")[1].strip()

        sumStr = sumStr.replace(",", ".")
        return float(sumStr), fiat

    @classmethod
    def parse_report(self, file_path, dest_path):
        transactions: List[ForteReport] = []

        with pdfplumber.open(file_path) as pdf:
            for page_data in pdf.pages:
                tables = page_data.extract_tables()

                for table in tables:
                    for row in table:
                        trx_data: ForteReport = ForteReport()

                        # if column count is not 4, then skip this row
                        if len(row) != 4:
                            continue

                        # parse date, if date is not valid, then skip this row
                        date = self.get_date(row[0])
                        if not date:
                            continue

                        # parse sum, if sum is not valid, then skip this row
                        sum, fiat = self.parse_sum(row[1])
                        if not sum:
                            print("sum is None", row)
                            continue

                        trx_data.date = date.date()
                        trx_data.sum = sum
                        trx_data.fiat = fiat
                        trx_data.operation = row[2]
                        trx_data.details = row[3]

                        transactions.append(trx_data)

        ForteExcelExporter.export_to_excel(transactions, dest_path)
