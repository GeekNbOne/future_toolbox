from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime
from dateutil.relativedelta import relativedelta
from dateutil import parser


class DateRule(Enum):
    ThirdFriday = 0
    LastFriday = 1
    ThirdFridayMinus30days = 2
    BeforeLastBusinessDay = 3


class FutureMaturity(ABC):

    def __init__(self,  final_settlement_rule,holiday_calendar= None):
        self._final_settlement_rule = final_settlement_rule
        if holiday_calendar is None:
            self._holiday_calendar = []
        else:
            self._holiday_calendar = [parser.parse(date) for date in holiday_calendar]



    @property
    @abstractmethod
    def max_index(self):
        return 0

    def values(self,analysis_date):
        try:
            analysis_date = parser.parse(analysis_date)
        except TypeError as ve:
            if ve.args[0].split()[-1] not  in ('Timestamp','datetime'):
                raise

        for i in range(self.max_index):
            yield self.get_date(i,analysis_date)

    # def __iter__(self):
    #     self._iter_index = 0
    #     return self
    #
    # def __next__(self):
    #     if self._iter_index >= self.max_index:
    #         raise StopIteration
    #     else:
    #         self._iter_index += 1
    #
    #     return self.get_date(self._iter_index)

    def _third_friday_minus_30_day(self, date):
        base_date = self._third_friday(date + relativedelta(months=1))
        return base_date - relativedelta(days=30)

    def _third_friday(self, date):

        base_date = datetime(date.year, date.month, 1)

        day = (4 - base_date.weekday()) % 7 + 15

        return datetime(date.year, date.month, day)

    def _last_business_day(self,date):

        temp_date = date+ relativedelta(months = 1)
        base_date = datetime(temp_date.year,temp_date.month,1) - relativedelta(days=1)

        while self.none_business_day(base_date):
            base_date = base_date - relativedelta(days=1)

        return base_date

    def _before_last_business_day(self,date):
        base_date = self._last_business_day(date) - relativedelta(days=1)

        while self.none_business_day(base_date):
            base_date = base_date - relativedelta(days=1)

        return base_date

    # def __getitem__(self, item):
    #     return self.get_date(item)

    @abstractmethod
    def get_date(self, index,analysis_date):
        pass

    @property
    def convert_to_date_mapping(self):
        return {DateRule.ThirdFridayMinus30days: self._third_friday_minus_30_day,
                DateRule.ThirdFriday:self._third_friday,
                DateRule.BeforeLastBusinessDay:self._before_last_business_day}[self._final_settlement_rule]

    def none_business_day(self,date):
        if date.weekday() in (5, 6):
            return True
        elif date in self._holiday_calendar:
            return True
        else:
            return False