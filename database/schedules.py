from database.base_connection import BaseConnection


class Schedules(BaseConnection):
    def __init__(self):
        super().__init__(collection_name='schedules')

    def get_schedule(self, schedule_id):
        return self.collection.search(self.query._id == schedule_id)

    def delete_schedule(self, schedule_id):
        self.collection.remove(self.query._id == schedule_id)

    def add_schedule(self, schedule_id, interval):
        self.collection.insert({'_id': schedule_id, 'interval': interval})

    def get_all_schedules(self):
        return self.collection.all()
