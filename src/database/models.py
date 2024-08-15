from sqlalchemy import Column, Integer, String, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class Member(Base):
    __tablename__ = "members"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    room_id = Column(Integer, ForeignKey('rooms.url'), nullable=False)

    room = relationship("Room", back_populates="members")

class Room(Base):
    __tablename__ = "rooms"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    url = Column(String, nullable=False)
    members = relationship("Member", back_populates="room", cascade="all, delete-orphan")
    
engine = create_engine('sqlite:///sqlite.db')

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

session = Session()