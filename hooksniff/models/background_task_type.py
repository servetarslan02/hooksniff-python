from enum import Enum


class BackgroundTaskType(str, Enum):
    ENDPOINT_RECOVER = "endpoint.recover"
    ENDPOINT_REPLAY = "endpoint.replay"
    ENDPOINT_BULK_REPLAY = "endpoint.bulk-replay"
    APPLICATION_STATS = "application.stats"
    APPLICATION_PURGE_CONTENT = "application.purge_content"
    EVENT_TYPE_AGGREGATE = "event-type.aggregate"
