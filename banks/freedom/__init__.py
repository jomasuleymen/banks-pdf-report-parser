import datetime


class FreedomReport:
    date: datetime.datetime
    doc_number: str
    receiver_bank_name: str
    receiver_bank_bic: str
    sender_bank_name: str
    sender_bank_bic: str
    sender_account: str
    sum: float
    details: str
