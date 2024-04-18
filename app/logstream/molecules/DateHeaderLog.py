
"""
Two lines:
|
| November 28th, 2024

In addition to visually separating days, these are helpful for day-by-day and week-by-week log sorting.
The logstreams contained between them are considered owned by whichever is most recent.

A nice way of printing a day is finding one of these and printing all logstream objects from this until
the next date header.

- Should the Manager have to scan every object looking for these guys?
  - Or can there be a lookup dictionary these things self manage themselves within?
"""