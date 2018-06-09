#coding=utf-8
from datetime import datetime

DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

def datetime_to_str(d, f=DATETIME_FORMAT):
    return d.strftime(f)

def date_to_str(d):
    return datetime_to_str(d, f=DATE_FORMAT)

def log_error(message):
    file_name = './log/meals.log.%s' % date_to_str(datetime.now().date())
    with open(file_name, 'a') as f:
        f.write('Time: %s, Message: %s\n' % (datetime_to_str(datetime.now()), message))
