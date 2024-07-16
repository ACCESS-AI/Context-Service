from peewee import PostgresqlDatabase, Model, IntegerField, TextField, fn
from datetime import datetime
from playhouse.postgres_ext import ArrayField
import os



database_name = os.getenv('CHATBOT_DB_NAME', 'chatbot')
username = os.getenv('CHATBOT_DB_USER', 'postgres')
password = os.getenv('CHATBOT_DB_PASSWORD', 'postgres')
host = os.getenv('CHATBOT_DB_HOST', 'localhost')
port = os.getenv('CHATBOT_DB_PORT', '5555')

database = PostgresqlDatabase(database_name, user=username, password=password, host=host, port=port)

class BaseModel(Model):
    class Meta:
        database = database

class ExtractionStatistic(BaseModel):
    timestamp = IntegerField(default=int(datetime.now().timestamp())) 
    course_slug = TextField()
    successfull_files = ArrayField(TextField)  
    unsuccessfull_files = ArrayField(TextField)  


def initialize_database():
    database.create_tables([ExtractionStatistic], safe=True)



