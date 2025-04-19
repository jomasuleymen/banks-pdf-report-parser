import os
from banks.bank_report_parser import BankReportParser
from banks.bcc.report import BCCReportParser
from banks.freedom.report import FreedomReportParser
from banks.forte.report import ForteReportParser
from banks.halyk.report import HalykReportParser
from banks.jusan.report import JusanReportParser

from banks.kaspi.report import KaspiReportParser

REPORTS_FOLDER = "reports"


def get_bank_reports_path(account_name, year):
    return os.path.join(REPORTS_FOLDER, account_name, year)


def get_full_path_of_bank_report(account_name, year, bank_name):
    return os.path.join(get_bank_reports_path(account_name, year), bank_name)


def get_bank_report_files(account_name, year):
    bank_report_names = os.listdir(get_bank_reports_path(account_name, year))

    return list(filter(lambda x: x.endswith(".pdf"), bank_report_names))


def get_excel_reports_path(account_name, year):
    return os.path.join(get_bank_reports_path(account_name, year), "excel")


def get_full_path_of_excel_report(account_name, year, bank_name):
    return os.path.join(get_excel_reports_path(account_name, year), bank_name + ".xlsx")


def create_excel_reports_folder(account_name, year):
    excel_reports_folder = get_excel_reports_path(account_name, year)

    if not os.path.exists(excel_reports_folder):
        os.makedirs(excel_reports_folder)

    return excel_reports_folder


if __name__ == "__main__":
    account_name = "kusher"
    year = "2024"

    create_excel_reports_folder(account_name, year)

    bank_report_names = get_bank_report_files(account_name, year)

    for bank_file_name in bank_report_names:
        # get file name without extension
        bank_name = bank_file_name.split(".")[0]

        # if "каспий" in bank_name.lower():
        #     # parse report and save into folder
        #     data = KaspiReportParser.parse_report(
        #         get_full_path_of_bank_report(account_name, year, bank_file_name),
        #         get_full_path_of_excel_report(account_name, year, bank_name),
        #     )

        # if "халык" in bank_name.lower():
        #     # parse report and save into folder
        #     data = HalykReportParser.parse_report(
        #         get_full_path_of_bank_report(account_name, year, bank_file_name),
        #         get_full_path_of_excel_report(account_name, year, bank_name),
        #     )

        # if "форте" in bank_name.lower():
        #     # parse report and save into folder
        #     data = ForteReportParser.parse_report(
        #         get_full_path_of_bank_report(account_name, year, bank_file_name),
        #         get_full_path_of_excel_report(account_name, year, bank_name),
        #     )
        # if "жусан" in bank_name.lower():
        #     # parse report and save into folder
        #     data = JusanReportParser.parse_report(
        #         get_full_path_of_bank_report(account_name, year, bank_file_name),
        #         get_full_path_of_excel_report(account_name, year, bank_name),
        #     )
        if "бцк" in bank_name.lower():
            # parse report and save into folder
            data = BCCReportParser.parse_report(
                get_full_path_of_bank_report(account_name, year, bank_file_name),
                get_full_path_of_excel_report(account_name, year, bank_name),
            )
        # if "фридом" in bank_name.lower():
        #     # parse report and save into folder
        #     data = FreedomReportParser.parse_report(
        #         get_full_path_of_bank_report(account_name, year, bank_file_name),
        #         get_full_path_of_excel_report(account_name, year, bank_name),
        #     )
