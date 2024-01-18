class BankReportParser:
	def __init__(self, bank):
		self.bank = bank

	def parse(self, report):
		return self.bank.parse_report(report)