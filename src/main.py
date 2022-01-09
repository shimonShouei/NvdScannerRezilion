import shutil
import sys
from datetime import datetime
import socket
from time import sleep

import requests
from src.app import App
from itertools import product


def main(args_list):
    try:
        app = App(*args_list)
        app.logger.info(f"args = {args_list}")
        app.download_cpe_xml()
        app.parse_cpe_xml()
        app.get_local_sw()
        app.build_searcher()
        my_cpe = app.find_my_cpe()
        cve_year_dict = app.download_cve_dicts()
        invInd = app.build_inverted_ind(cve_year_dict)
        cve_d = app.scan(my_cpe, invInd)
        bool_update_my_cve = app.update_my_cve
        comp_name = socket.gethostname() + datetime.now().strftime("%d_%m-%H_%M_%S")
        print("Sending...")
        sleep(5)
        response = requests.post("http://localhost:5000/vulnerabilities/insert",
                                 json={"update_mode": bool_update_my_cve, "name": comp_name, "cve_list": cve_d})
        app.logger.info(response.text)
    except Exception as e:
        # shutil.rmtree('./resources')
        # app.logger.info("Removed resources")
        # shutil.rmtree('./models')
        # app.logger.info("Removed models")
        app.logger.error(e, exc_info=True)
        # app.logger.info("Please try again")


if __name__ == '__main__':
    args = sys.argv[1:]
    # for args in product([True, False], repeat=3):
    main(args)
