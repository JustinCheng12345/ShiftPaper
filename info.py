import requests

class AtisReader:
    def __init__(self):
        self.address = "https://atis.cad.gov.hk/ATIS/ATISweb/atis.php"
        self.r = ""

    def read(self):
        self.r = requests.get(self.address)

    def get_runway(self):
        self.read()

        print(self.r.text.find("ARRIVALS, RWY"))
        print(self.r.text.find("DEPARTURES, RWY "))