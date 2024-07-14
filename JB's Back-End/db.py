from sqlalchemy import create_engine, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker




# create sqlalchemy engine

#local network
engine = create_engine('mysql+mysqlconnector://drew:drew@192.168.1.2:3306/thesis_system')


#hotspot
#engine = create_engine('mysql+mysqlconnector://drew:drew@172.20.10.5:3306/thesis_system')

#create session class
Session = sessionmaker(bind=engine)
