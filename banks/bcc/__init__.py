import datetime


class BCCReport:
    date_processing: datetime.datetime
    date_carry_out: datetime.datetime
    details: str
    sum: float
    fiat: str
    sum_in_kzt: float
    comission: float
    cashback: float

    def __init__(
        self,
        date_processing: datetime.datetime,
        date_carry_out: datetime.datetime,
        details: str,
        sum: float,
        fiat: str,
        sum_in_kzt: float,
        comission: float,
        cashback: float,
    ):
        self.date_processing = date_processing
        self.date_carry_out = date_carry_out
        self.details = details
        self.sum = sum
        self.fiat = fiat
        self.sum_in_kzt = sum_in_kzt
        self.comission = comission
        self.cashback = cashback