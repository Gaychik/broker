from sqlalchemy import Column,Integer,String,create_engine,ForeignKey,and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker,DeclarativeBase,relationship

class Base(DeclarativeBase):
    pass

class Message(Base):
    __tablename__="messages"
    message_id=Column(Integer,primary_key=True,autoincrement=True)
    command=Column(String)
    device_id=Column(Integer)
    status=Column(String)
    result=Column(String)
    from_id=Column(Integer,ForeignKey("services.id"))
    to_id=Column(Integer,ForeignKey("services.id"))
    service_from=relationship('Service',backref='sent_messages',foreign_keys='Message.from_id')
    service_to=relationship('Service',backref='received_messages',foreign_keys='Message.to_id')
    
class Service(Base):
    __tablename__="services"
    id = Column(Integer,primary_key=True,autoincrement=True) 
    host = Column(String)
    port = Column(Integer)
    name = Column(String)
    
    def __repr__(self):
        return {'id':self.id,'host':self.host,'port':self.port}
     
engine = create_engine("sqlite:///info.db")
Session = sessionmaker(bind = engine)
def get_db():
    try:
        yield session
    finally:
        session.close()

session =Session()
Base.metadata.create_all(bind=engine)