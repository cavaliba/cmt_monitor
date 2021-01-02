# persist.py

import json

import globals as cmt
from logger import debug


# ----------------------------------------------------------
# Class PERSIST
# ----------------------------------------------------------
class Persist():
    ''' Implement a persistent on-disk key/value structure, between cmt runs'''

    def __init__(self, file=None):
        self.file = file
        self.dict = {}
        self.load()

    def has_key(self, key):
        return key in self.dict

    def get_key(self, key, value=None):
        return self.dict.get(key, value)

    def set_key(self, key, value):
        self.dict[key] = value

    def delete_key(self, key):
        self.dict.pop(key, None)

    def load(self):
        debug("Persist.load() : ", self.file)
        data = ""
        try:
            with open(self.file, "r") as fi:
                data = fi.read()
        except Exception as e:
            debug("ERROR - Persist() : couldn't read file {} - {}".format(self.file, e))
        # decoding the JSON to dictionay
        try:
            self.dict = json.loads(data)
        except Exception as e:
            debug("ERROR - Persist() : couldn't decode data - {}".format(e))

    def save(self):
        # Save Persistance to file

        if not cmt.ARGS['cron'] and not cmt.ARGS['persist']:
            debug("Persist: save disabled")
            return

        data = json.dumps(self.dict, indent=2)
        try:
            with open(self.file, "w") as fi:
                fi.write(data)
        except Exception as e:
            debug("ERROR - Persist() : couldn't write file {} - {}".format(self.file, e))
            return

        debug("Persist saved")
