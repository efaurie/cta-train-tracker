import requests

from xml.etree import ElementTree


class CTAInterface():
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'http://lapi.transitchicago.com/api/1.0/ttarrivals.aspx'

    def ping_many(self, station_id_list):
        schedule = list()

        for station_id in station_id_list:
            parameters = {
                'key': self.api_key,
                'mapid': station_id,
            }

            response = requests.get(self.base_url, params=parameters)
            schedule += self.parse_xml_response(response.content)

        return schedule

    def parse_xml_response(self, xml_content):
        entries = list()
        xml_tree = ElementTree.fromstring(xml_content)

        for node in xml_tree.iter('eta'):
            entry = [None] * 4
            for child in node._children:
                if child.tag == 'staNm':
                    entry[0] = child.text
                elif child.tag == 'rt':
                    entry[1] = child.text
                elif child.tag == 'stpDe':
                    entry[2] = child.text
                elif child.tag == 'arrT':
                    entry[3] = child.text
            entries.append(entry)

        return entries