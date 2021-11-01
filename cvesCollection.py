import utils
import json


class CVEsCollection:

    def __init__(self, year: str):
        """

        :param year:
        """
        self.cve_dict = utils.getCVE_Dict(year)
        self.numberOfCVEs = self.cve_dict['CVE_data_numberOfCVEs']
        self.CVE_data_timestamp = self.cve_dict['CVE_data_timestamp']
        self.CVE_Items = self.cve_dict['CVE_Items']

    def printCveDict(self):
        """
        This function prints the dictionary in JSON representation
        :return:
        """
        print(json.dumps(self.cve_dict['CVE_Items'][0], sort_keys=True, indent=4, separators=(',', ': ')))

    def getNumberOfCVEs(self) -> int:
        """

        :return:  number Of CVEs
        """
        return self.numberOfCVEs

    def getCVE_data_timestamp(self) -> str:
        """

        :return: CVE data timestamp
        """
        return self.CVE_data_timestamp

    def getCVE_Items(self) -> {}:
        """

        :return: CVE Items
        """
        return self.CVE_Items
