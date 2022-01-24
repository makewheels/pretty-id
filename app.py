from flask import Flask
import random
import pymysql

app = Flask(__name__)


@app.route('/')
def hello_world():
    start = 0
    randomRange = random.randint(0, 100001)
    end = start + randomRange

    result = random.randint(0, end)
    return changeBase(result, 62)


baseList = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'


def changeBase(n, b):
    x, y = divmod(n, b)
    if x > 0:
        return changeBase(x, b) + baseList[y]
    else:
        return baseList[y]


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
