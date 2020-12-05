import datetime


def parse_duration(string):
    """parse something like "1 day 2 hours".

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
