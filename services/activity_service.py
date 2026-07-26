from database import get_session
from models import Activity

def list_activities(published_only=True):
    with get_session() as db:
        q = db.query(Activity).order_by(Activity.activity_date.desc(), Activity.id.desc())
        if published_only:
            q = q.filter(Activity.is_published.is_(True))
        items = q.all()
        for item in items:
            _ = list(item.gallery_images)
            db.expunge(item)
        return items
