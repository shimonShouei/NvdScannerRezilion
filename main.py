import utils
from cvesCollection import CVEsCollection

def main():
    """

    :return:
    """
    year = "2021"
    cve_year_collection = CVEsCollection(year)
    cve_dict = cve_year_collection.getCVE_Items()
    cve_year_collection.getCveByIndex(0)
    print()



if __name__ == '__main__':
    main()

