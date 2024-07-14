from sqlalchemy import create_engine, select, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import subprocess
import datetime





# create sqlalchemy engine

#local network
#engine = create_engine('mysql+mysqlconnector://drew:drew@192.168.1.9:3306/thesis_system')

#radmin
engine = create_engine('mysql+mysqlconnector://drew:drew@192.168.1.2:3306/thesis_system')

#engine = create_engine('mysql+mysqlconnector://drew:drew@localhost:3306/thesis_system')
#hotspot
#engine = create_engine('mysql+mysqlconnector://drew:drew@172.20.10.5:3306/thesis_system')

#create session class
Session = sessionmaker(bind=engine)


def backup_db():
    db_name = 'thesis_system'
    today_date = datetime.datetime.now().strftime('%b%d%y%H%M')
    file_name = f'BU-{db_name}-{today_date}.sql'
    mysql_dump = r"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqldump.exe"
    engine = create_engine('mysql+mysqlconnector://drew:drew@192.168.1.2:3306')
    backup_command = f'"{mysql_dump}" -h 192.168.1.2 -u drew -pdrew {db_name} > {file_name}'

    try:
        subprocess.run(backup_command, shell=True, check=True)
        print("SUCCESS")
    except subprocess.CalledProcessError as e:
        print(e)

backup_db()
"""
inspector = inspect(engine)
table_names = inspector.get_table_names() """