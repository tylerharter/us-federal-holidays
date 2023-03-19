# US Federal Holidays

CSV containing holidays scraped from https://www.opm.gov/policy-data-oversight/pay-leave/federal-holidays by scrape.py.  Results checkpointed to history.csv.

Notes:
* the scraped data is split on `<section class="tab-content" title="Historical Data">`, and only the dates after are considered.  Removing this would scrape future as well as historical dates.
* quote types are manually replaced
* cells containing dates with years are ignored.  For example, 2011 contains an entry "Friday, December 31, 2010" -- this is not included in the CSV.
