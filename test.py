

from datetime import date, timedelta
import time

start_Date = date.today()  # год, месяц, число
result_date = start_Date - timedelta(days = 1)
timestamp = time.mktime(start_Date.timetuple())
print(type(result_date))

