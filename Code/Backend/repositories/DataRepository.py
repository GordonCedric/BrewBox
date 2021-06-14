from .Database import Database
import time


class DataRepository:
    @staticmethod
    def json_or_formdata(request):
        if request.content_type == 'application/json':
            gegevens = request.get_json()
        else:
            gegevens = request.form.to_dict()
        return gegevens

    @staticmethod
    def read_status_lampen():
        sql = "SELECT * from lampen"
        return Database.get_rows(sql)

    @staticmethod
    def read_status_lamp_by_id(id):
        sql = "SELECT * from lampen WHERE id = %s"
        params = [id]
        return Database.get_one_row(sql, params)

    @staticmethod
    def update_status_lamp(id, status):
        sql = "UPDATE lampen SET status = %s WHERE id = %s"
        params = [status, id]
        return Database.execute_sql(sql, params)

    @staticmethod
    def update_status_alle_lampen(status):
        sql = "UPDATE lampen SET status = %s"
        params = [status]
        return Database.execute_sql(sql, params)

    # BrewBox
    @staticmethod
    def add_temperatures(temperatures):
        datetime = time.strftime('%Y-%m-%d %H:%M:%S')
        sql = "INSERT INTO historiekDevices (devices_id, value, timestamp) VALUES (1, %s, %s), (2, %s, %s)"
        params = [temperatures[0], datetime, temperatures[1], datetime]
        return Database.execute_sql(sql, params)

    @staticmethod
    def add_volumes(volumes):
        datetime = time.strftime('%Y-%m-%d %H:%M:%S')
        sql = "INSERT INTO historiekDevices (devices_id, value, timestamp) VALUES (3, %s, %s), (4, %s, %s)"
        params = [volumes[0], datetime, volumes[1], datetime]
        return Database.execute_sql(sql, params)

