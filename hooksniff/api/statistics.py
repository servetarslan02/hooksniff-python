# Adapted for HookSniff API
import typing as t
from dataclasses import dataclass

from ..models import AggregateEventTypesOut, AppUsageStatsIn, AppUsageStatsOut
from .common import ApiBase, BaseOptions, serialize_params


@dataclass
class StatisticsAggregateAppStatsOptions(BaseOptions):
    idempotency_key: t.Optional[str] = None

    def _header_params(self) -> t.Dict[str, str]:
        return serialize_params(
            {
                "idempotency-key": self.idempotency_key,
            }
        )


class StatisticsAsync(ApiBase):
    async def get_account_stats(self) -> dict:
        """Get account statistics."""
        response = await self._request_asyncio(
            method="get",
            path="/v1/stats",
            path_params={},
        )
        return response.json()


class Statistics(ApiBase):
    def get_account_stats(self) -> dict:
        """Get account statistics."""
        response = self._request_sync(
            method="get",
            path="/v1/stats",
            path_params={},
        )
        return response.json()
