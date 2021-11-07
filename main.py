import utils
from cvesCollection import CVEsCollection
from cve import Cve

def main():
    """

    :return:
    """
    year = "2021"
    cve_year_collection = CVEsCollection(year)
    cve = cve_year_collection.getCveByIndex(51)
    print("Hello")





if __name__ == '__main__':
    main()

