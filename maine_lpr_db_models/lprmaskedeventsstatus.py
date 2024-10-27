from enum import Enum

from base import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class LprMaskedEventStatusesEnum(Enum):
    PENDING_DATA_ENTRY: int = 1
    RESERVED_FOR_DATA_ENTRY: int = 2
    PENDING_DELIVERY: int = 3
    DELIVERED: int = 4
    DELIVERY_FAILED: int = 5


class LprMaskedEventStatuses(Base):
    __tablename__ = "lpr_masked_event_statuses"
    __table_args__ = {"schema": "lprdb"}

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(50))

    events = relationship("LprMaskedEvents", back_populates="status")
