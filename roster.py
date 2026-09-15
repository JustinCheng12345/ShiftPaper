import logging
import requests, csv

class MonthlyRoster:
    def __init__(self, year, month):
        self.year = year
        self.month = month
        self.schedule = {}

    def __repr__(self):
        return str(self.schedule)

    def add_shift(self, day, stream, shift):
        # off by 1
        self.schedule[day] = (stream, shift)

    def get_schedule(self, day):
        return self.schedule[day]

class Roster:
    def __init__(self, callsign):
        self.callsign = callsign
        self.name = ""
        self.rosters = {}
        self.roster_address = "https://www.dropbox.com/s/cfk0gwggic0v2o5/STRostersData.txt?raw=1"
        self.read_roster()

    def read_roster(self):
        logging.info("Reading roster...")

        r = requests.get(self.roster_address)
        reader = csv.reader(r.text.splitlines(), delimiter=';')

        month=''
        day=1
        name_selected=False
        for row in reader:
            if any('Roster:' in item for item in row):
                month = row[0][7:]
                day = 1
                self.rosters[month]=MonthlyRoster(row[1], month)
                continue
            if any('Name:' in item for item in row):
                name_selected = row[1] == self.callsign
                if name_selected:
                    self.name = row[0][7:]
                    logging.info("Roster name: " + self.name)
                continue
            if not name_selected:
                continue
            if len(row) > 1:
                self.rosters[month].add_shift(day, row[0], row[1])
                day += 1

    def get_shift(self, month, day):
        return self.rosters[month].get_schedule(day)