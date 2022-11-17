from copy import deepcopy
from flask import session
from datetime import datetime
import json


def save_entry(id, entry):
    tmp_entry = deepcopy(entry)
    tmp_entry["date"] = str(tmp_entry["date"])
    session["id"] = json.dumps(id)
    session["entry"] = json.dumps(tmp_entry)
    print("Saved entry: {}".format(session["entry"]))


def save_tags_and_dates(tags, date_interval):
    session["tags"] = json.dumps(tags)
    stringified_date_interval =\
        None if date_interval is None else (str(date_interval[0]), str(date_interval[1]))
    session["date_interval"] = json.dumps(stringified_date_interval)


def pop_tags_and_dates():
    if "tags" in session:
        session.pop("tags")
    if "date_interval" in session:
        session.pop("date_interval")


def get_tags_and_dates():
    tags = json.loads(session["tags"]) if "tags" in session else None
    date_interval = None
    if "date_interval" in session and json.loads(session["date_interval"]) is not None:
        stringified_date_interval = json.loads(session["date_interval"])
        date_interval =\
            (datetime.fromisoformat(stringified_date_interval[0]),
             datetime.fromisoformat(stringified_date_interval[1]))
    print("Type of saved in session date_interval is: {}".format(type(date_interval)))
    return tags, date_interval


def get_entry_if_exists():
    if "entry" in session:
        id = json.loads(session["id"])
        entry = json.loads(session["entry"])
        entry["date"] = datetime.fromisoformat(entry["date"])
        return id, entry
    return None, None


def pop_entry_if_exists():
    if "entry" in session:
        session.pop("id")
        session.pop("entry")
