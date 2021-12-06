import psycopg2
from datetime import datetime
import time
import os

from faker import Faker

faker_instance = Faker(['en_US'])

dsn = (
    "dbname={dbname} "
    "user={user} "
    "password={password} "
    "port={port} "
    "host={host} ".format(
        dbname="pedidos",
        user=os.environ["USER"],
        password=os.environ["PASSWORD"],
        port=5432,
        host=os.environ["HOST"],
    )
)

conn = psycopg2.connect(dsn)
print("connected")
conn.set_session(autocommit=True)
cur = conn.cursor()


def get_update_query():
    cur.execute("select customer_id from customers order by random() limit 1")
    customer_id = cur.fetchone()[0]
    return f"update customers set phone = '{faker_instance.phone_number()}', updated_at = '{datetime.utcnow()}' where customer_id='{customer_id}'"


while True:
    query = get_update_query()
    cur.execute(query)
    print(query)
    time.sleep(5)