from db_connect import talk_to_db
import datetime
import random



#  Here we should read temp from raspberry, lets have random generator until
deg = round(random.uniform(17, 23), 2)

talk_to_db(room_temp=deg)
