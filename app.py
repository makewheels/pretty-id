    from flask import Flask
    import random
    import pymysql
    import os

    app = Flask(__name__)

    @app.route('/')
    def hello_world():
        start = getMaxId()
        randomRange = random.randint(0, 100000)
        print('randomRange = ' + str(randomRange))
        end = start + randomRange

        max_id = random.randint(0, end)
        max_id_str = changeBase(max_id, 62)

        setMaxId(max_id)
        return max_id_str


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
        db=getDb()
        cursor = db.cursor()
        cursor.execute('SELECT max_id FROM t_max_id')
        max_id = cursor.fetchone()[0]
        print('max_id = ' + str(max_id))
        db.close()
        return max_id


    def setMaxId(max_id):
        db=getDb()
        cursor = db.cursor()
        cursor.execute('UPDATE t_max_id SET max_id = ' + str(max_id))
        db.commit()
        cursor.close()
        db.close()


    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=9000)
