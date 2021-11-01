
class Cve:

    def __init__(self, dict : {}):
        """

        """
        self.ID = dict['cve']['CVE_data_meta']['ID']
        self.ASSIGNER = dict['cve']['CVE_data_meta']['ASSIGNER']
        self.description = dict['cve']['problemtype']['problemtype_data'][0]['description'][0]['value']

    def getCveId(self) -> int:
        """

        :return:
        """
        return self.ID

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

