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
    def parse_sum_fiat(self, str_data: str):
        splitted = str_data.rsplit(" ", 1)

        sumStr = splitted[0].strip()
        fiat = splitted[1].strip()

        return self.parse_sum(sumStr), fiat

    @classmethod
    def parse_report(self, file_path, dest_path):
        transactions: List[BCCReport] = []

        with pdfplumber.open(file_path) as pdf:
            for page_data in pdf.pages:
                tables = page_data.extract_tables(
                    table_settings={
                        "explicit_vertical_lines": [30, 112, 158, 340, 420, 480, 530, 580],
                    }
                )

                for table in tables:
                    date_processing_idx = None
                    date_carry_out_idx = None
                    # Find the first row with two valid dates and set their indices
                    for row in table:
                        for i in range(len(row)):
                            if date_processing_idx is None:
                                if self.get_date(row[i]):
                                    date_processing_idx = i
                                    continue
                            elif date_carry_out_idx is None and i != date_processing_idx:
                                if self.get_date(row[i]):
                                    date_carry_out_idx = i
                                    break
                        if date_processing_idx is not None and date_carry_out_idx is not None:
                            break
                    # If not found, fallback to default indices
                    if date_processing_idx is None:
                        date_processing_idx = 0
                    if date_carry_out_idx is None:
                        date_carry_out_idx = 1

                    for row in table:
                        # parse date, if date is not valid, then skip this row
                        date_processing = self.get_date(row[date_processing_idx])
                        if not date_processing:
                            continue

                        # parse date, if date is not valid, then skip this row
                        date_carry_out = self.get_date(row[date_carry_out_idx])
                        if not date_carry_out:
                            continue

                        # The rest of the columns are assumed to be in the same order as before
                        # Adjust indices if necessary
                        # We'll build a new row with the correct order for details, sum, etc.
                        # Assume details is the next column after the last date
                        other_indices = [i for i in
                         range(len(row)) if i not in [date_processing_idx, date_carry_out_idx]]
                        details = " ".join((row[other_indices[0]] or "").split())
                        sum, fiat = self.parse_sum_fiat(row[other_indices[1]] or "")
                        sum_in_kzt = self.parse_sum(row[other_indices[2]] or "")
                        comission = self.parse_sum(row[other_indices[3]] or "")
                        cashback = self.parse_sum(row[other_indices[4]] or "")

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
