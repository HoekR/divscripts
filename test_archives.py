import oai_harvester

if __name__ == "__main__":
    oai_url = "http://www.archieven.nl/pls/oai/!pck_oai_pmh.OAIHandler"
    config = {
        "MAX_RETRIES": 10,
        "RETRY_WAIT": 5,
    }
    harvester = oai_harvester.OAIHarvester(config, oai_url)
    request_params = {
        "prefix": "oai_ead",
        "verb": "ListRecords"
    }
    harvester.harvestRecords(request_params)

