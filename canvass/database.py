from peewee import *
import datetime
import config

# Connect to database using credentials from config.py
db = MySQLDatabase(host=config.dbhost, user=config.dbuser, password=config.dbpass, database=config.dbname)
# Create models
class BaseModel(Model):
    class Meta:
        database = db

class Record(BaseModel):
    ip = CharField()
