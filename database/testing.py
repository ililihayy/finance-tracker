# Copyright (c) 2025 ililihayy. All rights reserved.

import datetime

from .create_database import conn, create_full_database
from .utils import Utils as Ut

if __name__ == "__main__":
    create_full_database()
    Ut.add_user("bro")
    Ut.add_expense("bro", "Food", 150.75, datetime.datetime.now(datetime.UTC).strftime("%d-%m-%Y"))
    Ut.add_user_category("john_doe", "Utilities")

conn.commit()
conn.close()
