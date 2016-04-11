#!env/bin/python

import json
import datetime
import requests
from tabulate import tabulate

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

    table = [ [ c["id"], c["name"], c["start_date"] ] for c in competitions ]
    print(tabulate(table, headers=[ "ID", "Name", "Start Date"]))

if __name__ == "__main__":
    main()
