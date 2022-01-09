
class DataLayer:
    def __init__(self, conn_string):
        self.conn_string = conn_string

    def connect_to_db(self, db_name):
        pass

    def get_table_cursor(self, db, name):
        pass

    def get_record_by_name(self, name, table):
        pass

    def insert_new_record(self, name, record, table):
        pass

    def update_record(self, name, record, table):
        pass