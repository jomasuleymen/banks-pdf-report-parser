import datetime


class HalykReport:
    date_carry_out: datetime.datetime
    date_processing: datetime.datetime
    details: str
    sum: float
    fiat: str
    income: float
    expense: float
    comission: float
    card_number: str

    def __init__(
        self,
        date_carry_out: datetime.datetime,
        date_processing: datetime.datetime,
        details: str,
        sum: float,
        fiat: str,
        income: float,
        expense: float,
        comission: float,
        card_number: str,
    ):
        self.date_carry_out = date_carry_out
        self.date_processing = date_processing
        self.details = details
        self.sum = sum
        self.fiat = fiat
        self.income = income
        self.expense = expense
        self.comission = comission
        self.card_number = card_number
