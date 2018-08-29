import requests
import xmltodict
from requests.exceptions import ConnectionError as RequestsConnectionError
import re
import time

class OAIHarvester(object):

    def __init__(self, config, baseUrl = None):
        self.config = config
        self.baseUrl = baseUrl
        self.granularity = self.setGranularity()

    def changeOAI(self, baseUrl):
        self.baseUrl = baseUrl
        self.granularity = self.setGranularity()

    def listPrefixes(self):
        requestParams = {"verb": "ListMetadataFormats"}
        response = self.makeRequest(requestParams)
        data = self.parseResponse(response)
        formats = data['OAI-PMH']['ListMetadataFormats']['metadataFormat']
        prefixes = [format['metadataPrefix'] for format in formats]
        return prefixes

    def makeRequest(self, requestParams):
        tryNum = 0
        while tryNum < self.config['MAX_RETRIES']:
            try:
                response = requests.post(self.baseUrl, requestParams)
                return response
            except RequestsConnectionError:
                time.sleep(self.config['RETRY_WAIT'])
                tryNum += 1
        raise OAIConnectionError("OAI unavailable after %d retries, stopping harvest" % self.config['MAX_RETRIES'])

    def parseResponse(self, response):
        xmlString = re.sub("<\?xml.*?\?>", "", response.text)
        data = xmltodict.parse(xmlString, process_namespaces=False)
        if 'error' in data['OAI-PMH']:
            if data['OAI-PMH']['error']['@code'] == "noRecordsMatch":
                self.finished = True
            else:
                raise OAIRequestError({'error': data['OAI-PMH']['error']['@code'], 'message': data['OAI-PMH']['error']['#text']})
        return data

    def initialiseHarvest(self):
        self.finished = False
        self.harvestedListSize = 0
        self.completeListSize = None

    def getGranularity(self):
        return self.granularity

    def setGranularity(self):
        response = requests.post(self.baseUrl, {"verb": "Identify"})
        if response.status_code == 200:
            data = self.parseResponse(response)
            granularity = data['OAI-PMH']['Identify']['granularity']
            if granularity == "YYYY-MM-DD":
                return "%Y-%m-%d"
            elif granularity == "YYYY-MM-DDThh:mm:ssZ":
                return "%Y-%m-%dT%H:%M:%SZ"

    def harvestRecords(self, requestParams):
        self.initialiseHarvest()
        while not self.finished:
            records = self.listRecords(requestParams)
            self.harvestedListSize += len(records)
            for record in records:
                yield record
            requestParams = {"verb": "ListRecords", "resumptionToken": self.resumptionToken}

    def listRecords(self, requestParams):
        response = self.makeRequest(requestParams)
        data = self.parseResponse(response)
        try:
            self.setResumptionToken(data['OAI-PMH']['ListRecords'])
        except KeyError:
            self.resumptionToken = None
            self.finished = True
            return []
        return self.getRecords(data)

    def getRecords(self, data):
        return data['OAI-PMH']['ListRecords']['record']

    def setResumptionToken(self, data):
        if 'resumptionToken' not in data.keys():
            self.resumptionToken = None
            self.finished = True
            return False
        if '#text' in data['resumptionToken']:
            self.resumptionToken = data['resumptionToken']['#text']
            print self.resumptionToken
        else:
            self.resumptionToken = None
            self.finished = True
        if '@cursor' in data['resumptionToken']:
            self.cursor = data['resumptionToken']['@cursor']
        if '@completeListSize' in data['resumptionToken']:
            self.completeListSize = data['resumptionToken']['@completeListSize']
            print "completeListSize:", self.completeListSize, "\tharvestedListSize", self.harvestedListSize

class OAIConnectionError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class OAIRequestError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class OAIHarvestError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

