# Copyright (c) 2025 ililihayy. All rights reserved.

import datetime

from .create_database import create_full_database
from .utils import Utils as Ut

if __name__ == "__main__":
    create_full_database()
    Ut.add_user("bro2344", "12email@gail", "pas11")
    Ut.add_expense("bro2344", "Food", 150.75, datetime.datetime.now(datetime.UTC).strftime("%d-%m-%Y"))
    Ut.add_user_category("bro2344", "Utilities2")
