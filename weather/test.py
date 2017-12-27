#!/usr/bin/env python

from get_weather_data import get_weather_custom_data
from datetime import timedelta, date, datetime



start_date = date(2016,12,27)
end_date = date(2016, 12, 28)
print get_weather_custom_data(start_date,end_date)