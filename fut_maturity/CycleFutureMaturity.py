from fut_maturity.future_maturity import FutureMaturity
from datetime import datetime

class CycleFutureMaturity(FutureMaturity):


    def __init__(self,final_settlement_rule,cycle,max_index, holiday_calendar = None):
        super(CycleFutureMaturity, self).__init__(final_settlement_rule, holiday_calendar)
        self._cycle = cycle
        self._max_index = max_index

    @property
    def max_index(self):
        return self._max_index

    def get_date(self, index,analysis_date):

        first_index = self._find_first_index(analysis_date)
        month_index = (first_index + index ) % len(self._cycle)
        year_add = (first_index + index ) //  len(self._cycle)
        month_add = self._cycle[month_index]

        base_date = datetime(analysis_date.year + year_add, month_add,1)

        return self.convert_to_date_mapping(base_date)

    def _find_first_index(self,analysis_date):

        settlement_date = self.convert_to_date_mapping(analysis_date)

        if settlement_date < analysis_date:
            current_month = analysis_date.month + 1
        else:
            current_month = analysis_date.month

        for index, month in enumerate(self._cycle):
            if month >= current_month:
                return index

        return 0


