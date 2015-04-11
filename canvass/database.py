from peewee import *
import datetime
import config

# Connect to database using credentials from config.py
# Edit the following statement to change DB type
db = MySQLDatabase(host=config.dbhost, user=config.dbuser, password=config.dbpass, database=config.dbname)
# Create models
class BaseModel(Model):
    class Meta:
        database = db

class Record(BaseModel):
    location = CharField() # coords
    ip = TextField() # ip
    total_storage = DecimalField() # GiB
    total_memory = IntegerField() # kB
    linux_distro = CharField() # e.g Fedora
    linux_distro_version = CharField() # e.g 21
    linux_distro_name = CharField() # e.g Twenty One
    kernel_release = CharField() # e.g 3.18.3-201.fc21.x86_64
    cpus = TextField() # e.g [' Intel(R) Core(TM) i5-4200U CPU @ 1.60GHz', ' Intel(R) Core(TM) i5-4200U CPU @ 1.60GHz']
    machine_arch = CharField() # e.g x86_64
    processor_arch = CharField() # e.g x86_64
    num_cpus = IntegerField() # e.g 4
