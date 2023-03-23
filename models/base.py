from peewee import Model
from playhouse.mysql_ext import MySQLDatabase
from os import getenv

mysql_db = MySQLDatabase(user=getenv('BD_USER'), password=getenv('BD_PASS'), host=getenv('BD_HOST'), database=getenv('BD_NAME'))

class BaseModel(Model):
    class Meta:
        database = mysql_db