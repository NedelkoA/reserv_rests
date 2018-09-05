from datetime import datetime, timedelta


class DateConversion:
    def __init__(self, date, time):
        self.date = date
        self.time = time

    @property
    def reserve_time(self):
        return datetime.combine(self.date, self.time)

    def utc_time(self):
        return self.reserve_time - timedelta(hours=3)
