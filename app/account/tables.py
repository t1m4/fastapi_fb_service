from sqlalchemy import BigInteger, Column, Identity, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship

from app.db import Base


class Account(Base):
    __tablename__ = "account"

    id = Column(BigInteger, Identity(), primary_key=True)
    account_id = Column(String)
    company_id = Column(BigInteger, nullable=False)
    name = Column(String, nullable=False)
    businesses = Column(ARRAY(String))

    campaigns = relationship("Campaign", back_populates="credential", cascade="all, delete-orphan")
