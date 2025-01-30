from sqlalchemy import Column, Integer, Float, String
from compartidos.database import Base

class PostcodeEntry(Base):
    __tablename__ = 'postcodes'
    
    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    postcode = Column(String, nullable=True)
