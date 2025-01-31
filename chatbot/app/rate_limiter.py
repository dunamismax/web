# chatbot/app/rate_limiter.py
import asyncio
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, List


class RateLimiter:
    def __init__(self, rate_limit_per_minute: int):
        self.rate_limit = rate_limit_per_minute
        self.requests: Dict[str, List[datetime]] = defaultdict(list)
        self._lock = asyncio.Lock()
        self.cleanup_task = asyncio.create_task(self.periodic_cleanup())

    async def is_rate_limited(self, client_id: str) -> bool:
        async with self._lock:
            now = datetime.now()
            self._expire_old_requests(client_id, now)

            if len(self.requests[client_id]) >= self.rate_limit:
                return True

            self.requests[client_id].append(now)
            return False

    def _expire_old_requests(self, client_id: str, now: datetime) -> None:
        cutoff = now - timedelta(minutes=1)
        self.requests[client_id] = [
            ts for ts in self.requests[client_id] if ts > cutoff
        ]

    async def periodic_cleanup(self) -> None:
        """Regularly clean up old entries"""
        while True:
            await asyncio.sleep(60)
            async with self._lock:
                now = datetime.now()
                for client_id in list(self.requests.keys()):
                    self._expire_old_requests(client_id, now)
                    if not self.requests[client_id]:
                        del self.requests[client_id]

    async def stop(self):
        self.cleanup_task.cancel()
