import redis
import pickle
from datetime import datetime

class DataBase():

    def __init__(self):
        self.database = redis.Redis(host="redis", port=6379) # redis
        self.__id_of_entry = 0

    def __get_id(self):
        self.__id_of_entry += 1
        return str(self.__id_of_entry)

    def __get_tags_by_key(self, key):
        entry = pickle.loads(self.database.get(key))
        tags = entry.get_tags()
        return tags

    def __get_datetime_by_key(self, key):
        entry = pickle.loads(self.database.get(key))
        datetime = entry.get_datatime()
        return datetime

    def __is_in_interval(self, target_date_interval, entry_date):
        is_apropriate = False
        if target_date_interval[0] <= entry_date <= target_date_interval[1]:
            is_apropriate = True
        return is_apropriate

    def __has_necessary_tags(self, target_tags, entry_tags):
        is_apropriate = True
        for target_tag in target_tags:
            if target_tag not in entry_tags:
                is_apropriate = False
        return is_apropriate

    def __get_entry(self, key):
        return pickle.loads(self.database.get(key))

    def create_entry(self, text, tags, date):
        entry = {"text": text, "tags": tags, "date": date}
        pickled_entry = pickle.dumps(entry)
        generated_id = self.__get_id()
        self.database.set(generated_id, pickled_entry, nx=True)
        return generated_id, entry

    def edit_entry(self, id_of_entry, text, tags, date):
        entry = {"text": text, "tags": tags, "date": date}
        pickled_entry = pickle.dumps(entry)
        self.database.set(id_of_entry, pickled_entry, xx=True)
        return id_of_entry, entry

    def delete_entry(self, id_of_entry):
        self.database.delete(id_of_entry)
        return id_of_entry

    def get_entries(self, tags=None, date_interval=None):
        target_keys = []
        for key in self.database.keys("*"):
            key = key.decode("utf-8")
            in_date_interval, has_necessary_tags = True, True
            entry_dict = self.__get_entry(key)
            current_tags, current_datetime = entry_dict["tags"], entry_dict["date"]

            if tags is not None:
                has_necessary_tags =\
                    self.__has_necessary_tags(tags, current_tags)

            if date_interval is not None:
                in_date_interval = self.__is_in_interval(date_interval, current_datetime)

            if in_date_interval and has_necessary_tags:
                target_keys.append(key)

        target_entries = {}
        for key in target_keys:
            target_entries[key] = pickle.loads(self.database.get(key))
        return target_entries
