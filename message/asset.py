from dataclasses import dataclass
from enum import Enum
from typing import List

from message import RootMessage


class StoreAssetType(str, Enum):
    """Represents a type of asset at a store."""
    SERVICE_BAY = 'SERVICE_BAY'


class StoreAssetEventAction(str, Enum):
    """Represents an action upon a store's asset."""
    DELETED = 'DELETED'
    HOURS_UPDATED = 'HOURS_UPDATED'
    ADDED = 'ADDED'


@dataclass(frozen=True)
class AssetUpdatedMessage(RootMessage):
    """A message to send to SNS to indicate that asset(s) at a store has been updated."""
    andgo_correlation_id: str
    store_id: str
    user_id: str
    fleet_id: str
    assets: List['StoreAssetUpdatedEvent']


@dataclass(frozen=True)
class StoreAssetUpdatedEvent:
    id: str
    type: StoreAssetType
    action: StoreAssetEventAction
