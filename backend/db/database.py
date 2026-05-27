from sqlalchemy import create_engine

from core.config import settings
from db.base import Base  # noqa: F401 - re-exported for convenience

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {},
)


def init_db() -> None:
    """Import all models to register them, then create tables."""
    import models.user  # noqa: F401
    import models.news_cache  # noqa: F401
    import models.watchlist  # noqa: F401
    import models.news  # noqa: F401
    import models.feedback  # noqa: F401
    Base.metadata.create_all(bind=engine)
