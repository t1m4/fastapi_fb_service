from sqlalchemy import BigInteger, Column, ForeignKey, Identity, String

from app.db import Base


class Campaign(Base):
    __tablename__ = "campaign"

    id = Column(BigInteger, Identity(), primary_key=True)
    credential_id = Column(BigInteger, ForeignKey("account.id", ondelete="RESTRICT"), nullable=False)
    name = Column(String, nullable=False)


class AdSet(Base):
    __tablename__ = "adset"

    id = Column(BigInteger, Identity(), primary_key=True)
    campaign = Column(BigInteger, ForeignKey("campaign.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)


class Ad(Base):
    __tablename__ = "ad"

    id = Column(BigInteger, Identity(), primary_key=True)
    ad_set = Column(BigInteger, ForeignKey("adset.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
