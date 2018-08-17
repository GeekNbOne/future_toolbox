from fut_maturity.future_maturity import FutureMaturity
from datetime import datetime
from dateutil.relativedelta import  relativedelta

class NearTermFutureMaturity(FutureMaturity):

    def __init__(self,final_settlement_rule,month_serial):
        super(NearTermFutureMaturity, self).__init__(final_settlement_rule)
        self._month_serial = month_serial
        self.current = 1

    @property
    def max_index(self):
        return self._month_serial

    def get_date(self,index,analysis_date):

        base_date = datetime(analysis_date.year,analysis_date.month,1)

        if self._passed_analysis_date(analysis_date):
            base_date = base_date + relativedelta(months=1)

        base_date = base_date + relativedelta(months = index)

        return self.convert_to_date_mapping(base_date)

    def _passed_analysis_date(self,analysis_date):

        month = analysis_date.month
        base_date = datetime(analysis_date.year, month, 1)

        settlement_date = self.convert_to_date_mapping(base_date)

        if settlement_date < analysis_date:
            return True
        else:
            return False



