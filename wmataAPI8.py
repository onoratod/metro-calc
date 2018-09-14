import http.client, urllib.request, urllib.parse, urllib.error, base64
from bs4 import BeautifulSoup as bs
import json
import requests

'''
headers = {
    # Request headers
    'api_key': '0d79b57328d54a1688294c01d9402f50',
}

params = urllib.parse.urlencode({
    # Request parameters
    'FromStationCode': 'E10',
    'ToStationCode': 'J03',
})

try:
    conn = http.client.HTTPSConnection('api.wmata.com')
    conn.request("GET", "/Rail.svc/SrcStationToDstStationInfo?%s" % params, "{body}", headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))
    
page_response = requests.get('https://api.wmata.com/Rail.svc/json/jSrcStationtoDstStationInfo?%s' % params, headers)
page_content = bs(page_response.content, "html.parser")
'''

class wmataAPI(object):
    class _station2station(object):
        def __init__(self, API, start_station, end_station):
            self.params = urllib.parse.urlencode({
                # Request parameters
                'FromStationCode': start_station,
                'ToStationCode': end_station,
            })
            self.url = 'https://api.wmata.com/Rail.svc/json/jSrcStationtoDstStationInfo?%s' % self.params
            page_response = requests.get(self.url, API)
            self.content = json.loads(bs(page_response.content, "html.parser").contents[0])["StationToStationInfos"][0]
            self.set_params()
        
        def set_params(self):
            self.source = self.content['SourceStation']
            self.destination = self.content['DestinationStation']
            self.miles = self.content['CompositeMiles']
            self.railtime = self.content['RailTime']
            self.peak_fare = self.content['RailFare']['PeakTime']
            self.offpeak_fare = self.content['RailFare']['OffPeakTime']
            self.senior_fare = self.content['RailFare']['SeniorDisabled']
    
    def __init__(self, api_key):
        self.API = {'api_key' : api_key}
        self.name_to_code_map()
        
    def name_to_code_map(self):
        page_response = requests.get('https://api.wmata.com/Rail.svc/json/jStations?%s', self.API)
        page_content = bs(page_response.content, "html.parser")
        stations = json.loads(str(page_content))['Stations']
        stations_map = {}
        for station in stations:
            stations_map[station['Name']] = station['Code']
        self.name_to_code_map = stations_map
        
    def name_to_code(self, station_name):
        return self.name_to_code_map[station_name]
        
    
    def __s2s__(self, start, end):
        return wmataAPI._station2station(self.API, start, end)
        

#test = wmataAPI('0d79b57328d54a1688294c01d9402f50')
#stest = test.__s2s__('E10', 'J10')

'''
page_response = requests.get('https://api.wmata.com/Rail.svc/json/jStations?%s', headers)
page_content = bs(page_response.content, "html.parser")
'''
