import requests, re, time, sys
import pandas as pd

out_file = "holidays.csv"
out_date_format = "%Y-%m-%d"

if len(sys.argv) == 3:
    out_file, out_date_format = sys.argv[1:]

r = requests.get("https://www.opm.gov/policy-data-oversight/pay-leave/federal-holidays/#url=Historical-Data")
r.raise_for_status()

html = r.text.split('<section class="tab-content" title="Historical Data">')[1]

rows = []
for table in re.findall(r'<table class="DataTable HolidayTable">([\s\S]*?)</table>', html):
    year = re.findall(r"(\d{4}) Holiday Schedule", table)
    if len(year) == 1:
        year = year[0]
    else:
        continue

    for tr in re.findall(r"<tr>([\s\S]*?)</tr>", table):
        row = []
        for td in re.findall(r"<td>([\s\S]*?)</td>", tr):
            row.append(re.sub(r"<.*>", "", td).replace("’", "'").strip())
        if len(row) == 2:
            years = re.findall("\d{4}", row[0])
            if years and years[0] != year:
                continue # this table specified for a different year
            date = row[0].split(", ")[1] + ", " + year
            date = time.strptime(date, "%B %d, %Y")
            row[0] = time.strftime(out_date_format, date)
            rows.append(row)

df = pd.DataFrame(rows, columns=["date", "holiday"])
df.sort_values(by="date").to_csv(out_file, index=False)
