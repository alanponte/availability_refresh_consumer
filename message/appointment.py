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
    """Message to send to SNS when an appointment has been created.

    Example:

    ```
        {
            user_id: 'e863b41f-acdc-4eff-93eb-b47a60879dec',
            fleet_id: 'e35396fb-053e-4479-b7e2-2ff207073485',
            store_id: '4fe35389-f3fe-4996-ab48-86e5225795f9',
            service_windows: {
                start_time: 1,
                service_completion_time: 2
                end_time:3,
                jobs: [job1, job2, ..],
                availability_asset: '487792fe-b115-4889-9299-2404f7e2807d'
            }
        }
    ```
    """
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
