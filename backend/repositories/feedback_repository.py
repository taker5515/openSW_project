from typing import Dict, Tuple, Optional


class FeedbackRepository:
    def __init__(self) -> None:
        # news_id -> (up_count, down_count)
        self._counts: Dict[str, Tuple[int, int]] = {}

    def _ensure(self, news_id: str) -> None:
        if news_id not in self._counts:
            self._counts[news_id] = (0, 0)

    def get(self, news_id: str) -> Tuple[int, int]:
        self._ensure(news_id)
        return self._counts[news_id]

    def add(self, news_id: str, feedback_type: str) -> Tuple[int, int]:
        self._ensure(news_id)
        up, down = self._counts[news_id]
        if feedback_type == "up":
            self._counts[news_id] = (up + 1, down)
        else:
            self._counts[news_id] = (up, down + 1)
        return self._counts[news_id]


feedback_repository = FeedbackRepository()
