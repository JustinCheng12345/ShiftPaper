import requests
import json

class AtisReader:
    def __init__(self):
        self.address = "https://atis.cad.gov.hk/ATIS/ATISweb/atis.php"
        self.runway_config = None
        self.updated = True

    def get_runway(self):
        ATIS_data = requests.get(self.address).text

        print(ATIS_data.find("ARRIVALS, RWY"))
        print(ATIS_data.find("DEPARTURES, RWY "))

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
        #test data
        test = '''{"WFROST":{"name":"霜凍警告","code":"WFROST","actionCode":"ISSUE","issueTime":"2020-09-24T11:15:00+08:00","updateTime":"2020-09-24T11:15:00+08:00"},"WHOT":{"name":"酷熱天氣警告","code":"WHOT","actionCode":"ISSUE","issueTime":"2020-09-24T07:00:00+08:00","updateTime":"2020-09-24T07:00:00+08:00"},"WCOLD":{"name":"寒冷天氣警告","code":"WCOLD","actionCode":"ISSUE","issueTime":"2020-09-24T11:15:00+08:00","updateTime":"2020-09-24T11:15:00+08:00"},"WFNTSA":{"name":"新界北部水浸特別報告","code":"WFNTSA","actionCode":"ISSUE","issueTime":"2020-09-24T11:40:00+08:00","updateTime":"2020-09-24T11:40:00+08:00"},"WMSGNL":{"name":"強烈季候風信號","code":"WMSGNL","actionCode":"ISSUE","issueTime":"2020-09-24T11:15:00+08:00","updateTime":"2020-09-24T11:15:00+08:00"},"WL":{"name":"山泥傾瀉警告","code":"WL","actionCode":"ISSUE","issueTime":"2020-09-24T11:15:00+08:00","updateTime":"2020-09-24T11:15:00+08:00"},"WRAIN":{"name":"暴雨警告信號","code":"WRAINR","type":"紅色","actionCode":"ISSUE","issueTime":"2020-09-24T11:15:00+08:00","updateTime":"2020-09-24T11:15:00+08:00"},"WTMW":{"name":"海嘯警告","code":"WTMW","actionCode":"ISSUE","issueTime":"2020-09-24T11:15:00+08:00","updateTime":"2020-09-24T11:15:00+08:00"},"WTS":{"name":"雷暴警告","code":"WTS","actionCode":"EXTEND","issueTime":"2020-09-24T11:40:00+08:00","expireTime":"2020-09-24T19:30:00+08:00","updateTime":"2020-09-24T05:00:00+08:00"},"WTCSGNL":{"name":"熱帶氣旋警告信號","code":"TC3","actionCode":"ISSUE","type":"三號強風信號","issueTime":"2020-09-24T11:15:00+08:00","updateTime":"2020-09-24T11:15:00+08:00"},"WFIRE":{"name":"火災危險警告","code":"WFIRER","type":"紅色","actionCode":"ISSUE","issueTime":"2020-09-24T11:15:00+08:00","updateTime":"2020-09-24T11:15:00+08:00"}}'''
        warning_data = json.loads(test)
        for warning in warning_data:
            if warning == "WTCSGNL":
                typhoon = warning_data["WTCSGNL"]["code"]
            elif warning == "WRAIN":
                rainstorm = warning_data["WRAIN"]["code"]
        if (self.typhoon != typhoon) or (self.rainstorm != rainstorm):
            self.typhoon = typhoon
            self.rainstorm = rainstorm
            self.updated = True