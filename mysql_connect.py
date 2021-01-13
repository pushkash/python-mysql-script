import json
import mysql.connector
from mysql.connector import errorcode

from config import config


insert_cmd = (f"INSERT INTO {config['database']} "
               "(idmutasi, tgl, pkl, desc1, desc2, vendor, amount, ftype) "
               "VALUES (%(idmutasi)s, %(tgl)s, %(pkl)s, %(desk1)s, %(desk2)s, %(vendor)s, %(amount)s, %(ftype)s)"
               )


def insert_data(data):
    try:
        cnx = mysql.connector.connect(**config)

        cursor = cnx.cursor()

        for el in json.loads(data):
            el_data = {
                'idmutasi': el.get('desc2') + el.get('vendor') + el.get('amount') + el.get('ftype'),
                'tgl': el.get('tgl'),
                'pkl': el.get('pkl'),
                'desc1': el.get('desc1'),
                'desc2': el.get('desc2'),
                'vendor': el.get('vendor'),
                'amount': el.get('amount'),
                'ftype': el.get('ftype')
            }

            cursor.execute(insert_cmd, el_data)
            cnx.commit()

        cursor.close()
        cnx.close()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Invalid user or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
