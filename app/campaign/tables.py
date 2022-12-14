from sqlalchemy import BigInteger, Column, ForeignKey, Identity, String
from sqlalchemy.orm import relationship

from app.db import Base


class Campaign(Base):
    __tablename__ = "campaign"

    id = Column(BigInteger, Identity(), primary_key=True)
    credential_id = Column(BigInteger, ForeignKey("account.id", ondelete="RESTRICT"), nullable=False)
    name = Column(String, nullable=False)

    credential = relationship("Account", back_populates="campaigns")
    adsets = relationship("AdSet", back_populates="campaign", cascade="all, delete-orphan")


class AdSet(Base):
    __tablename__ = "adset"

    id = Column(BigInteger, Identity(), primary_key=True)
    campaign_id = Column(BigInteger, ForeignKey("campaign.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)

    campaign = relationship("Campaign", back_populates="adsets")
    ads = relationship("Ad", back_populates="ad_set", cascade="all, delete-orphan")


class Ad(Base):
    __tablename__ = "ad"

    id = Column(BigInteger, Identity(), primary_key=True)
    ad_set_id = Column(BigInteger, ForeignKey("adset.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)

    ad_set = relationship("AdSet", back_populates="ads")
