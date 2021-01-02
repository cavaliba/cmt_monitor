# logger.py

import sys
import datetime

import globals as cmt


def logit(line):
    now = datetime.datetime.today().strftime("%Y/%m/%d - %H:%M:%S")
    print(now + ' : ' + line)


def abort(line):
    now = datetime.datetime.today().strftime("%Y/%m/%d - %H:%M:%S")
    print(now + ' : ' + line)
    print("ABORTING.")
    sys.exit()


def debug(*items):
    if cmt.ARGS['debug'] or cmt.ARGS['debug2']:
        print('DEBUG :', ' '.join(items))


def debug2(*items):
    if cmt.ARGS['debug2']:
        print('DEBUG2:', ' '.join(items))
