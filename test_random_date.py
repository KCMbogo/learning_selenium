import random
from datetime import datetime, timedelta

def get_random_date(start_date, end_date, date_format="%Y-%m-%d"):
    delta = end_date - start_date
    random_days = random.randint(a=0, b=delta.days)
    random_date = start_date + timedelta(days=random_days)
    return random_date.strftime(date_format)

start = datetime(year=1970, month=1, day=1)
end = datetime.now() - timedelta(days=365 * 12)

random_date = get_random_date(start, end)

print(random_date)