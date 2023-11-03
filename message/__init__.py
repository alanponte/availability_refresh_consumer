from dataclasses import dataclass
from enum import Enum


class RefreshAvailabilityEvent(str, Enum):
    """An SNS event for availability messages."""
    APPOINTMENT_SCHEDULED = 'APPOINTMENT_SCHEDULED'
    APPOINTMENT_CANCELED = 'APPOINTMENT_CANCELED'
    APPOINTMENT_RESCHEDULED = 'APPOINTMENT_RESCHEDULED'
    AVAILABILITY_REQUEST = 'AVAILABILITY_REQUEST'
    ASSET_UPDATE = 'ASSET_UPDATE'


@dataclass(frozen=True)
class RootMessage:
    event_type: RefreshAvailabilityEvent
