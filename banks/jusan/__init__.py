import datetime


class JusanReport:
    date_carry_out: datetime.datetime
    date_processing: datetime.datetime
    operation: str
    details: str
    sum: float
    fiat: str
    sum_in_fiat: float

    def __init__(
        self,
        date_carry_out: datetime.datetime,
        date_processing: datetime.datetime,
        operation: str,
        details: str,
        sum: float,
        fiat: str,
        sum_in_fiat: float,
    ):
        self.date_carry_out = date_carry_out
        self.date_processing = date_processing
        self.details = details
        self.sum = sum
        self.fiat = fiat
        self.sum_in_fiat = sum_in_fiat
        self.operation = operation
