import datetime
from typing import List

import pdfplumber
from banks.freedom import FreedomReport

from banks.freedom.excel import FreedomExcelExporter


class FreedomReportParser:
    @classmethod
    def get_date(self, date_str):
        try:
            # 02.10.2024
            date = datetime.datetime.strptime(date_str, "%d.%m.%Y")
            return date
        except Exception:
            return None

    @classmethod
    def parse_sum(self, str_data: str):
        # Keep only digits, commas, dots, and minus sign (only if at the start)
        str_data = str_data.strip()
        negative = str_data.startswith('-')
        # Remove all characters except digits, commas, and dots
        cleaned = ''.join(c for c in str_data if c.isdigit() or c in [',', '.'])
        cleaned = cleaned.replace(',', '.')
        if negative:
            cleaned = '-' + cleaned
        try:
            return float(cleaned)
        except ValueError:
            return 0.0

    @classmethod
    def parse_report(self, file_path, dest_path):
        transactions: List[FreedomReport] = []

        with pdfplumber.open(file_path) as pdf:
            for page_data in pdf.pages:
                table = page_data.extract_table()
                # print(table)
                if not table:
                    continue
                for row in table:
                    trx_data: FreedomReport = FreedomReport()

                    # if column count is not 4, then skip this row
                    if len(row) < 7:
                        continue

                    # parse date, if date is not valid, then skip this row
                    date = self.get_date(row[0])
                    if not date:
                        print(date)
                        continue

                    # parse sum, if sum is not valid, then skip this row
                    income = self.parse_sum(row[7])
                    outcome = self.parse_sum(row[8])

                    trx_data.date = date.date()
                    trx_data.doc_number = row[1]
                    trx_data.receiver_bank_name = row[2]
                    trx_data.receiver_bank_bic = row[3]
                    trx_data.sender_bank_name = row[4]
                    trx_data.sender_bank_bic = row[5]
                    trx_data.sender_account = row[6]
                    trx_data.sum = income if income > 0 else -outcome
                    trx_data.details = row[9]

                    transactions.append(trx_data)

        FreedomExcelExporter.export_to_excel(transactions, dest_path)
