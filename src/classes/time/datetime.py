import datetime

from datetime import datetime, timedelta
from dateutil import parser


class Datetime:


    def days_to_timestamp(self, days: int):
        timestamp = datetime.today() - timedelta( days = days )
        return timestamp


    def age_days(self, date) -> int:
        get_date_obj = parser.parse(date)
        date_obj = get_date_obj.replace(tzinfo=None)
        diff = datetime.now() - date_obj
        
        return diff.days
