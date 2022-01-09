import pymongo as pymongo

from dataLayer import DataLayer


class MongoDataLayer(DataLayer):
    def connect_to_db(self, db_name):
        client = pymongo.MongoClient(self.conn_string)
        db = client[db_name]
        return db

    def get_table_cursor(self, db, name):
        return db[name]

    def get_record_by_name(self, name, table):
        try:
            return table.find({"name": name}, {"_id": 0})[0]
        except IndexError as e:
            return -1

    def insert_new_record(self, name, record, table):
        final = {"name": name, "cve_list": record}
        table.insert_one(final)

    def update_record(self, name, record, table):
        final = {"cve_list": record}
        myquery = {"name": name}
        newvalues = {"$set": final}
        table.update_one(myquery, newvalues)