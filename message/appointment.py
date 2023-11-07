from dataclasses import dataclass
from typing import List

from message import RootMessage


@dataclass(frozen=True)
class AppointmentCanceledMessage(RootMessage):
    user_id: str
    fleet_id: str
    store_id: str
    appointment_id: str


@dataclass(frozen=True)
class AppointmentScheduledMessage(RootMessage):
    """Message to send to SNS when an appointment has been created."""
    user_id: str
    fleet_id: str
    store_id: str
    service_windows: List['AppointmentServiceWindow']


@dataclass(frozen=True)
class AppointmentServiceWindow:
    """A service window represents one or more jobs being performed within an asset
    (e.g. service bay)."""
    start_time: int
    service_completion_time: int
    end_time: int
    jobs: List[str]
    availability_asset: str
