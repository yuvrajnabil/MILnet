from database import get_session
from models import WeeklyArchive

def list_archives(published_only=True):
    with get_session() as db:
        q = db.query(WeeklyArchive).order_by(WeeklyArchive.week_number.desc())
        if published_only:
            q = q.filter(WeeklyArchive.is_published.is_(True))
        items = q.all()
        for item in items:
            _ = list(item.posts)
            db.expunge(item)
        return items
