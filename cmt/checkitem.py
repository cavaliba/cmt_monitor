# checkitem.py

import datetime
# import globals as cmt


# ----------------------------------------------------------
# Class CheckItem
# ----------------------------------------------------------

class CheckItem():

    ''' Store one single data point '''

    def __init__(self, name, value, description="", unit=''):
        self.name = name
        self.value = value
        self.description = description
        self.unit = unit

    def fmt_bytes(self, num, suffix='B'):
        for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
            if abs(num) < 1000.0:
                return "%3.1f %s%s" % (num, unit, suffix)
            num /= 1000.0
        return "%.1f %s%s" % (num, 'Y', suffix)

    def fmt_hms(self, sec):
        a = datetime.timedelta(seconds=sec)
        return str(a)

    def human(self):
        '''Build an optional ()  human formatted string for some units values'''
        if self.unit == 'bytes':
            x = self.fmt_bytes(int(self.value))
            return str(x)
        elif self.unit == 'seconds':
            x = self.fmt_hms(int(self.value))
            return x
        else:
            return ''
