import databases
import sqlalchemy
import ormar

config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'passwd1234',
    'database': 'chat_API'
}

db_user = config.get('user')
db_pwd = config.get('password')
db_host = config.get('host')
db_port = config.get('port')
db_name = config.get('database')

connection_str = f'mysql+pymysql://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}'

database = databases.Database(connection_str)
metadata = sqlalchemy.MetaData()