from database.base_connection import BaseConnection


class Schedules(BaseConnection):
    def __init__(self):
        super().__init__(collection_name='schedules')

    def get_schedule(self, schedule_id):
        return self.collection.find_one({'_id': schedule_id})

    def delete_schedule(self, schedule_id):
        self.collection.delete_one({'_id': schedule_id})

    def add_schedule(self, schedule_id, job):
        self.collection.insert_one({'_id': schedule_id, 'schedule': job})
