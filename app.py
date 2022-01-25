from flask import Flask
import random
import pymysql
import os
import json

app = Flask(__name__)


@app.route('/')
def hello_world():
    start = getMaxId()
    print('start = ' + str(start))
    randomRange = random.randint(0, 20000)
    print('randomRange = ' + str(randomRange))
    end = start + randomRange
    print('end = ' + str(end))

    prettyId = random.randint(start, end)
    prettyId_str = changeBase(prettyId, 62)
    print('prettyId = ' + prettyId_str)
    setMaxId(prettyId)
    return json.dumps({"data": {"prettyId": prettyId_str}})


def changeBase(n, b):
    baseList = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    x, y = divmod(n, b)
    if x > 0:
        return changeBase(x, b) + baseList[y]
    else:
        return baseList[y]


def getDb():
    db = pymysql.connect(host='10.0.0.12',
                         port=3306,
                         user='pretty_id',
                         password=os.environ.get('mysql_password'),
                         database='pretty_id')
    return db


def getMaxId():
    db = getDb()
    cursor = db.cursor()
    cursor.execute('SELECT max_id FROM t_max_id')
    max_id = cursor.fetchone()[0]
    db.close()
    return max_id


def setMaxId(max_id):
    db = getDb()
    cursor = db.cursor()
    cursor.execute('UPDATE t_max_id SET max_id = ' + str(max_id))
    db.commit()
    cursor.close()
    db.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
