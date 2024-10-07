from tinydb import TinyDB, Query


class BaseConnection:
    def __init__(self, db_path='database/db.json', collection_name=None):
        self.db = TinyDB(db_path)
        if collection_name is None:
            raise ValueError("Collection name must be provided.")
        self.collection = self.db.table(collection_name)
        self.query = Query()
