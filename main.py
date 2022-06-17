import numpy as np
import sqlite3
import time
import io
import concurrent.futures
from threading import Semaphore

lock = Semaphore(10)


def adapt_array(arr):
    out = io.BytesIO()
    np.save(out, arr)
    out.seek(0)
    return sqlite3.Binary(out.read())


def convert_array(text_):
    out = io.BytesIO(text_)
    out.seek(0)
    return np.load(out, allow_pickle=True)


#  When inserting data, the array Convert to text Insert
sqlite3.register_adapter(np.ndarray, adapt_array)

#  When querying data, the text Convert to array
sqlite3.register_converter("array", convert_array)


def convert_to_numbers(data):
    batch_token_list = [t.split() for t in data]
    num_list = [[[ord(char) for char in token] for token in token_list] for token_list in batch_token_list]
    num_array_list = [np.array([items], dtype=object) for items in num_list]
    sum_array_list = [np.array([sum(single_word) for single_word in sentence], dtype=object) for sentence in num_list]
    return data, num_array_list, sum_array_list


def search(data, r):
    search_text, search_numbers, search_sum = convert_to_numbers([data])
    for item in search_numbers:
        sn = item

    lock.acquire()
    con = sqlite3.connect("vectorized.db", detect_types=sqlite3.PARSE_DECLTYPES)
    c = con.cursor()
    c.execute("SELECT rowid, text FROM vectors WHERE numbers = ? and rowid BETWEEN ? and ?", (sn, r[0], r[1]))
    items = c.fetchall()
    for item in items:
        print(f"{item[0]}, {item[1]}")
    con.close()
    lock.release()


def create_table():
    con = sqlite3.connect("vectorized.db", detect_types=sqlite3.PARSE_DECLTYPES)
    c = con.cursor()
    c.execute("""CREATE TABLE vectors (
    text TEXT,
    numbers array,
    sum_of_words array
    )""")
    con.commit()
    con.close()


def delete_table():
    con = sqlite3.connect("vectorized.db", detect_types=sqlite3.PARSE_DECLTYPES)
    c = con.cursor()
    c.execute("DROP TABLE vectors")
    con.commit()
    con.close()


def insert(t, n, s):
    con = sqlite3.connect("vectorized.db", detect_types=sqlite3.PARSE_DECLTYPES)
    c = con.cursor()
    c.executemany("INSERT INTO vectors VALUES (?,?,?)", zip(t, n, s))
    con.commit()
    con.close()


def fetch():
    con = sqlite3.connect("vectorized.db", detect_types=sqlite3.PARSE_DECLTYPES)
    c = con.cursor()
    c.execute("SELECT rowid, text numbers FROM vectors")
    items = c.fetchall()
    print(items)
    con.close()


def threaded_search(search_text):
    con = sqlite3.connect("vectorized.db", detect_types=sqlite3.PARSE_DECLTYPES)
    c = con.cursor()
    c.execute("SELECT COUNT(*) FROM vectors")
    total_rows = c.fetchone()[0]
    con.close()
    tp_list = [
               [0, int(total_rows/10)],
               [int(total_rows/10) + 1, int(2*total_rows/10)],
               [int(2 * total_rows / 10) + 1, int(3 * total_rows / 10)],
               [int(3 * total_rows / 10) + 1, int(4 * total_rows / 10)],
               [int(4 * total_rows / 10) + 1, int(5 * total_rows / 10)],
               [int(5 * total_rows / 10) + 1, int(6 * total_rows / 10)],
               [int(6 * total_rows / 10) + 1, int(7 * total_rows / 10)],
               [int(7 * total_rows / 10) + 1, int(8 * total_rows / 10)],
               [int(8 * total_rows / 10) + 1, int(9 * total_rows / 10)],
               [int(9 * total_rows / 10) + 1, total_rows]
               ]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(search, search_text, tp) for tp in tp_list]


st = time.time()

with open("data.txt") as file:
    batch = file.readlines()

# delete_table()
create_table()
text, num, sum_ = convert_to_numbers(batch)
insert(text, num, sum_)
# fetch()
# search("Hello world.", [1, 126564])
threaded_search("Hello world.")
f = time.time()

print(f"total time: {f - st}")

