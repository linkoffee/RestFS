from sqlalchemy import Column, Integer, String, DateTime

from app.db.session import Base


class File(Base):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    fname = Column(String, nullable=False)
    fsize = Column(Integer, nullable=False)
    mdt = Column(DateTime, nullable=False)
