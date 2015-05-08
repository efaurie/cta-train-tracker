import requests

from xml.etree import ElementTree


class CTAInterface():
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'http://lapi.transitchicago.com/api/1.0/ttarrivals.aspx'

    def get_next_arrivals(self, station_id_list):
        next_arrivals = list()
        parameters = {'key': self.api_key}

        for station_id in station_id_list:
            parameters['mapid'] = station_id
            response = requests.get(self.base_url, params=parameters)
            next_arrivals += self.parse_xml_response(response.content)

        return next_arrivals

    @staticmethod
    def parse_xml_response(xml_content):
        next_arrivals = list()
        xml_tree = ElementTree.fromstring(xml_content)

        for node in xml_tree.iter('eta'):
            this_arrival = [None] * 4
            for child in node._children:
                if child.tag == 'staNm':
                    this_arrival[0] = child.text
                elif child.tag == 'rt':
                    this_arrival[1] = child.text
                elif child.tag == 'stpDe':
                    this_arrival[2] = child.text
                elif child.tag == 'arrT':
                    this_arrival[3] = child.text
            next_arrivals.append(this_arrival)

        return next_arrivals