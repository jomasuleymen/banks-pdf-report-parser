import datetime
from typing import List

import pdfplumber
from banks.bcc import BCCReport

from banks.bcc.excel import BCCExcelExporter


class BCCReportParser:
    @classmethod
    def get_date(self, date_str: str):
        if not date_str:
            return None

        # replace all new lines with spaces
        date_str = date_str.replace("\n", " ")

        try:
            if len(date_str.split(" ")) == 1:
                return datetime.datetime.strptime(date_str, "%d.%m.%Y").date()

            return datetime.datetime.strptime(date_str, "%d.%m.%Y %H:%M:%S")
        except Exception:
            return None

    @classmethod
    def parse_num(self, str_data: str):
        str_data = str_data.replace(" ", "")
        str_data = str_data.replace(",", ".")
        str_data = str_data.replace("\n", "")

        return float(str_data)

    @classmethod
    def parse_sum_fiat(self, str_data: str):
        splitted = str_data.rsplit(" ", 1)

        sumStr = splitted[0].strip()
        fiat = splitted[1].strip()

        sumStr = sumStr.replace(" ", "")
        sumStr = sumStr.replace(",", ".")
        return float(sumStr), fiat

    @classmethod
    def parse_report(self, file_path, dest_path):
        transactions: List[BCCReport] = []

        with pdfplumber.open(file_path) as pdf:
            for page_data in pdf.pages:
                tables = page_data.extract_tables(
                    table_settings={
                        "explicit_vertical_lines": [
                            30,
                            110,
                            154,
                            367,
                            440,
                            495,
                            550,
                            590,
                        ],
                    }
                )

                for table in tables:
                    for row in table:
                        # # if column count is not 4, then skip this row
                        if len(row) != 7:
                            continue

                        # parse date, if date is not valid, then skip this row
                        date_processing = self.get_date(row[0])
                        if not date_processing:
                            continue

                        # parse date, if date is not valid, then skip this row
                        date_carry_out = self.get_date(row[1])
                        if not date_carry_out:
                            continue

                        details = " ".join(row[2].split())
                        sum, fiat = self.parse_sum_fiat(row[3])
                        sum_in_kzt = self.parse_num(row[4])
                        comission = self.parse_num(row[5])
                        cashback = self.parse_num(row[6])

                        trx_data = BCCReport(
                            date_processing=date_processing,
                            date_carry_out=date_carry_out,
                            details=details,
                            sum=sum,
                            fiat=fiat,
                            sum_in_kzt=sum_in_kzt,
                            comission=comission,
                            cashback=cashback,
                        )
                        transactions.append(trx_data)

        BCCExcelExporter.export_to_excel(transactions, dest_path)
