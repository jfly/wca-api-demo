#!env/bin/python

import io
import csv
import json
import datetime
import requests
import pyperclip

def fetch_competitions():
    competitions = []

    now = datetime.date.today()

    start_date = (now - datetime.timedelta(days=60)).isoformat()
    end_date = now.isoformat()

    next_url = 'https://staging.worldcubeassociation.org/api/v0/competitions?start={start}&end={end}'.format(start=start_date, end=end_date)
    while next_url:
        # print("Fetching {}".format(next_url))
        r = requests.get(url=next_url)
        assert r.status_code == 200
        competitions.extend(r.json())

        next_url = r.links.get("next", {}).get('url')

    return competitions


def main():
    competitions = fetch_competitions()

    output = io.StringIO()
    writer = csv.writer(output)
    for c in competitions:
        writer.writerow([c["id"], c["name"], c["start_date"]])
    csv_comps = output.getvalue()
    pyperclip.copy(csv_comps)
    print(csv_comps)

if __name__ == "__main__":
    main()
