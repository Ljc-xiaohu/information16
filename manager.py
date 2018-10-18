from flask import Flask,session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
import redis
from flask_wtf import CSRFProtect

app = Flask(__name__)

class Config(object):
    DEBUG = True

    SECRET_KEY = "hsdfgfgafv"

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:mysql@localhost:3306/information16"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379

    SESSION_TYPE = "redis"
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST,port=REDIS_PORT)
    SESSION_USE_SIGNER = True
    PERMANENT_SESSION_LIFETIME = 3600*24*2


app.config.from_object(Config)

db = SQLAlchemy(app)

redis_store = redis.StrictRedis(host=Config.REDIS_HOST,port=Config.REDIS_PORT,decode_responses=True)

CSRFProtect(app)

Session(app)

@app.route('/')
def hello_world():

    redis_store.set("name","laowang")
    print(redis_store.get("name"))

    session["age"] = "13"
    print(session.get("age"))

    return "helloworld100"

if __name__ == '__main__':
    app.run()