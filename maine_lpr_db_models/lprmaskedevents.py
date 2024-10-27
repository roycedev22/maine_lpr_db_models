from datetime import datetime, timezone

from base import Base
from lprmaskedeventsstatus import LprMaskedEventStatuses
from sqlalchemy import (
    TIMESTAMP,
    BigInteger,
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    text,
)
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import relationship


def utc_now():
    return datetime.now(timezone.utc)


class LprMaskedEvents(Base):
    __tablename__ = "lpr_masked_events"
    __table_args__ = {"schema": "lprdb"}

    id = Column(BigInteger, primary_key=True)
    lpr_event = Column(LONGTEXT, nullable=False)
    message_id = Column(String(36), nullable=False, unique=True)
    camera_vendor_id = Column(
        Integer, ForeignKey("lprdb.lpr_camera_vendors.id"), nullable=False
    )
    plate_number = Column(String(50), nullable=True)
    plate_state = Column(String(10), nullable=True)
    status_id = Column(
        Integer, ForeignKey("lprdb.lpr_masked_event_statuses.id"), nullable=False
    )
    reserved_by = Column(String(36), nullable=True)
    reserved_at = Column(TIMESTAMP, nullable=True)
    completed_at = Column(TIMESTAMP, nullable=True)
    delivered_at = Column(TIMESTAMP, nullable=True)
    delivered = Column(Boolean, nullable=True, server_default="0", default=0)
    created_at = Column(
        TIMESTAMP,
        nullable=False,
        default=utc_now,
        server_default=text("CURRENT_TIMESTAMP"),
    )
    updated_at = Column(
        TIMESTAMP,
        nullable=True,
        default=utc_now,
        onupdate=utc_now,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        # server_onupdate=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
    )

    status = relationship(LprMaskedEventStatuses.__name__, back_populates="events")
    status = relationship(LprMaskedEventStatuses.__name__, back_populates="events")
