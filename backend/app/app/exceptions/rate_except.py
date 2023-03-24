import datetime


class RateAPIError(Exception):
    """Exception - API ЦБ РФ не вернуло текущий курс"""

    def __init__(self, date: datetime.date):
        self.date = date

    def __str__(self):
        return f"Не удалось получить курс от API на {self.date}"
