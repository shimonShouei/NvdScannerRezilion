from flask import Flask, request, jsonify
from pymongo.errors import DuplicateKeyError

from mongoDataLayer import MongoDataLayer

app = Flask(__name__)
conn_string = 'mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false'
dataLayer = MongoDataLayer(conn_string)


@app.route('/vulnerabilities/getByComputerName/<comp_name>', methods=['GET'])
def get_by_comp(comp_name):
    try:
        db = dataLayer.connect_to_db("vulnerabilities_scanner")
        cves_table = dataLayer.get_table_cursor(db, "cve_collection")
        record = dataLayer.get_record_by_name(comp_name, cves_table)
        if record == -1:
            return jsonify(f"{comp_name} is not exist!"), 404
        return jsonify({"Requested cve list": record}), 200
    except Exception as e:
        return jsonify("Some problem"), 500


@app.route('/vulnerabilities/insert', methods=['POST'])
def insert_my_vulnerabilities():
    try:
        update_mode = request.json["update_mode"]
        comp_name = request.json["name"]
        cves = request.json["cve_list"]
        db = dataLayer.connect_to_db("vulnerabilities_scanner")
        cves_table = dataLayer.get_table_cursor(db, "cve_collection")
        if update_mode:
            dataLayer.update_record(comp_name, cves, cves_table)
        else:
            dataLayer.insert_new_record(comp_name, cves, cves_table)
        return jsonify("Data inserted succsesful"), 201
    except DuplicateKeyError as e:
        return jsonify("Name exist already"), 404
    except Exception as e:
        return jsonify("Some problem"), 500


if __name__ == '__main__':
    app.run(debug=True)
