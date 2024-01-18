import sqlite3


def add_items(cur, o_date=None, o_temp=None, room_temp=None):
    if o_date is not None and o_temp is not None:
        cur.execute("INSERT INTO out_temp(date, temp) VALUES(:ins_date, :ins_temp)", {"ins_date": o_date, "ins_temp": o_temp})
    if room_temp is not None:
        cur.execute("INSERT INTO room_temp(temp) VALUES(:ins_temp)", {"ins_temp": room_temp})


def init_con(cur):
    cur.execute("CREATE TABLE IF NOT EXISTS out_temp(id INTEGER PRIMARY KEY, date DATE, temp TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS room_temp(id INTEGER PRIMARY KEY, date DATE DEFAULT CURRENT_TIMESTAMP, temp TEXT)")


#  Connecting to our database and dumping data. Queries coming later.
def talk_to_db(o_date=None, o_temp=None, room_temp=None):
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    with con:
        init_con(cur)
        add_items(cur, o_date, o_temp, room_temp)
        con.commit()
