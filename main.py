from dataclasses import dataclass, asdict
from enum import Enum

from typing import Optional, List

from logger import get_logger
from sns.sns import SNS
from utils import create_random_uuid_str

_LOGGER = get_logger()

DEFAULT_DAYS_OFFSET = 6

AVAILABILITY_REFRESH_SNS_TOPIC = 'availability-update-dev.fifo'

AVAILABILITY_REFRESH_SNS_TOPIC_ARN = 'arn:aws:sns:us-west-2:612996534754:availability-update-dev.fifo'


class RefreshAvailabilitySubject(str, Enum):
    """An SNS Subject for availability messages."""
    APPOINTMENT_SCHEDULED = 'APPOINTMENT_SCHEDULED'
    APPOINTMENT_CANCELED = 'APPOINTMENT_CANCELED'
    APPOINTMENT_RESCHEDULED = 'APPOINTMENT_RESCHEDULED'
    AVAILABILITY_REQUEST = 'AVAILABILITY_REQUEST'
    ASSET_UPDATE = 'ASSET_UPDATE'


class StoreAssetType(str, Enum):
    """Represents a type of asset at a store."""
    SERVICE_BAY = 'SERVICE_BAY'


@dataclass(frozen=True)
class AppointmentScheduledMessage:
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
class AvailabilityRequestedMessage:
    """Message to send to SNS for a fetch availability request."""
    andgo_correlation_id: str
    requested_day: str
    vin: str
    user_id: str
    fleet_id: str
    store_id: str
    jobs: List[str]


@dataclass(frozen=True)
class AppointmentServiceWindow:
    """A service window represents one or more jobs being performed within an asset
    (e.g. service bay)."""
    andgo_correlation_id: str
    start_time: int
    service_completion_time: int
    end_time: int
    jobs: List[str]
    availability_asset: str


@dataclass(frozen=True)
class AssetUpdatedMessage:
    """A message to send to SNS to indicate that asset(s) at a store has been updated."""
    andgo_correlation_id: str
    store_id: str
    user_id: str
    fleet_id: str
    assets: List['StoreAsset']


@dataclass(frozen=True)
class StoreAsset:
    id: str
    type: StoreAssetType


def _create_availability_refresh_sns_message(
        andgo_correlation_id: str,
        store_id: str,
        user_id: str,
        fleet_id: str,
        days_offset: Optional[int] = DEFAULT_DAYS_OFFSET,
):
    """Create an availability refresh message to publish to SNS"""
    return dict(
        andgo_correlation_id=andgo_correlation_id,
        store_id=store_id,
        user_id=user_id,
        fleet_id=fleet_id,
        days_offset=days_offset
    )


def _send_appointment_scheduled_message(sns_client: SNS):
    """Send a test `AppointmentScheduled` message to the SNS topic."""
    appointment_scheduled_message = AppointmentScheduledMessage(
        user_id=create_random_uuid_str(),
        fleet_id=create_random_uuid_str(),
        store_id=create_random_uuid_str(),
        service_windows=[
            AppointmentServiceWindow(
                andgo_correlation_id=create_random_uuid_str(),
                start_time=1698920446,
                service_completion_time=1698924046,
                end_time=1698960046,
                availability_asset=create_random_uuid_str(),
                jobs=[create_random_uuid_str(), create_random_uuid_str()]
            )
        ]
    )
    print(f'Publishing `AppointmentScheduledMessage` to topic')
    response = sns_client.publish(
        subject=RefreshAvailabilitySubject.APPOINTMENT_SCHEDULED,
        message=asdict(appointment_scheduled_message)
    )
    print(f'Successfully published message {appointment_scheduled_message} to topic: {AVAILABILITY_REFRESH_SNS_TOPIC_ARN} '
          f'Response: {response}')


def _send_availability_requested_message(sns_client: SNS):
    """Send a test `AvailabilityRequested` message to the SNS topic."""
    availability_requested_message = AvailabilityRequestedMessage(
        andgo_correlation_id=create_random_uuid_str(),
        user_id=create_random_uuid_str(),
        fleet_id=create_random_uuid_str(),
        store_id=create_random_uuid_str(),
        vin='2HHFD55707H200235',
        jobs=[create_random_uuid_str(), create_random_uuid_str()],
        requested_day='2023-11-02'
    )
    print(f'Publishing `AvailabilityRequestedMessage` to topic')
    response = sns_client.publish(
        subject=RefreshAvailabilitySubject.AVAILABILITY_REQUEST,
        message=asdict(availability_requested_message)
    )

    print(
        f'Successfully published message {availability_requested_message} to topic: {AVAILABILITY_REFRESH_SNS_TOPIC_ARN} '
        f'Response: {response}')


def _send_asset_updated_message(sns_client: SNS):
    """Send a test `AssetUpdated` message to the SNS topic."""
    asset_updated_message = AssetUpdatedMessage(
        andgo_correlation_id=create_random_uuid_str(),
        user_id=create_random_uuid_str(),
        fleet_id=create_random_uuid_str(),
        store_id=create_random_uuid_str(),
        assets=[StoreAsset(id=create_random_uuid_str(), type=StoreAssetType.SERVICE_BAY)]
    )

    print(f'Publishing `AssetUpdatedMessage` tp topic')
    response = sns_client.publish(
        subject=RefreshAvailabilitySubject.ASSET_UPDATE,
        message=asdict(asset_updated_message)
    )

    print(
        f'Successfully published message {asset_updated_message} to topic: {AVAILABILITY_REFRESH_SNS_TOPIC_ARN} '
        f'Response: {response}')


def main():
    print(f'Creating SNS client for topic {AVAILABILITY_REFRESH_SNS_TOPIC_ARN}')
    sns_client = SNS(AVAILABILITY_REFRESH_SNS_TOPIC_ARN)

    # Appointment Scheduled
    _send_appointment_scheduled_message(sns_client)

    # Availability Requested
    _send_availability_requested_message(sns_client)

    _send_asset_updated_message(sns_client)


if __name__ == '__main__':
    main()
