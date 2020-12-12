import datetime



# -----------------
# Timeout stop
# -----------------
def timeout_handler(signum, frame):
    #raise Exception("Timed out!")
    print("Timed out ! (max_execution_time)")
    sys.exit()


# ----------------------------------------------------------
# logit
# ----------------------------------------------------------


def logit(line):
    now = datetime.datetime.today().strftime("%Y/%m/%d - %H:%M:%S")
    print(now + ' : ' + line)

def abort(line):
    now = datetime.datetime.today().strftime("%Y/%m/%d - %H:%M:%S")
    print(now + ' : ' + line)
    print("ABORTING.")
    sys.exit()


# ----------------------------------------------------------


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# ----------------------------------------------------------


def parse_duration(string):
    """parse a duration like "1 day 2 hours".

    Units can be singular or plural. Supported units are years, months, weeks, days and
    hours. A months is equivalent to 30 days. A year is 365 days.

    Negatives values aren't supported.
    """

    if string.strip() == "":
        raise ValueError("duration cannot be just empty space {!r}", string)

    words = string.split(" ")
    kwargs = {}
    quantifier = None
    for i, word in enumerate(words):
        if i % 2 == 0:
            try:
                quantifier = int(word)
            except ValueError:
                # for better context (both exceptions will be printed though)
                raise ValueError(
                    "failed parsing quantifier {!r} in duration {!r}".format(
                        word, string
                    )
                )

            if quantifier < 0:
                raise ValueError("don't use negative values {!r}".format(string))

        else:
            # it's a unit
            if not word.endswith("s"):
                word += "s"

            if word not in ("years", "weeks", "days", "months", "hours"):
                raise ValueError("invalid unit {!r} in {!r}".format(word, string))

            if word in kwargs:
                raise ValueError("unit {!r} already used in {!r}".format(word, string))

            kwargs[word] = quantifier

            quantifier = None

    if quantifier is not None:
        raise ValueError(
            "unit expected for the last quantifier {!r} in {!r}".format(
                quantifier, string
            )
        )

    # dealing with the variations in the number of days of each months/year would be an
    # overkill here

    if "months" in kwargs:
        kwargs["days"] = kwargs.get("days", 0) + 30 * kwargs["months"]
        del kwargs["months"]

    if "years" in kwargs:
        kwargs["days"] = kwargs.get("days", 0) + 365 * kwargs["years"]
        del kwargs["years"]

    return datetime.timedelta(**kwargs)

# ----------------------------------------------------------


def is_timeswitch_on(myconfig):
    ''' check if a date/time time range is active
        myconfig can be :
              yes
              no
              after YYYY-MM-DD hh:mm:ss
              before YYYY-MM-DD hh:mm:ss
              hrange  hh:mm:ss hh:mm:ss
              ho   (Mon-Fri 8h30-18h)
              hno
        returns True or False if current datatime match myconfig
    '''

    # yaml gotcha
    myconfig = str (myconfig)

    if myconfig == "True" or myconfig == "yes" or myconfig == "true":
        return True

    if myconfig == "False" or myconfig =="no"  or myconfig == "false":
        return False

    myarray = myconfig.split()
    action = myarray.pop(0)

    if action  == "after":
        mynow = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        target = ' '.join(myarray)
        #print(mynow)
        if mynow >= target:
            return True
        return False

    if action == "before":
        mynow = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        target = ' '.join(myarray)
        if mynow <= target:
            return True
        return False

    if action == "hrange":
        mynow = datetime.datetime.today().strftime("%H:%M:%S")
        if mynow >= myarray[0] and mynow <= myarray[1]:
            return True
        return False

    if action == "ho":
        myday  = datetime.datetime.today().strftime("%a")
        myhour = datetime.datetime.today().strftime("%H:%M:%S")
        if myday in ["Sat","Sun"]:
            return False
        if myhour < "08:30:00" or myhour > "18:00:00":
            return False
        return True

    if action == "hno":
        myday  = datetime.datetime.today().strftime("%a")
        myhour = datetime.datetime.today().strftime("%H:%M:%S")
        if myday in ["Mon","Tue","Wed","Thu","Fri"]:
            if myhour >= "08:30:00" or myhour <= "18:00:00":
                return False
        return True

    # default, unknown / no match
    return False

# ----------------------------------------------------------


# ----------------------------------------------------------


# ----------------------------------------------------------


