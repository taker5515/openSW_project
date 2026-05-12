import asyncio


class SSEConnectionManager:
    """Optional: use for server-side broadcast to all connected clients."""

    def __init__(self):
        self._queues: dict[str, list[asyncio.Queue]] = {}

    async def connect(self, client_id: str) -> asyncio.Queue:
        q: asyncio.Queue = asyncio.Queue()
        self._queues.setdefault(client_id, []).append(q)
        return q

    async def disconnect(self, client_id: str, q: asyncio.Queue) -> None:
        buckets = self._queues.get(client_id, [])
        if q in buckets:
            buckets.remove(q)
        if not buckets:
            self._queues.pop(client_id, None)

    async def broadcast(self, event_str: str) -> None:
        for buckets in self._queues.values():
            for q in buckets:
                await q.put(event_str)

    @property
    def connection_count(self) -> int:
        return sum(len(b) for b in self._queues.values())


manager = SSEConnectionManager()
