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

# connection_str = f'mysql+pymysql://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}'
connection_str = f'sqlite:///./database.db'
connection_str = f'mysql://zp3dtdcvamb8q9az:ryrfis37bzow9fbi@d6rii63wp64rsfb5.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/j1kx10jepegkf2gs'

database = databases.Database(connection_str)
metadata = sqlalchemy.MetaData()
engine = sqlalchemy.create_engine(connection_str)
