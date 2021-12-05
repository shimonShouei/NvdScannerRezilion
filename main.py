import get_files_programfiles
from cve_parser import CveParser


def main():
    # parse = CveParser()
    # year = "2021"
    # cve_specific_year_collection = parse.get_cve_collection_for_specific_year(year)
    # print(cve_specific_year_collection[0].identifier)
    # print(cve_specific_year_collection[0].cve_to_string())
    # parse.write_all_cve_collection_for_specific_year_to_file("2002")

    get_files_programfiles.get_file_from_path("TeamViewer")
    # get_files_programfiles.get_file_from_path("C:\Program Files (x86)")






if __name__ == '__main__':
    main()