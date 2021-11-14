
class Cve:

    def __init__(self, dict : {}):
        """

        """
        self.identifier = dict['cve']['CVE_data_meta']['ID']
        self.ASSIGNER = dict['cve']['CVE_data_meta']['ASSIGNER']
        self.description = dict['cve']['problemtype']['problemtype_data'][0]['description'][0]['value']
        self.severity = dict['impact']
        if len(self.severity) > 1:
            self.severity = self.severity['baseMetricV3']['cvssV3']['baseSeverity']
        else:
            self.severity = self.severity['baseMetricV2']['severity']



    def getCveId(self) -> int:
        """

        :return:
        """
        return self.identifier

    def getCveAssigner(self) -> str:
        """

        :return:
        """
        return self.ASSIGNER

    def getCveDescription(self) -> str:
        """

        :return:
        """
        return self.description

    def getCveSeverity(self) -> str:
        """
        :return:
        """
        return self.severity

    def printCve(self):
        print("CVE identifier: " + self.identifier)
        print("CVE Assigner: " + self.ASSIGNER)
        print("CVE description: " + self.description)
        print("CVE severity: " + self.severity)