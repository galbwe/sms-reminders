import os
from uuid import uuid4
from datetime import datetime, timedelta

from app import Reminder, ReminderSchema, db

init_db_csv = os.environ.get('INIT_DB_CSV') or '../../data/init_db.csv'

db.create_all()


with open(init_db_csv) as f:
    lines = f.readlines()
    columns = lines[0][:-1].split(',') # [:-1] removes trailing \n
    print(columns)
    reminders = []
    for line in lines[1:]:
        field_values = line[:-1].split(',')
        print(field_values)
        reminder = dict(zip(columns, field_values))
        reminder['to'] = '+' + str(reminder['to'])
        reminder['from_'] = '+' + str(reminder['from_'])
        reminder['time'] = str(datetime.strptime(reminder['time'], '%m/%d/%y %H:%M %p'))
        reminder['is_recurring'] = bool(int(reminder['is_recurring']))
        print(reminder)
        print(ReminderSchema().load(reminder))
        db.session.add(ReminderSchema().load(reminder))

    print(reminders)
    db.session.commit()
