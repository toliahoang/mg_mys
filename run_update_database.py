from utils.update_database import Singleton
from config.mystique_config import *


s1 = Singleton(**access_dict)
s1.show_db(select_sql)
# s1.insert_db(insert_event_sql)
