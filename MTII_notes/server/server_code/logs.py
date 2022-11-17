from server.database import DataBase
from datetime import datetime

date_a = datetime(2022, 11, 13, 13, 15, 40)
date_a_str = str(date_a)
date_a = datetime.fromisoformat(date_a_str)
date_b = datetime(2020, 11, 13, 13, 15, 40)
interval = (datetime(2019, 11, 13, 13, 15, 40),
            datetime(2023, 11, 13, 14, 15, 40))

print((7, {1: 1, 2: 2}))
a = DataBase()
a.create_entry("Blarg1", ["Real", "Fake"], date_a)
a.create_entry("Blarg1", ["Real", "Real"], date_b)
a.create_entry("Blarg1", ["Real", "Real"], date_a)
a.edit_entry(3, "Blarg2", ["Real", "Real"], date_a)