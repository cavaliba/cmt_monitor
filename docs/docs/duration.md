
## timerange fields

Moste option like `enable`, or `enable_pager` accept at timerange value.

    # -------------------------------------
    # timerange fields (from documentation)
    # -------------------------------------
    # yes, 24/7                    : always
    # no                           : never
    # after YYYY-MM-DD hh:mm:ss    : after time of the day
    # before YYYY-MM-DD hh:mm:ss   : before ... 
    # hrange hh:mm:ss hh:mm:ss     : time intervall
    # ho, bh, business_hours       : 8h30/18h mon>fri - see global configuration for custom time
    # nbh,hno, non_business_hours  : !(8h30/18h mon>fri)
    #


## Duration for module certifcate

    duration = quantifier space unit space quantifier space unit ...

    quantifier = positive integer (0, 1, 2, ...)
    unit       = "hour", "day", "week", "month", "year"

    Units may have an extra "s" at the end.

A month is 30 days, and a year is 365 days, always.

### Examples

    1 day 3 hours
    2 weeks
    3 years 2 month 1 day 23 hours
    50 hours
    1 hour 3 days

These are invalid:

    1 day 2           what is the unit for 2?
    2 day 3 day       duplicate units not allowed
    2 day -1 hour     negatives not allowed
    2hours            space required
    3 foo             invalid unit

Equivalence:

    1 day    == 24 hours
    1 month  == 30 days
    1 year   == 365 days