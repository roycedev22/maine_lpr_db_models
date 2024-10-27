from enum import Enum

from base import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class LprCameraVendorsEnum(Enum):
    OPENALPR: int = 1
    LAB18: int = 2
    SURVISION: int = 3


class LprCameraVendors(Base):
    __tablename__ = "lpr_camera_vendors"
    __table_args__ = {"schema": "lprdb"}

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(50))

    events = relationship("LprMaskedEvents", back_populates="status")
