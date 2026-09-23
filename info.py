import logging
import requests, json, re

class AtisReader:
    def __init__(self):
        self.address = "https://atis.cad.gov.hk/ATIS/ATISweb/atis.php"
        self.runway_config = None
        self.updated = True

    def get_runway(self):
        ATIS_data = requests.get(self.address).text

        arr_rwy = re.search('ARRIVALS, RWY (.*?)\\.', ATIS_data).group(1)
        dep_rwy = re.search('DEPARTURES, RWY (.*?)\\.', ATIS_data).group(1)
        logging.info("ARRIVALS: " + arr_rwy + " / DEPARTURES: " + dep_rwy)
        if arr_rwy == dep_rwy:
            # Single Runway
            self.runway_config = arr_rwy
        elif arr_rwy == '07L/R' and dep_rwy == '07C/R':
            self.runway_config = '07ADM'
        elif arr_rwy == '25L/R' and dep_rwy == '25L/C':
            self.runway_config = '25ADM'
        elif arr_rwy == '07L' and dep_rwy == '07R':
            self.runway_config = '07NS'
        elif arr_rwy == '25R' and dep_rwy == '25L':
            self.runway_config = '25NS'
        elif arr_rwy == '07C' and dep_rwy == '07R':
            self.runway_config = '07CS'
        elif arr_rwy == '25C' and dep_rwy == '25L':
            self.runway_config = '25CS'

        return self.runway_config

class WeatherReader:
    def __init__(self):
        self.address = "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=warnsum&lang=en"
        self.typhoon = None
        self.rainstorm = None
        self.updated = False

    def get_weather(self):
        typhoon = None
        rainstorm = None

        r = requests.get(self.address)
        warning_data = r.json()
        # test data
        # test = '''{"WRAIN":{"name":"暴雨警告信號","code":"WRAINR","type":"紅色","actionCode":"ISSUE","issueTime":"2020-09-24T11:15:00+08:00","updateTime":"2020-09-24T11:15:00+08:00"},"WTCSGNL":{"name":"熱帶氣旋警告信號","code":"TC3","actionCode":"ISSUE","type":"三號強風信號","issueTime":"2020-09-24T11:15:00+08:00","updateTime":"2020-09-24T11:15:00+08:00"}}'''
        # warning_data = json.loads(test)
        for warning in warning_data:
            if warning == "WTCSGNL":
                typhoon = warning_data["WTCSGNL"]["code"]
            elif warning == "WRAIN":
                rainstorm = warning_data["WRAIN"]["code"]
        if (self.typhoon != typhoon) or (self.rainstorm != rainstorm):
            self.typhoon = typhoon
            self.rainstorm = rainstorm
            self.updated = True

        logging.info("Typhoon: " + str(typhoon) + " / Rainstorm: " + str(rainstorm))