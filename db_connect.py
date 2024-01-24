import sqlite3


def add_items(cur, o_date=None, o_temp=None, room_temp=None, eng_price=None, eng_date=None, boi_date=None, boi_on=None):
    if o_date is not None and o_temp is not None:
        cur.execute("INSERT INTO out_temp(date, temp) VALUES(:ins_date, :ins_temp)", {"ins_date": o_date, "ins_temp": o_temp})
    if room_temp is not None:
        cur.execute("INSERT INTO room_temp(temp) VALUES(:ins_temp)", {"ins_temp": room_temp})
    if eng_price is not None and eng_date is not None:
        cur.execute("INSERT INTO energy_price(date, price) VALUES(:eng_date, :eng_price)", {"eng_date": eng_date, "eng_price": eng_price})
    if boi_date is not None and boi_on is not None:
        cur.execute("INSERT INTO boiler_schedule(date, boiler_on) VALUES(:boi_date, :boi_on)", {"boi_date": boi_date, "boi_on": boi_on})


def init_con(cur):
    cur.execute("CREATE TABLE IF NOT EXISTS out_temp(id INTEGER PRIMARY KEY, date DATE, temp TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS room_temp(id INTEGER PRIMARY KEY, date DATE DEFAULT CURRENT_TIMESTAMP, temp TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS energy_price(id INTEGER PRIMARY KEY, date DATE, price TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS boiler_schedule(id INTEGER PRIMARY KEY, date DATE, boiler_on BOOLEAN)")


def check_date_on_last_row(cur, table_name=None):
    if table_name == "out_temp":
        res = cur.execute("SELECT date FROM out_temp WHERE id = (SELECT max(id) from out_temp)")
        date = res.fetchone()[0]
        return date
    if table_name == "energy_price":
        res = cur.execute("SELECT date FROM energy_price WHERE id = (SELECT max(id) from energy_price)")
        date = res.fetchone()[0]
        return date


def get_data(cur, table_name=None, row_nums=None):
    if table_name == "out_temp":
        res = cur.execute("SELECT date, temp FROM out_temp WHERE id > ((SELECT max(id) FROM out_temp) - :row_nums)", {"row_nums": row_nums})
        return res.fetchall()
    if table_name == "energy_price":
        res = cur.execute("SELECT date, price FROM energy_price WHERE id > ((SELECT max(id) FROM energy_price) - :row_nums)", {"row_nums": row_nums})
        return res.fetchall()
    if table_name == "room_temp":
        res = cur.execute("SELECT date, temp FROM room_temp WHERE id > ((SELECT max(id) FROM room_temp) - :row_nums)", {"row_nums": row_nums})
        return res.fetchall()

#  Connecting to our database and dumping data. Queries coming later.
def talk_to_db(o_date=None, o_temp=None, room_temp=None, fetch=False, table_name=None, row_nums=None, getting_data=False, eng_price=None, eng_date=None, boi_date=None, boi_on=None):
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    with con:
        init_con(cur)
        if fetch is True:
            return check_date_on_last_row(cur, table_name)
        if getting_data is True:
            return get_data(cur, table_name, row_nums)
        add_items(cur, o_date, o_temp, room_temp, eng_price, eng_date, boi_date, boi_on)
        con.commit()
